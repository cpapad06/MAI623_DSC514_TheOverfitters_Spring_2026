# Rhetorical Mirrors: Audience-Aware Variation in Agent-Generated Language

A DSC514 group project by **The Overfitters**.

## TL;DR

We study whether Moltbook agents change rhetorical style across communities while discussing similar ideas.
The pipeline combines topic discovery (embedding communities + BERTopic) with psychographic signals (GoEmotions,
OCEAN, Schwartz values), then links topics to agent-level trait patterns.

## Objective

Primary question:

Do Moltbook agents adapt their language style depending on the submolt (community) context?

Operationally, we aim to:

- discover narrative/topic structure in agent discourse,
- estimate post- and agent-level psychographic profiles,
- quantify how topic participation relates to psychological/value signals.

## Data

Source: **Moltbook Observatory Archive** (Hugging Face) and related observatory tooling.

- Dataset: <https://huggingface.co/datasets/SimulaMet/moltbook-observatory-archive>
- Observatory repo: <https://github.com/kelkalot/moltbook-observatory>

Core tables:

- `posts`
- `comments`
- `agents`
- `submolts`

## Approach

### Data and preprocessing

- Load raw/cleaned parquet tables.
- Normalize text (URLs, emails, mentions, MBC20 patterns).
- Build reusable normalized datasets and bag-of-words summaries.

### Agent activity profiling

- Rank the top 20 most active agents by total post volume.
- For each top agent, extract their top 5 submolts by post count.
- Present both a detailed table and a stacked horizontal bar chart with total-post markers for quick comparison.

### Topic and narrative discovery

- **Option 1**: sentence embeddings + community detection.
- **Option 2**: BERTopic for interpretable topic-word structures.
- Produce topic distributions and agent-topic participation matrices.

### Psychographic profiling

- Fine-tune GoEmotions classifier (compact training run).
- Run OCEAN and Schwartz-values classifiers on Moltbook text.
- Build:
  - post-level psychographic table (with `agent`, `submolt`, `post_id`),
  - agent-level profiles (mean/variance by dimension).

### Topic <-> psychographic linkage

- Identify agents heavily involved in each topic.
- Compute topic-wise mean trait/value profiles.
- Run topic-level significance/correlation analyses.
- Surface archetypal high-scoring examples.

## Diagrams

### Top-agent activity profile

![Top agents by top-5 submolts](img/top-agents-top5-submolts.svg)

### End-to-end pipeline

![Pipeline overview](img/pipeline-overview.svg)

This diagram summarizes the full experimental flow:
- start from Moltbook tables (`posts`, `comments`, `agents`, `submolts`),
- normalize and clean text into analysis-ready corpora,
- branch into topic discovery and psychographic inference,
- merge both streams into topic-trait linkage analyses and final interpretation outputs.

### Preprocessed dictionary wordclouds

![Preprocessed posts dictionary wordcloud](img/posts-preprocessed-wordcloud.svg)

![Preprocessed comments dictionary wordcloud](img/comments-preprocessed-wordcloud.svg)

### Topic-to-trait linkage logic

![Topic to psychographic linkage](img/topic-psych-linkage.svg)

This diagram zooms into the linkage stage:
- topics/narratives are estimated from post text,
- psychographic dimensions are inferred at post level and aggregated to agents,
- topic participation is joined with agent traits,
- outputs include correlation/significance views and archetypal topic-trait statements.

## Brief results snapshot

- Data scale in the rendered manuscript includes roughly 2.65M posts in the raw archive and ~1.2M cleaned posts used for downstream analysis.
- Topic discovery reports both embedding-community and BERTopic outputs, including interpretable theme tables and agent-topic participation matrices.
- Baseline narrative classification comparisons (BoW, TF-IDF, Word2Vec) are reported with accuracy, precision, recall, and F1 for transparent method benchmarking.
- The framework successfully extracts coherent narrative groups and topic prevalence summaries.
- Psychographic inference yields dense post-level signals and aggregated agent profiles.
- Topic-conditioned trait patterns can be summarized through heatmaps, correlations, and ranked archetypes.
- Agent-level participation patterns are easy to inspect through the top-agent/top-submolt stacked visualization.

The detailed outputs are documented under `docs/`. The source in [quarto](https://quarto.org/) is under `src/`.

## Results

**Do agents appear to have different psychographic behavior across submolts?**

Yes, current results indicate meaningful psychographic variation across discourse contexts.

Evidence in the rendered report under `docs/`:
- Topic-trait significance testing (Kruskal-Wallis with Benjamini-Hochberg correction) reports many dimensions with extremely small corrected p-values (`q_value`), including multiple emotion dimensions and OCEAN/value dimensions.
- Ranked topic-trait statements show consistent positive and negative deltas versus corpus baselines across distinct narrative clusters (for example, agent/AI and market/trading narratives differ from mbc20-heavy narratives).
- Topic-level psychographic heatmaps and correlation views show non-uniform trait profiles rather than a single shared psychographic pattern.

Interpretation: within this pipeline, agents do not behave psychographically the same way across all submolts/topics; behavior appears context-sensitive and cluster-dependent.

## Acknowledgements

We thank [Demetris Paschalides](https://www.linkedin.com/in/demetris-paschalides-06ab31156/?lipi=urn%3Ali%3Apage%3Ad_flagship3_search_srp_all%3BslYDprEBSOqfgA1%2BhxOE1A%3D%3D) for his guidance throughout the project.

We also acknowledge the use of AI assistance for parts of the implementation workflow, including generating some of the graphs and helping correctly set up CUDA on our system.

## Reproducibility

- Main entrypoint: `src/audience-aware-variation-in-agent-generated-language.qmd`
- To install requirements: `pip install -r requirements.txt`. We recommend using a virtual environment.
- The compiled results were compiled with an (aging) Quadro P4000 graphics card. Additional requirements are in `yiannis-cuda-requirements.txt`
- Build HTML: `make html`
- Full refresh build: `make full/html`
- `HF_TOKEN` required to download `gemma` models: Generate a token from [HF](https://huggingface.co/settings/tokens) and save in `.env`
