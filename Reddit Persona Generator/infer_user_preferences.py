from collections import Counter
from datetime import datetime, timezone
from personality_patterns import personality_patterns
import re
from get_user_subreddits import extract_topic_from_subreddit, get_subreddit_description



####################### User's interests ##########################
def extract_topics_from_subreddits(entries):
    topic_dict = {}
    for e in entries[:10]:  # limit to first 10 subreddits
        subreddit = e['data'].get('subreddit')
        if subreddit and subreddit not in topic_dict:
            desc = get_subreddit_description(subreddit)
            topics = extract_topic_from_subreddit(subreddit, desc)
            topic_dict[subreddit] = {
                "topics": topics[:2],  # top 2 noun chunks per subreddit
                "url": f"https://reddit.com/r/{subreddit}"
            }
    return topic_dict


######################## Sentiment and Style Analysis ##########################

def get_sentiment_model():
    from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
    return SentimentIntensityAnalyzer()

def analyze_sentiment(analyzer, text):
    score = analyzer.polarity_scores(text)
    if score['compound'] >= 0.5:
        return 'Positive'
    elif score['compound'] <= -0.5:
        return 'Negative'
    else:
        return 'Neutral'

def detect_style(text):
    style = []
    if len(text) < 50:
        style.append("short")

    if '😂' in text or 'lol' in text.lower():
        style.append("humorous")

    if len(re.findall(r'[.!?]', text)) > 5: # too much punctuation
        style.append("expressive")

    return style if style else ["neutral"]  

######################### Activity Times ##########################
def extract_activity_times(entries):
    hours = []
    for e in entries:
        utc_time = datetime.fromtimestamp(e['data']['created_utc'], tz=timezone.utc)
        hours.append(utc_time.hour)
    if not hours:
        return "Unknown"
    avg = sum(hours) / len(hours)
    if 5 <= avg < 12:
        return "Mornings"
    elif 12 <= avg < 18:
        return "Afternoons"
    elif 18 <= avg < 24:
        return "Evenings"
    else:
        return "Late nights"
    


########################### Personality Traits ##############################

def infer_personality_with_citations(entries):
    traits = []
    trait_citations = {}

    for e in entries:
        text = e['data'].get('body') or e['data'].get('selftext') or ""
        url = f"https://reddit.com{e['data']['permalink']}"

        for trait, patterns in personality_patterns.items():
            if any(p in text.lower() for p in patterns):
                traits.append(trait)
                if trait not in trait_citations:
                    trait_citations[trait] = []
                trait_citations[trait].append({"quote": text[:200], "url": url})
    
    trait_summary = ", ".join(set(traits)) or "neutral or hard to determine"
    return trait_summary, trait_citations
   

def fallback_personality(entries, analyzer):
    # Fallback personality traits from semantic analysis
    fallback_traits = {}
    for e in entries:
        text = e['data'].get('body') or e['data'].get('selftext') or ""
        url = f"https://reddit.com{e['data']['permalink']}"
        lowered = text.lower()

        # Detect curiosity
        if "?" in text or any(q in lowered for q in ["how do", "why does", "i wonder", "can anyone"]):
            fallback_traits.setdefault("curious", []).append({"quote": text[:200], "url": url})

        # Detect optimism
        if analyzer.polarity_scores(text)["compound"] > 0.5:
            fallback_traits.setdefault("generally optimistic", []).append({"quote": text[:200], "url": url})

        # Detect expressiveness
        if len(text) > 150 and "!" in text:
            fallback_traits.setdefault("expressive", []).append({"quote": text[:200], "url": url})

    if fallback_traits:
        trait_summary = ", ".join(sorted(fallback_traits.keys()))
        return trait_summary, fallback_traits

    return "Unable to determine dominant traits with confidence.", {}




def behavior_and_style(sentiment_list, styles):
    personality_traits = []

    # Sentiment-based tone
    sentiment_mode = Counter(sentiment_list).most_common(1)[0][0]
    if sentiment_mode == 'Positive':
        personality_traits.append("generally optimistic")
    elif sentiment_mode == 'Negative':
        personality_traits.append("possibly critical or frustrated")
    else:
        personality_traits.append("neutral or balanced")

    # Style-based traits
    style_mode = Counter(styles).most_common(1)[0][0]
    if 'short' in style_mode:
        personality_traits.append("tends to be concise")
    if 'humorous' in style_mode:
        personality_traits.append("occasionally humorous")
    if 'expressive' in style_mode:
        personality_traits.append("emotionally expressive")

    return ", ".join(personality_traits)



def infer_habits(styles, activity_time):
    habits = []

    if 'short' in styles:
        habits.append("prefers short-form replies")
    if 'humorous' in styles:
        habits.append("uses emojis or humor regularly")

    habits.append(f"active mostly during {activity_time.lower()}")

    return ", ".join(habits)

