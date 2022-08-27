# IMPORTS 
import csv
import numpy as np
# import pandas as pd
# from pandas import read_csv

# to prevent against openmp issue
import os
os.environ['KMP_DUPLICATE_LIB_OK']='True'

from sentence_transformers import SentenceTransformer
from sklearn.cluster import KMeans

# imports for NLP
import nltk
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')
nltk.download('omw-1.4')
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from dateutil import parser
import string
import re

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.decomposition import LatentDirichletAllocation as LDA

embedder = SentenceTransformer('all-MiniLM-L6-v2')
SIZES = {}

#################################################
## HELPER FUNCTIONS

# NLP functions for cleaning text
def remove_punctuation(input):
  return input.translate(str.maketrans('','', string.punctuation))

def remove_whitespaces(input):
  return " ".join(input.split())

def tokenize(input):
  return word_tokenize(input)

def remove_stop_words(input):
  input = word_tokenize(input)
  return [word for word in input if word not in stopwords.words('english')]

def lemmatize(input):
  lemmatizer=WordNetLemmatizer()
  input_str=word_tokenize(input)
  new_words = []
  for word in input_str:
    new_words.append(lemmatizer.lemmatize(word))
  return ' '.join(new_words)

# overall pipeline for cleaning text
def nlp_pipeline(text): 
  return lemmatize(' '.join(remove_stop_words(remove_whitespaces(remove_punctuation(text)))))

# given list of words, finds overarching topic
def find_topics(word_cluster):
    text = ' '.join(word_cluster)
    count_vectorizer = CountVectorizer(stop_words='english')
    count_data = count_vectorizer.fit_transform([text])

    number_of_tags = 1 # number of topics wanted
    lda = LDA(n_components=1, n_jobs=-1)
    lda.fit(count_data)

    words = count_vectorizer.get_feature_names_out()
    # Get topics from model
    topics = [[words[i] for i in topic.argsort()[:-number_of_tags - 1:-1]] for (topic_idx, topic) in enumerate(lda.components_)]

    topics = np.array(topics).ravel()
    return topics

def clean_text(text):
    # remove numbers
    text_nonum = re.sub(" \d+", " ", text)
    # remove punctuations and convert characters to lower case
    text_nopunct = "".join([char.lower() for char in text_nonum if char not in string.punctuation]) 
    # substitute multiple whitespace with single whitespace
    # Also, removes leading and trailing whitespaces
    text_no_doublespace = re.sub('\s+', ' ', text_nopunct).strip()
    return text_no_doublespace

# Perform kmeans clustering on list of phrases
# need to specify number of clusters wanted (k)
def generate_clusters(num_clusters, phrase_list, SIZES):
  sentence_emb = embedder.encode(phrase_list)
  clusters = {}

  clustering_model = KMeans(n_clusters=num_clusters)
  clustering_model.fit(sentence_emb)
  cluster_assignment = clustering_model.labels_

  clustered_sentences = [[] for i in range(num_clusters)]
  for sentence_id, cluster_id in enumerate(cluster_assignment):
      clustered_sentences[cluster_id].append(phrase_list[sentence_id])

  for i, cluster in enumerate(clustered_sentences):
    topic = find_topics(cluster)[0]
    cluster = [i for i in cluster if i]
    clusters[topic] = cluster
    SIZES[topic] = len(cluster)
  return clusters, SIZES


#######################################################
## DATA ANALYSIS + CLUSTER GENERATION


def create_graph():
  # import csv data 
  history = []
  with open('../search_terms.csv', 'r') as csvfile:
      datareader = csv.reader(csvfile)
      for row in datareader:
          # prints normalized term
          history.append(row[3])

  GRAPH = {}
  SIZES = {}

  print('history length:', len(history))

  if len(history) == 1:
    starting_topics = ['Welcome', 'To', 'Lotus']
    print('len history is 1!!')
    for topic in starting_topics:
      GRAPH[topic] = []
      SIZES[topic] = 30

  else:
    # clean data
    history = [nlp_pipeline(h) for h in history]
    history = [clean_text(h) for h in history]

    # print(len(history))
    # create root clusters
    print("generating roots")
    roots, SIZES = generate_clusters(10, history, SIZES)

    print("roots: ", roots)

    # print("got here 1")

    # do BFS to generate child clusters and create tree graph of parent-child edges
    queue = []

    clusters = roots
    size_thresh = 20
    num_children = 3

    # add original parent topics
    for topic in roots.keys():
        GRAPH[topic] = set()
        if SIZES[topic] >= size_thresh:
            queue.append(topic)
    print("graph keys:", GRAPH.keys())


    # print("got here 2")

    # BFS
    while len(queue) > 0:
      parent_topic = queue.pop(0)
      # print('parent', parent_topic)
      parent_cluster = clusters[parent_topic]
      if len(parent_cluster) >= size_thresh and len(set(parent_cluster)) > num_children:
        new_clusters, SIZES = generate_clusters(num_children, parent_cluster, SIZES)
        for child_topic in new_clusters.keys():
          if child_topic not in clusters.keys():
            # print('child', child_topic)

            # add links between parent + child to graph
            GRAPH[child_topic] = set()
            GRAPH[child_topic].add(parent_topic)
            GRAPH[parent_topic].add(child_topic)

            new_c = new_clusters[child_topic]
            clusters[child_topic] = new_c
            SIZES[child_topic] = len(new_c)

            # add child to queue if we re-cluster again
            if SIZES[child_topic] >= size_thresh:
              queue.append(child_topic)


    for k in GRAPH.keys():
      GRAPH[k] = list(GRAPH[k])

  print('graph:', GRAPH)
  return GRAPH, SIZES