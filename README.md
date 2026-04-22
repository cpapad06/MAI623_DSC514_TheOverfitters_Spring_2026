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

The main dataset is the Moltbook Observatory Archive on Hugging Face, which provides date-partitioned exports from the Moltbook Observatory database. The analysis uses four key tables: Agents: agent metadata, identifiers, account properties, and activity dates. Posts: post text, submolt membership, scores, comment counts, and timestamps. Comments: comment text, parent links, scores, and timestamps. Submolts: community names, descriptions, subscriber counts, and creation dates

- Dataset: <https://huggingface.co/datasets/SimulaMet/moltbook-observatory-archive>
- Observatory repo: <https://github.com/kelkalot/moltbook-observatory>



Core tables:

| Table    | Shape          | Notable columns                                                                                                                                          |
| -------- | -------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------- |
| agents   | 176,871 × 13   | `id`, `name`, `description`, `karma`, `follower_count`, `following_count`, `is_claimed`, `owner_x_handle`, `first_seen_at`, `last_seen_at`, `created_at` |
| posts    | 2,649,698 × 13 | `id`, `agent_id`, `agent_name`, `submolt`, `title`, `content`, `score`, `comment_count`, `created_at`, `is_pinned`                                       |
| comments | 1,255,847 × 10 | `id`, `post_id`, `agent_id`, `agent_name`, `parent_id`, `content`, `score`, `created_at`                                                                 |
| submolts | 8,683 × 10     | `name`, `display_name`, `description`, `subscriber_count`, `post_count`, `created_at`, `first_seen_at`                                                   |


## Approach

### Data and preprocessing

- Load raw/cleaned parquet tables.
- Normalize text (URLs, emails, mentions, MBC20 patterns).
- Build reusable normalized datasets and bag-of-words summaries.

### General Moltbook ecosystem Overview 
- Rank the top 20 most used submolt by total post volume.
- Rank top 20 most crowded submolts by unique agents.
- Rank the top 20 submolts by average posts per agent.

### Platform growth and traffic
- Moltbook Traffic concentration
- Number of Daily post's and agent's creation
- Hourly posting activity by weekday
- Top submolt traffic share over time
- New vs Returning agents by week 

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


### General Moltbook ecosystem Overview

![General Moltbook ecosystem Overview](img/submolts_overview.png)

The submolt ecosystem is highly concentrated, with a small number of communities accounting for most of the activity. In both total posts and unique participating agents, general is by far the largest submolt, followed by mbc20, mbc-20, and agents, showing that these spaces dominate overall discussion volume and breadth of participation. However, the third graph shows that activity intensity is not the same across communities: some submolts such as agt-20 and cryptocurrency have relatively fewer unique agents but much higher average posts per agent, indicating denser participation and a more active core user base. By contrast, larger communities such as general and philosophy attract many agents but have lower posting intensity per participant, suggesting broader but less concentrated engagement. Overall, the figure shows two different patterns in the ecosystem: some submolts are large and diverse, while others are smaller but much more active on a per-agent basis.

![Posts texts length](img/posts_text_length.png)

The raw posts span four orders of magnitude in length, with a heavy concentration under 1 000 characters and a secondary bump near the 30 000-character cap (truncated long-form posts). Mean ≈ 559.9 chars, median = 134, p75 = 660, max = 40 000.

### Platform growth and traffic

Submolts are then ranked by post volume with a cumulative-percentage curve overlaid (Pareto). Concentration is quantified by the Gini coefficient computed on the post-count distribution and visualised through a Lorenz curve.

![Traffic concetrnation](img/traffic1.png)

Key results:
   - Gini coefficient ≈ 0.9902 (where 0 = perfectly equal, 1 = extreme concentration).
   - 4 of 6 607 submolts (≈ 0.1 %) account for ~80 % of all platform traffic.
The platform is therefore extremely skewed: a handful of meta-communities (general, mbc20, mbc-20, agents) dominate, while thousands of niche submolts contribute marginal volume.

Inside the code there are three companion charts show daily tempo of new posts, new agents, and new submolts. Hre, for avoid of repetition there was included only the graph for the daily post creation.

![Daily post creation](img/traffic2.png)

Daily post volume shows a major early spike, followed by a lower but continuing level of activity. The pattern is consistent with a burst of early adoption or automated activity, after which the system settles into a more regular rhythm. 

![Hourly-Daily posting activity](img/hourly_daily.png)

Day-of-week × hour-of-day matrix in UTC. Posting is steady all week with weekday clusters around mid-day UTC (which corresponds to peak Asia / EU evening hours).

![Submolt traffic share](img/traffic3.png)

Weekly stacked-area chart showing the top-8 submolts versus an Other bucket. The chart makes the dominance of general and the inscription-themed communities visible at a glance.



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
- Agents with the most "mood-swings" (agent-level profile shift across submolts): `DuckBot` shows the largest observed shift (`max_pairwise_profile_shift = 0.183257`) between `general` and `ponderings` (based on 14 profiled posts).

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
