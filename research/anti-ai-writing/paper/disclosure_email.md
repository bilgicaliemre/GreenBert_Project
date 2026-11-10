# Disclosure to detector developers (send by about 1 Dec 2026)

ACL's ethics policy asks authors who report ways that detectors can be bypassed to tell the affected
developers before submission and to wait 30 days before posting a preprint. Our skill is not designed to evade
detectors, but the paper reports that its output scores low on three open-source detectors, so we notify all
three. Find each contact on the model's Hugging Face page (the "Community" tab opens a discussion that the
maintainers receive) or the project's GitHub repository. Do not guess email addresses.

- Desklib: https://huggingface.co/desklib/ai-text-detector-v1.01 (also https://github.com/desklib/ai-text-detector)
- Fakespot (Mozilla): https://huggingface.co/fakespot-ai/roberta-base-ai-text-detection-v1
- SuperAnnotate: https://huggingface.co/SuperAnnotate/ai-detector (also https://github.com/superannotateai/generated_text_detector)

Keep a copy of each message and the date sent. The paper's Ethical Considerations section will say when the
developers were notified.

---

**Subject:** Advance notice: student research paper evaluating [model name] on AI-generated text

Hello,

I am a high-school student researcher, and I am writing to let you know about results involving your model,
[model name], before I submit a paper to the NAACL 2027 Student Research Workshop (deadline 11 January 2027).

The paper evaluates a writing-style instruction set for language models. Its goal is better writing: it
removes generic content and stock structures and forbids adding unsupported facts. It is not an evasion tool
and uses no character tricks or paraphrasing attacks. Two results concern your detector:

1. Texts written with the instruction set scored below 20% on [model name] in [n of N] cases, compared with
   [n of N] for the same model writing without it.
2. Human-written texts collected before ChatGPT also scored high: [n of 16] admitted college essays published
   by Hamilton College and Connecticut College scored above 20%. We think personal narrative is outside the
   detector's training domain, and we say so in the paper.

I can share the scored texts, the scoring script and a draft of the paper on request. I plan to wait at least
30 days after this message before posting a preprint. If you see an error in how we ran your model (we used the
code on your model card, with texts split into chunks of about 350 words and a length-weighted mean), I would be
grateful to hear about it.

Thank you for releasing the model openly; it made this study possible.

[Your name]
[School], [City, Country]
