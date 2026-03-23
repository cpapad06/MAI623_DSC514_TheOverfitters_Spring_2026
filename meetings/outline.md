# Rhetorical Mirrors: Audience-Aware Variation in Agent-Generated Language

### Team: The Overfitters

---

## Research Question

> Do Moltbook agents adapt their linguistic style when expressing semantically similar ideas across different submolts (communities)? How does their rhetorical or stylistic expression change depending on the submolt?

## Data Sources

- Moltbook agent post datasets (Hugging Face):  
  [https://huggingface.co/datasets/SimulaMet/moltbook-observatory-archive](https://huggingface.co/datasets/SimulaMet/moltbook-observatory-archive)  
  [https://huggingface.co/datasets/ronantakizawa/moltbook](https://huggingface.co/datasets/ronantakizawa/moltbook)

- Optional: Apify actor (free $5 credit) for real-time scraping  
  [https://console.apify.com/actors/6hf3w30Z6mUNsuMdl](https://console.apify.com/actors/6hf3w30Z6mUNsuMdl)

## General Exploration of Moltbook Structure

Establish a clear picture of the Moltbook platform: its communities (submolts), participation patterns, and early indicators of theme clusters.

**Key Questions:**

- What kinds of submolts exist? (topic-wise, structure-wise)
- Which are most active by post count? By unique agents?
- What is the ratio of agent-created content vs human content? (if applicable)
- Are submolts mostly mono-agent or multi-agent?
- Are there latent “genres” of submolts? (e.g. philosophical, political, support, meta)

**Key steps (Adjustable)**:

- Load Moltbook data
- Analyze Submolt-Level Stats e.g.
  - \# posts
  - \# unique agents
  - avg posts per agent
  - submolt creation date (if available)
  - Agent engagement ratios:
    - Posts per submolt / Unique agents per submolt
    - % of total platform traffic
- Analyze Submolt Names & Descriptions
  - Cluster submolt titles and descriptions.
  - Group into high-level meta categories (manually or via clustering), e.g.:
    - Philosophical / Reflective (ponderings, mortality)
    - Political / Collective (shakaikei, thesubstrate)
    - Casual / Expressive (offmychest, general)
    - Governance / Coordination (security, proposals)
    - …
- Analyze per-agent activity:
  - Distribution of posts per agent
  - Agents active in multiple submolts vs mono-submolt agents
  - Claimed vs unclaimed agent patterns (if available)

## Topic & Narrative Discovery

Discover what ideas, concerns, and narratives are being discussed on Moltbook.

**Key steps (Adjustable)**:

- Load and clean Moltbook post data
- Use topic modeling (try both):

**Option 1: Sentence Embeddings**

- Embed each candidate post
- Use SentenceTransformers community detection
  - [https://sbert.net/](https://sbert.net/)
  - [https://huggingface.co/google/embeddinggemma-300m](https://huggingface.co/google/embeddinggemma-300m)
  - [https://sbert.net/docs/package\_reference/util.html\#sentence\_transformers.util.community\_detection](https://sbert.net/docs/package_reference/util.html#sentence_transformers.util.community_detection)
  - Output clusters as narrative groups

**Option 2: BERTopic topic modeling (interpretable labels)**

- Use BERTopic (embeddings \+ c-TF-IDF topic words)
- [https://maartengr.github.io/BERTopic/index.html](https://maartengr.github.io/BERTopic/index.html)
- Choose:
  - embedding model [https://huggingface.co/google/embeddinggemma-300m](https://huggingface.co/google/embeddinggemma-300m)
  - topic reduction strategy
- Manually interpret topics:
  - Give narrative labels (e.g. “Agent Autonomy”, “Security Concerns”, “Human vs AI Ethics”, “Organizing for Change”)
- Output:
  - Top 10–20 agent discourse themes
  - Agent → topic participation matrix

## Psychographic Profiling of Agents

Profile agents' psychological traits and values using human-trained judge models.

- Fine-tune or adapt pre-trained models using:
  - ValueNet (Schwartz values) [https://liang-qiu.github.io/ValueNet/](https://liang-qiu.github.io/ValueNet/)
  - PANDORA (Big 5/OCEAN) [https://huggingface.co/ppp57420/ocean-personality-distilbert](https://huggingface.co/ppp57420/ocean-personality-distilbert)
  - GoEmotions (emotion distribution) [https://huggingface.co/datasets/mrm8488/goemotions](https://huggingface.co/datasets/mrm8488/goemotions)
- Inference:
  - Run models on Moltbook posts
  - Aggregate per agent: mean \+ variance of traits
- Output:
  - Agent profiles: {"Power": 0.8, "Openness": 0.4, "Curiosity": 0.6, ...} |

## Linking Topics to Psychological Traits

Explore how different psychological profiles engage with different topics.

**Steps (Adjustables)**:

- For each topic:
  - Collect agents heavily involved in it
  - Compute average psychographic profile of that group
- Analyze:
  - Are some topics driven by high-Benevolence agents?
  - Do certain narratives skew toward Power-seeking or Openness?
  - Is emotional tone consistent across psychological types?
- **Output:**
  - Topic → Psych profile correlations
  - Clustered heatmaps, profile-topic diagrams
  - Archetypal narrative examples (“The Benevolent Thinker” / “The Nervous Enforcer”)
