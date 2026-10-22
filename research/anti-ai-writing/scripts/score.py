"""Score text files with local open-source AI-text detectors.

usage: python3 score.py file1.txt [file2.txt ...] [--json out.json]

Detectors
  desklib   desklib/ai-text-detector-v1.01 (DeBERTa-v3-large, trained on RAID; MIT)
  fakespot  fakespot-ai/roberta-base-ai-text-detection-v1 (RoBERTa-base; Apache-2.0)
  superannotate  SuperAnnotate/ai-detector (RoBERTa-large; trained incl. Anthropic models + RAID; SAIPL)

Long texts are split into ~350-word chunks on paragraph boundaries; the document
score is the word-weighted mean of chunk probabilities (0-100 = % likely AI).
"""
import json
import re
import sys
from html import unescape

import torch
import torch.nn as nn
from transformers import AutoConfig, AutoModel, AutoTokenizer, AutoModelForSequenceClassification

torch.set_num_threads(4)
CHUNK_WORDS = 350


class DesklibAIDetectionModel(nn.Module):
    # Same architecture as the model card; loaded by hand because the card's
    # PreTrainedModel subclass breaks under transformers 5.x.
    def __init__(self, repo):
        super().__init__()
        from huggingface_hub import hf_hub_download
        from safetensors.torch import load_file
        config = AutoConfig.from_pretrained(repo)
        self.model = AutoModel.from_config(config)
        self.classifier = nn.Linear(config.hidden_size, 1)
        missing, unexpected = self.load_state_dict(load_file(hf_hub_download(repo, 'model.safetensors')), strict=False)
        assert not [k for k in missing if 'position_ids' not in k], missing
        assert not unexpected, unexpected

    def forward(self, input_ids, attention_mask=None):
        h = self.model(input_ids, attention_mask=attention_mask)[0]
        m = attention_mask.unsqueeze(-1).expand(h.size()).float()
        pooled = (h * m).sum(1) / m.sum(1).clamp(min=1e-9)
        return self.classifier(pooled)


def clean_text(t):
    # fakespot's recommended cleaning (utils.py in the model repo)
    t = re.sub(r'```.*?```', '', t, flags=re.DOTALL)
    t = re.sub(r'`[^`]*`', '', t)
    t = re.sub(r'\[([^\]]+)\]\(.*?\)', r'\1', t)
    t = re.sub(r'(\*\*|__)(.*?)\1', r'\2', t)
    t = re.sub(r'#+ ', '', t)
    t = re.sub(r'^(\s*[-*+]|\d+\.)\s+', '', t, flags=re.MULTILINE)
    t = unescape(re.sub(r'<.*?>', '', t))
    t = re.sub(r'[\n\t\r]', ' ', t).replace(' ,', ',')
    return re.sub(' +', ' ', t).strip()


def chunks(text):
    paras = [p.strip() for p in re.split(r'\n\s*\n', text) if p.strip()]
    out, cur = [], []
    for p in paras:
        words = p.split()
        # very long paragraph: split by sentences
        if len(words) > CHUNK_WORDS:
            for s in re.split(r'(?<=[.!?])\s+', p):
                if cur and len(' '.join(cur).split()) + len(s.split()) > CHUNK_WORDS:
                    out.append(' '.join(cur)); cur = []
                cur.append(s)
            continue
        if cur and len(' '.join(cur).split()) + len(words) > CHUNK_WORDS:
            out.append(' '.join(cur)); cur = []
        cur.append(p)
    if cur:
        out.append(' '.join(cur))
    # merge a tiny tail into the previous chunk
    if len(out) > 1 and len(out[-1].split()) < 80:
        tail = out.pop()
        out[-1] += ' ' + tail
    return out


class SuperAnnotateModel(nn.Module):
    # RobertaClassifier from superannotateai/generated_text_detector v1.1.0: <s> token -> linear, sigmoid.
    def __init__(self, repo='SuperAnnotate/ai-detector'):
        super().__init__()
        from huggingface_hub import hf_hub_download
        from safetensors.torch import load_file
        self.roberta = AutoModel.from_config(AutoConfig.from_pretrained('FacebookAI/roberta-large'), add_pooling_layer=False)
        self.dense = nn.Linear(self.roberta.config.hidden_size, 1)
        missing, unexpected = self.load_state_dict(load_file(hf_hub_download(repo, 'model.safetensors')), strict=False)
        assert not [k for k in missing if 'position_ids' not in k], missing
        assert not unexpected, unexpected

    def forward(self, input_ids, attention_mask=None):
        return self.dense(self.roberta(input_ids, attention_mask=attention_mask)[0][:, 0, :])


def sa_preprocess(t):
    # same steps as the SuperAnnotate package (markdown/HTML stripped, URLs/emails removed, whitespace collapsed)
    t = t.replace('\u200B', '')
    t = re.sub(r'<.*?>', '', clean_text(t))
    t = re.sub(r'http[s]?://\S+', '', t)
    t = re.sub(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b', '', t)
    return ' '.join(t.split()).strip()


class Detectors:
    def __init__(self):
        self.dt = AutoTokenizer.from_pretrained('desklib/ai-text-detector-v1.01')
        self.dm = DesklibAIDetectionModel('desklib/ai-text-detector-v1.01').eval()
        self.ft = AutoTokenizer.from_pretrained('fakespot-ai/roberta-base-ai-text-detection-v1')
        self.fm = AutoModelForSequenceClassification.from_pretrained('fakespot-ai/roberta-base-ai-text-detection-v1').eval()
        self.st = AutoTokenizer.from_pretrained('SuperAnnotate/ai-detector')
        self.sm = SuperAnnotateModel().eval()

    @torch.no_grad()
    def desklib(self, text):
        enc = self.dt(text, truncation=True, max_length=768, return_tensors='pt')
        return torch.sigmoid(self.dm(enc['input_ids'], enc['attention_mask'])).item()

    @torch.no_grad()
    def fakespot(self, text):
        enc = self.ft(clean_text(text), truncation=True, max_length=512, return_tensors='pt')
        probs = torch.softmax(self.fm(**enc).logits, -1)[0]
        return probs[1].item()  # id2label: 1 = AI

    @torch.no_grad()
    def superannotate(self, text):
        enc = self.st(sa_preprocess(text), truncation=True, max_length=512, return_tensors='pt')
        return torch.sigmoid(self.sm(enc['input_ids'], enc['attention_mask'])).item()

    def score(self, text):
        cs = chunks(text)
        w = [len(c.split()) for c in cs]
        res = {'words': sum(w), 'chunks': len(cs)}
        for name in ('desklib', 'fakespot', 'superannotate'):
            ps = [getattr(self, name)(c) for c in cs]
            res[name] = round(100 * sum(p * n for p, n in zip(ps, w)) / sum(w), 1)
            res[name + '_chunks'] = [round(100 * p, 1) for p in ps]
        return res


def main(argv):
    out_json = None
    if '--json' in argv:
        i = argv.index('--json'); out_json = argv[i + 1]; argv = argv[:i] + argv[i + 2:]
    det = Detectors()
    results = {}
    print(f"{'file':55s} {'words':>5s} {'desklib%':>9s} {'fakespot%':>10s} {'superann%':>10s}")
    for path in argv:
        r = det.score(open(path, encoding='utf-8').read())
        results[path] = r
        print(f"{path[-55:]:55s} {r['words']:5d} {r['desklib']:9.1f} {r['fakespot']:10.1f} {r['superannotate']:10.1f}")
    if out_json:
        json.dump(results, open(out_json, 'w'), indent=1)


if __name__ == '__main__':
    main(sys.argv[1:])
