# tellcheck.py

A quick check of your own draft for the surface patterns that blind judges cited most often for model-written text
in our benchmarks (DEVLOG sections 21 to 24).

```bash
python3 research/anti-ai-writing/tools/tellcheck.py my_draft.txt --genre short     # short answers, supplements
python3 research/anti-ai-writing/tools/tellcheck.py my_abstract.txt --genre abstract
python3 research/anti-ai-writing/tools/tellcheck.py my_essay.txt --genre essay
```

It prints a few lines such as "Hedges (1.2 per 100 words)" or "Average sentence 11 words; real short answers in our
data average 21.8", each with what to look at. It is not an AI detector and it does not prove anything about who
wrote a text: a human draft can trip it and a model draft can pass it. Never fix a flag by adding errors or tricks;
fix the sentence.

How well do these surface features alone separate real pre-2022 writing from model writing in our data? With a
cross-validated logistic model over all features: admitted essays AUC 0.997, admitted short answers 0.92, charity
appeals 0.80, science-fair abstracts 0.77 (`eval/results/modes/surface_auc.json`).
