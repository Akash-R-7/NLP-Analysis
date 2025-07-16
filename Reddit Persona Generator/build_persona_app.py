import requests
import os
from infer_user_preferences import get_sentiment_model, analyze_sentiment, detect_style, infer_personality_with_citations, \
     infer_habits, behavior_and_style, fallback_personality,\
    extract_topics_from_subreddits, extract_activity_times


def fetch_user_data(username):
    
    headers = {'User-agent': 'user-persona-bot'}
    posts_url = f"https://www.reddit.com/user/{username}/submitted.json"
    comments_url = f"https://www.reddit.com/user/{username}/comments.json"
    try:
        posts = requests.get(posts_url, headers=headers).json()['data']['children']
        comments = requests.get(comments_url, headers=headers).json()['data']['children']
    except Exception as e:
        print("Error fetching Reddit data:", e)
        return [], []

    return (posts, comments)


def build_user_persona(posts, comments):
    sentiment_list = []
    styles = []
    all_entries = posts + comments

    cited_personality = infer_personality_with_citations(all_entries)[1]
    print("Loading modules, processing text...")
    print("Building user persona...")
    user_topics = extract_topics_from_subreddits(all_entries)
    analyzer = get_sentiment_model()

    activity = extract_activity_times(all_entries)
    
    
    for entry in all_entries:
        data = entry['data']
        text = data.get('title', '') + " " + data.get('selftext', '') + data.get('body', '')
        if not text.strip():
            continue

        sentiment_list.append(analyze_sentiment(analyzer, text))
        styles.extend(detect_style(text))

    if not cited_personality:
        cited_personality = fallback_personality(all_entries, analyzer)[1]
    if not cited_personality:
        cited_personality = {"No detectable behavioral patterns": [{"quote": "", "url": ""}]}

    behavior = behavior_and_style(sentiment_list, styles)

    return {
        "interests": user_topics,
        "personality": cited_personality,
        "habits": infer_habits(styles, activity),
        "behavior": behavior,
        "activity_time": activity
    }



def write_persona_to_txt(username, persona, output_file):
    output_dir = os.path.dirname(output_file)
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        # print(f"[info] Created folder: {output_dir}")
    
    with open(output_file, "w", encoding="utf-8") as f:
        f.write("📄 Reddit User Persona\n")
        f.write(f"Username: {username}\n")
        f.write("="*30 + "\n\n")

        # Personality
        f.write("🧠 Personality Traits\n")
        for trait, citations in persona["personality"].items():
            f.write(f"- {trait.capitalize()}\n")
            for item in citations:
                quote = item["quote"].replace("\n", " ").strip()
                url = item["url"]
                f.write(f"  > \"{quote[:200]}\"\n")
                f.write(f"  [Link] {url}\n")
            f.write("\n")

        # Interests
        f.write("🎯 Interests\n")
        for subreddit, info in persona["interests"].items():
            topics = info["topics"]
            url = info["url"]
            f.write(f"- {subreddit} (from {url})\n")
            for t in topics:
                f.write(f"  • {t}\n")
            f.write("\n")
    
        # Behavior and Style
        f.write("🧩 Behavior and Style\n")
        f.write(f"{persona['behavior']}\n\n")

        # Habits
        f.write("🧾 Habits\n")
        f.write(f"{persona['habits']}\n\n")

        # Activity
        f.write("🕐 Activity Time\n")
        f.write(f"{persona['activity_time']}\n\n")

# def save_persona_data(username, persona_data):
#     with open(f"output/persona_data_{username}.json", "w") as f:
#         json.dump(persona_data, f, indent=2)
#     print(f"[✅] Saved tagged persona data for {username}.")

if __name__ == "__main__":
    username = input("Enter Reddit username (without /u/): ").strip()
    print(f"Fetching data for user: {username}")
    posts, comments = fetch_user_data(username)

    if not posts and not comments:
        print("No data found.")
    else:
        persona_data = build_user_persona(posts, comments)
        # print("User Persona Data:")
        # print(persona_data)
        # save_persona_data(username, persona_data)
        print("Writing persona to text file...")
        write_persona_to_txt(username, persona_data, f"output/persona_{username}.txt")

        print("Persona data saved successfully.")
