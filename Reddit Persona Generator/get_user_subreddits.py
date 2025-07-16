import requests



# def get_nlp():
#     import spacy
#     return spacy.load("en_core_web_sm")

def get_pos_tagger():
    from nltk import pos_tag, word_tokenize, RegexpParser
    return word_tokenize, pos_tag, RegexpParser

def get_subreddit_description(subreddit):
    url = f"https://www.reddit.com/r/{subreddit}/about.json"
    try:
        data = requests.get(url, headers={'User-agent': 'topic-parser'}).json()
        return data['data'].get('public_description', '').strip()
    except Exception:
        return ""



def extract_topic_from_subreddit(subreddit_name, description):
    if not isinstance(description, str):
        print(f"[warn] Description for r/{subreddit_name} is not a string: {description}")
        return [subreddit_name.replace('_', ' ').lower()]

    word_tokenize, pos_tag, RegexpParser = get_pos_tagger()
    try:
        tokens = word_tokenize(description)
        # print('Tokens here: ', tokens)
        tagged = pos_tag(tokens)
        # print('POS tags here: ', tagged)

        grammar = "NP: {<DT>?<JJ.*>*<NN.*>+}"
        cp = RegexpParser(grammar)
        tree = cp.parse(tagged)

        phrases = []
        for subtree in tree.subtrees(filter=lambda t: t.label() == 'NP'):
            phrase = " ".join(word for word, tag in subtree.leaves())
            if 2 <= len(phrase) <= 40:
                phrases.append(phrase)

        return list(dict.fromkeys(phrases)) or [subreddit_name.replace('_', ' ').lower()]

    except Exception as e:
        print(f"[error] Failed to extract topic for r/{subreddit_name}: {e}")
        return [subreddit_name.replace('_', ' ').lower()]