from nltk.tokenize import word_tokenize
import re
# from sentence_transformers import SentenceTransformer
# from bertopic import BERTopic

from sklearn.decomposition import NMF
from sklearn.feature_extraction.text import CountVectorizer
from topicwizard.pipeline import make_topic_pipeline
from topicwizard.figures import topic_wordclouds, topic_map, topic_barcharts



stopwords = ['i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'you', "you're", "you've", "you'll", "you'd", 'your', 'yours', 'yourself', 
'yourselves', 'he', 'him', 'his', 'himself', 'she', "she's", 'her', 'hers', 'herself', 
'it', "it's", 'its', 'itself', 'they', 'them', 'their', 'theirs', 'themselves',
 'what', 'which', 'who', 'whom', 'this', 'that', "that'll", 'these', 'those', 'am', 'is', 'are',
 'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 'having', 'do', 'does', 'did', 'doing',
 'a', 'an', 'the', 'and', 'but', 'if', 'or', 'because', 'as', 'until', 'while', 'of', 'at', 'by', 'for', 
'with', 'about', 'against', 'between', 'into', 'through', 'during', 'before', 'after', 'above', 'below', 'to', 
'from', 'up', 'down', 'in', 'out', 'on', 'off', 'over', 'under', 'again', 'further', 'then', 'once', 
'here', 'there', 'when', 'where', 'why', 'how', 'all', 'any', 'both', 'each', 'few', 'more', 'most', 
'other', 'some', 'such', 'no', 'nor', 'not', 'only', 'own', 'same', 'so', 'than', 'too', 'very', 
's', 't', 'can', 'will', 'just', 'don', "don't", 'should', "should've", 'now', 'd', 'll', 'm', 'o', 're', 've', 'y',
 'ain', 'aren', "aren't", 'couldn', "couldn't", 'didn', "didn't", 'doesn', "doesn't", 
'hadn', "hadn't", 'hasn', "hasn't", 'haven', "haven't", 'isn', "isn't", 'ma', 'mightn',
 "mightn't", 'mustn', "mustn't", 'needn', "needn't", 'shan', "shan't", 'shouldn', "shouldn't", 
'wasn', "wasn't", 'weren', "weren't", 'won', "won't", 'wouldn', "wouldn't"]


def isNaN(string):
    return string != string


def remove_nulls(comment):
    if not isNaN(comment):
        return comment
    
def remove_urls(text, replacement_text=""):
    # Define a regex pattern to match URLs
    url_pattern = re.compile(r'https?://\S+|www\.\S+')
 
    # Use the sub() method to replace URLs with the specified replacement text
    text_without_urls = url_pattern.sub(replacement_text, text)
 
    return text_without_urls.strip()


def remove_stopwords(input_text):
    word_tokens = word_tokenize(input_text)
    
    filtered_sentence = [w for w in word_tokens if not w.lower() in stopwords]
    return " ".join(filtered_sentence)
    
# def get_topic_clusters(t1, t2, cleaned_input_text):
#     sentence_model = SentenceTransformer('sentence-transformers/all-mpnet-base-v2')
#     model = BERTopic(embedding_model=sentence_model, nr_topics=None, verbose=True)

#     doc_topics, prob_topics = model.fit_transform(cleaned_input_text)

#     topics = model.get_topics()

#     # fig = model.visualize_barchart()
#     file_name = t1+"_"+t2+"_"+"file.html"
#     fig = model.visualize_topics()
#     fig.write_html(file_name)

#     return (topics, file_name)

def topicwizard_plots(cleaned_input_text):
    bow_vectorizer = CountVectorizer()
    nmf = NMF(n_components=8)
    pipeline = make_topic_pipeline(bow_vectorizer, nmf)

    topic_data_nmf = pipeline.prepare_topic_data(cleaned_input_text)

    topical_map = topic_map(topic_data_nmf)
    topical_map.update_layout(height=700, width=900, font_color="#000")

    topical_barchart = topic_barcharts(topic_data_nmf)
    topical_barchart.update_layout(height=700, width=900, paper_bgcolor="#fff", font_color="#000", 
                                   legend_font_color="#000")

    topical_word_cloud = topic_wordclouds(topic_data_nmf)
    topical_word_cloud.update_layout(height=800, width=900, paper_bgcolor="#fff", font_color="#000")

    return (topical_map, topical_barchart, topical_word_cloud)
