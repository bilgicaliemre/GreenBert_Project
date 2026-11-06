"""Binoculars zero-shot detector (Hans et al., ICML 2024) with a small Qwen2.5 observer/performer pair.
score = log-perplexity(performer) / cross-perplexity(observer -> performer). LOWER = more machine-like.
Thresholds must be calibrated for this model pair (paper's 0.90 threshold is for Falcon-7B)."""
import sys, json, torch
from transformers import AutoTokenizer, AutoModelForCausalLM
torch.set_num_threads(4)
OBS, PERF = 'Qwen/Qwen2.5-1.5B', 'Qwen/Qwen2.5-1.5B-Instruct'

class Binoculars:
    def __init__(self, dtype=torch.bfloat16):
        self.tok = AutoTokenizer.from_pretrained(OBS)
        self.obs = AutoModelForCausalLM.from_pretrained(OBS, dtype=dtype).eval()
        self.perf = AutoModelForCausalLM.from_pretrained(PERF, dtype=dtype).eval()

    @torch.no_grad()
    def score(self, text, max_tokens=512):
        enc = self.tok(text, return_tensors='pt', truncation=True, max_length=max_tokens)
        lo = self.obs(**enc).logits[0, :-1].float()
        lp = self.perf(**enc).logits[0, :-1].float()
        tgt = enc['input_ids'][0, 1:]
        ppl = torch.nn.functional.cross_entropy(lp, tgt)            # performer log-ppl
        x_ppl = (torch.softmax(lo, -1) * -torch.log_softmax(lp, -1)).sum(-1).mean()  # cross-ppl
        return (ppl / x_ppl).item()

if __name__ == '__main__':
    import time; t=time.time(); b = Binoculars(); print('load', round(time.time()-t,1),'s')
    for p in sys.argv[1:]:
        t=time.time(); s=b.score(open(p).read()); print(f'{p:40s} {s:.4f}  ({time.time()-t:.1f}s)')
