import json
import praw

def get_reddit_extractor():
    client_id = ""
    client_secret = ""

    with open("reddit_keys.json") as infile:
        json_obj = json.load(infile)
        client_id = json_obj["Client ID"]
        client_secret = json_obj["Client Secret"]

    reddit = praw.Reddit(user_agent=True, client_id=client_id,
                        client_secret=client_secret)
    
    return reddit


# result_text = "Indian Premier League, 15th Match: Royal Challengers Bengaluru v Lucknow Super Giants at Wankhede, Apr 1, 2024"


def get_scrapper_url(text):
    team1 = text[text.index(':')+2:text.index(' v ')]
    team_1_cated = '+'.join(team1.split())
    team2 = text[text.index(' v ')+3:text.index(' at')]
    team_2_cated = '+'.join(team2.split())
    scrapper_url = "https://www.reddit.com/search/?q="+team_1_cated+"+v+"+team_2_cated+"&t=week"
    # https://www.reddit.com/search/?q=Mumbai+Indians+v+Rajasthan+Royals&t=week
    return (team1, team2, scrapper_url)

def get_scorecard(reddit, post_page):
    post = reddit.submission(url=post_page)
    return (post.title, post.selftext)

# @st.cache_data(show_spinner=False, ttl=3600, max_entries=2000)
def scrap_comments(t1, t2, reddit, post_page):
    # dataset = []
    all_comments = []

    post = reddit.submission(url=post_page)
    comment_ctr = 0

    post.comments.replace_more(limit=10) # None for loading more comments
    for comment in post.comments.list(): # does BFS on comment levels
        if comment_ctr >= 1500:
            break
        # dataset.extend([{'comment': comment.body}])
        all_comments.append(comment.body)
        comment_ctr += 1

    # df = pd.DataFrame(dataset)
    # df.to_csv(t1+'_vs_'+t2+'_reddit_comments.csv', index=False)
    print(len(all_comments))
    return all_comments
    