
# Reddit User Persona Generator

This tool extracts a user's Reddit comments and posts, analyzes their behavior, and builds a **grounded, citation-backed user persona**. It's built for accuracy, explainability, and flexibility.

---

## Features

*  Scrapes public Reddit posts and comments using only a username
*  Extracts personality traits, habits, interests, and activity patterns
*  Traits are backed by **quotes and citations**
*  Outputs a human-readable `.txt` persona report
*  100% local and offline — no API keys required

---

## 🗂️ Folder Structure

```
Reddit Persona Generator/
├── output/                      # Generated persona reports (.txt)
├── build_persona_app.py         # Main script
├── get_user_subreddits.py       # Subreddit → topic mapping
├── infer_user_preferences.py    # Trait & topic extraction
├── personality_patterns.py      # Phrase-based personality mapping
├── requirements.txt             # Python dependencies
```

---

## Installation

### 1️⃣ Clone the repository

```bash
git clone https://github.com/Akash-R-7/NLP-Analysis.git
cd "NLP-Analysis/Reddit Persona Generator"
```
---

### 2️⃣ Set up environment

```bash
# For conda:
conda create -n reddit-persona python=3.10.13
conda activate reddit-persona
```
---

### 3️⃣ Install dependencies

```bash
pip install -r requirements.txt
```
---

### 4️⃣ Download required NLTK data

```bash
import nltk
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
nltk.download('punkt_tab')
nltk.download('averaged_perceptron_tagger_eng')
```
---

## How to Run

```bash
python build_persona_app.py
```

Then follow the prompt:

```bash
Enter Reddit username (without /u/):
```

Outputs:<br>
`output/persona_<username>.txt` — formatted persona with citations

## Sample Output

<img width="1208" height="921" alt="image" src="https://github.com/user-attachments/assets/c4749bb5-41ad-4a55-8927-b47f2e18d227" />


## Notes:
* The method scrapes user's comments and posts, along with additional information like time, subreddit info. to build on persona.
* Uses Sentiment analyzer, POS taggers and rule-based modules to get relevant information about user grounded in proper citations.
* The advantage that follow such an approach are: zero cost, low-latency, proper citations, and interpretability.
* Other approach with open-sorce LLMs using Ollama was also tested, with some prompting techniques, but the results were unsatisfactory with hallucinations, increased latency, and inability to proper citing.

