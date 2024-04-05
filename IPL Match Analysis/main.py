import streamlit as st
import streamlit.components.v1 as components
from espncricinfo.match import Match
import requests
from bs4 import BeautifulSoup
import copy

from Reddit_matchpost_comments_scrapper_ import get_scorecard, get_reddit_extractor, get_scrapper_url, scrap_comments
from topic_analysis import remove_nulls, remove_stopwords, remove_urls, get_topic_clusters
from emotion_analysis import load_emotion_model, classify_emotions, form_df, plot_histogram, plot_pie


st.title("Recent IPL 2024 Match Analysis")

#### Get recent matches list ####

match_id_dict = {}
# with st.spinner("Getting recent matches..."):
recent_matches = Match.get_recent_matches()
recent_ipl_matches = []
recent_ipl_matches_indexes = []
for match in recent_matches:
    if "indian-premier-league-2024" in match:
        recent_ipl_matches.append(match[match.rindex("/")+1:-37].strip('-'))
        recent_ipl_matches_indexes.append(match[match.index('scorecard')+10:match.rindex("/")])

match_id_dict = dict(zip(recent_ipl_matches, recent_ipl_matches_indexes))
match_id_dict.update({None:0})
# print(match_id_dict)
desc = ""

match_selected = st.selectbox("Select from recent matches",
   list(match_id_dict.keys()),
   index=None,
   placeholder="Select match...",
)


match_id = match_id_dict[match_selected]

if match_id != 0:
    try:
        m = Match(str(match_id))

        desc = m.description
        result = m.result
        
        # with st.container(border=True):
        st.subheader(desc)
        st.markdown(result)

    except:
        # with st.container(border=True):
        st.markdown("Invalid match ID")
st.divider()

#################### OPTIONS ###########################################
display_stat = st.sidebar.selectbox("Match Stats : ", ["Scorecard", "Top Reddit Comments", "Perform Topic Analysis", "Public Emotion"],
                                     index=None, placeholder="Select stat")



################### Get match details ###################################
t1 = ""
t2 = ""
scrapped_url = ""
post_page = ""
reddit = ""
all_comments = []

# st.button("Get Scorecard", type="primary")
if display_stat == "Scorecard" and match_id != 0:
    try:
        with st.spinner("Fetching Scorecard..."):
            if reddit == "":
                reddit = get_reddit_extractor()
                t1, t2, scrapped_url = get_scrapper_url(desc)

                # Send an HTTP GET request to the website
                response = requests.get(scrapped_url)

                # Parse the HTML code using BeautifulSoup
                soup = BeautifulSoup(response.content, 'html.parser')


                link_element = str(soup.find("a", class_="absolute inset-0").get('href'))
                post_page = "https://www.reddit.com"+link_element

            print("Post URL fetched...")
        
        post_title, post_text = get_scorecard(reddit, post_page)
        with st.container(border=True):
            # st.header(post_title)
            st.markdown(post_text)
    except:
        st.markdown("Unable to fetch scorecard currently...")


################ Get recent top reddit comments ##############################################

elif display_stat == "Top Reddit Comments" and match_id != 0:
    try:
        with st.spinner("Fetching Top Comments..."):
            if reddit == "":
                reddit = get_reddit_extractor()
                t1, t2, scrapped_url = get_scrapper_url(desc)

                response = requests.get(scrapped_url)
                soup = BeautifulSoup(response.content, 'html.parser')


                link_element = str(soup.find("a", class_="absolute inset-0").get('href'))
                post_page = "https://www.reddit.com"+link_element

            all_comments = scrap_comments(t1, t2, reddit, post_page)

            print("Comments fetched...")

        st.subheader("Top Comments: ", divider="gray")
        for comment in all_comments[:10]:
            with st.container(border=True):
                st.markdown(comment)
    
    except:
        st.markdown("Unable to fetch comments currently...")


######################### Topic Analysis ##################################################

elif display_stat == "Perform Topic Analysis" and match_id != 0:
    try:
        with st.spinner("Fetching match comments..."):
            reddit = get_reddit_extractor()
            t1, t2, scrapped_url = get_scrapper_url(desc)

            response = requests.get(scrapped_url)
            soup = BeautifulSoup(response.content, 'html.parser')


            link_element = str(soup.find("a", class_="absolute inset-0").get('href'))
            post_page = "https://www.reddit.com"+link_element

            all_comments = scrap_comments(t1, t2, reddit, post_page)

        if len(all_comments) != 0:
            cpy_comments = copy.deepcopy(all_comments)
            non_null_comments = list(map(remove_nulls, cpy_comments))
            url_stripped_input_text = list(map(remove_urls, non_null_comments))
            cleaned_input_text = list(map(remove_stopwords, url_stripped_input_text))

            with st.spinner("Analysing clusters..."):
                topics , file_name = get_topic_clusters(t1, t2, cleaned_input_text)
            try:
                with open(file_name, 'r', encoding="utf-8") as file:
                    html_content = file.read()

                with st.container(border=True):
                    components.html(html_content, height=700)
            except:
                st.markdown("Unable to render figure")
                st.write(topics)
    
    except:
        st.markdown("Error while performing analysis...")


############################# Emotion Recognition ####################################################

elif display_stat == "Public Emotion" and match_id != 0:
    try:
        with st.spinner("Fetching match comments..."):
            reddit = get_reddit_extractor()
            t1, t2, scrapped_url = get_scrapper_url(desc)

            response = requests.get(scrapped_url)
            soup = BeautifulSoup(response.content, 'html.parser')


            link_element = str(soup.find("a", class_="absolute inset-0").get('href'))
            post_page = "https://www.reddit.com"+link_element

            all_comments = scrap_comments(t1, t2, reddit, post_page)

        with st.spinner('Detecting public emotion...'):
            if len(all_comments) != 0:
                tokenizer, model = load_emotion_model()

                comments_for_analysis = []
                if len(all_comments) > 500:
                    comments_for_analysis = all_comments[:500]
                else:
                    comments_for_analysis = all_comments

                preds = classify_emotions(model, tokenizer, comments_for_analysis)
                df = form_df(comments_for_analysis, preds)
            

        with st.spinner("Visualizing..."):
                hist_plot = plot_histogram(df)
                pie_plot = plot_pie(df)

                tab1, tab2 = st.tabs(["Histogram", "Pie Chart"])
                with tab1:
                    st.subheader("Public emotions on Reddit")
                    st.plotly_chart(hist_plot)
                with tab2:
                    st.subheader("Public emotions on Reddit")
                    st.plotly_chart(pie_plot)

    
    except:
        st.markdown("Error while performing analysis...")

    
else:
    st.markdown("")

