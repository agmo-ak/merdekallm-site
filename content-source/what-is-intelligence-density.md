---
title: Intelligence Density: Why the Next AI Breakthroughs Will Be Smaller, Not Bigger
author: Merdeka LLM Team
date: 2026-10-09
readtime: 5 min read
---

The most important shift in the AI race may no longer be model size. For years, progress came from scaling training runs: more GPUs, more parameters, more data. The new frontier is **intelligence density**: how much useful reasoning a model delivers per unit of compute, per parameter and per ringgit.

In this framing, the most powerful model is not necessarily the largest one. It is the one that delivers the most capability for the hardware it runs on. For Malaysian schools, government agencies and organisations that work in Bahasa Malaysia, that difference decides whether AI is something you rent from overseas or something you own.

### What is intelligence density?

Researchers at Tsinghua University gave the idea a precise form in [Densing Law of LLMs](https://www.nature.com/articles/s42256-025-01137-0) (Xiao et al., *Nature Machine Intelligence*, 2025). They define *capability density* as the size a reference model needs to match a model's score, divided by that model's actual size. A model with high density does the work of a much larger one.

Their key finding is that the best density among open models doubles about every three and a half months. Every few months, a model half the size can match the previous state of the art. Scale still matters, but the gains now come as much from better data, better training and sharper specialisation as from more parameters.

### Why it matters for Malaysia

A model's size decides where it can run. A model with hundreds of billions of parameters needs a data-centre cluster, so most organisations can only reach it through a foreign cloud. A dense, compact model fits on a single server that a school, a hospital or a ministry can own.

That brings three practical benefits:

- **Data stays at home.** Questions, documents and student work never leave your own premises, which keeps PDPA compliance simple.
- **Lower cost.** One GPU server costs a small fraction of the hardware a frontier-scale model needs, and there is no per-token bill to an overseas provider.
- **Resilience.** The model runs on your own network, so work does not stop when the internet or an outside provider does.

High intelligence density is what makes AI sovereignty practical, not only possible.

### MerdekaLLM-Sasbadi-27b: built for density

[MerdekaLLM-Sasbadi-27b](/merdeka-model-llm/) is fine-tuned with Sasbadi on Malaysian curriculum content: textbooks and learning materials written in standard, formal Bahasa Malaysia. That makes it a natural fit for schools, and for any government agency or organisation that needs clear, formal Bahasa Malaysia. It has 27 billion parameters and scores **84.9%** on MalayMMLU, the Malay-language benchmark of 24,213 questions across 22 Malaysian school subjects (internal evaluation, 26 August 2026). That is the highest score of the Malaysian-built models in our comparison against the [Pendakwah Teknologi leaderboard](https://pendakwah.tech/bahasa/mmlu/), and within seven points of the top frontier model.

Every other model in that comparison that publishes its size has 397 billion parameters or more. Measured as MalayMMLU accuracy per billion parameters, MerdekaLLM-Sasbadi-27b scores **3.1 points per billion**. The next-densest model scores about 0.22: our model delivers roughly **15 times** more Malay-language accuracy per parameter. That is the highest intelligence density in our comparison.

In practice, the whole model fits on a single 80 GB GPU. You can self-host it on your own server, in your own building, on your own network. No prompt, document or student record goes to an overseas cloud, and no outside provider can switch it off or change its terms. That is sovereign AI in practice: you own the model, the hardware and the data.

### How we measure it

We want this claim to be easy to check, so here is how we count:

- We divide MalayMMLU accuracy by **total** parameters, because total parameters decide the memory, and so the hardware, you need to host a model.
- Mixture-of-experts models use only part of their parameters for each token. Counted per *active* parameter, some of them score higher. They still need all of their parameters in memory to run.
- We include only models whose developers publish a parameter count. Closed models such as Gemini, GPT and Claude do not, so we cannot rank them.
- Our score is an internal evaluation, scored the same way as the leaderboard, on the full MalayMMLU set.

The full chart, the comparison table and the sources are on the [Merdeka Model Hub](/merdeka-model-llm/#local).

### The road ahead

If the densing trend holds, the models that matter most to Malaysia will not be the biggest ones. They will be the ones that do the most with the least: fluent in formal Bahasa Malaysia, trained on local data, and small enough to run on Malaysian soil. That is the model we are building.

Need an AI model that works in formal Bahasa Malaysia and runs on your own machine, so your data never leaves your school, agency or organisation? Want to help us build the next Merdeka model? [Get in touch](/#contact).
