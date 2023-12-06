import joblib # for importing model

import numpy as np # data handling
import pandas as pd # data handling

from sklearn.preprocessing import LabelEncoder # encode pos/neg sentiment
from sklearn.feature_extraction.text import TfidfVectorizer

def analyze_comments():
    loaded_model = joblib.load(open('Analysis/comment_topic_model.sav', 'rb'))
    loaded_tfidf = joblib.load(open('Analysis/comment_tfidf.sav', 'rb'))
    
    #input comments for model analysis
    new_comments = pd.read_csv('test_comments.csv')
    new_comments['comment'] = new_comments['comment'].apply(lambda x: x[x.find('\n')+1:] if '\n' in x else x) # remove the date from the comment
    new_comments['comment'] = new_comments['comment'].apply(lambda x: x.replace('\n', ' ') if '\n' in x else x) # replace newlines with spaces so words aren't considered as word + \n
    new_comments = new_comments.drop(["game","hours_players"], axis=1)
    
    le = LabelEncoder()
    new_comments["is_Recommended"] = le.fit_transform(new_comments["is_Recommended"])
    
    # Use tf-idf features for NMF.
    tfidf_vectorizer = TfidfVectorizer(
        max_df=0.95, min_df=2, max_features=1000, stop_words="english"
    )
    tfidf = tfidf_vectorizer.fit_transform(new_comments["comment"])
    
    # Vectorize the new text using the same vectorizer used for training
    new_text_tfidf = loaded_tfidf.transform(new_comments["comment"])
    
    # Infer topics with the MBNMFKL model
    new_text_topics_mbnmfkl = loaded_model.transform(new_text_tfidf)
    
    
    #create list of zeros to tally comment contribution to each topic
    MBNMFKLtopics = np.zeros((50,), dtype=int)
    LDAtopics = np.zeros((50,), dtype=int)
    
    for i in range(len(new_comments["comment"])):
        if new_comments["is_Recommended"][i] == 0:
            MBNMFKLtopics[np.argmax(new_text_topics_mbnmfkl[i])] += 1
        elif new_comments["is_Recommended"][i] == 1:
            MBNMFKLtopics[np.argmax(new_text_topics_mbnmfkl[i])] -= 1
    
    maxList = MBNMFKLtopics.copy()
    minList = MBNMFKLtopics.copy()
    
    nonsenseTopics = [0,1,2,5,13,22,24,25,28,30,35,38,40,45,48]
    
    for i in range(len(nonsenseTopics)):
        maxList[nonsenseTopics[i]] = -100
        minList[nonsenseTopics[i]] = 100
    
    posTopicList = []
    
    #Keep grabbing topics from most to least positive until you have three non nonsense categories
    while len(posTopicList) < 3:
        currMaxIndex = np.where(maxList == np.max(maxList))[0][0]
        if len(maxList) == 0:
            break
        else:
            posTopicList.append("Topic " + str(currMaxIndex + 1)) # Get index and adjust for 0 indexing
            maxList[currMaxIndex] = -100
        
    negTopicList = []
    
    #Keep grabbing topics from least to least positive until you have three non nonsense categories
    while len(negTopicList) < 3:
        currMinIndex = np.where(minList == np.min(minList))[0][0]
        if len(minList) == 0:
            break
        else:
            negTopicList.append("Topic " + str(currMinIndex + 1)) # Get index and adjust for 0 indexing
            minList[currMinIndex] = 100
    
    topicDict = {"Topic 4": "Animal/Pets/Friendships",
                 "Topic 5": "Party/Family Game",
                 "Topic 7": "Controls",
                 "Topic 8": "Movie Characters",
                 "Topic 9": "Cute Art Style",
                 "Topic 10": "Puzzles/Thinking",
                 "Topic 11": "Legacy Games",
                 "Topic 12": "Beautiful Art/Soundtrack/Story",
                 "Topic 13": "Dialogue/Interaction",
                 "Topic 15": "Creating",
                 "Topic 16": "Smooth Experience",
                 "Topic 17": "Annoyance",
                 "Topic 18": "Worth Time",
                 "Topic 19": "Multiplayer",
                 "Topic 20": "Cozy/Cute",
                 "Topic 21": "Length/Progression/Achievements",
                 "Topic 22": "Worth Cost",
                 "Topic 24": "Developers/Updates",
                 "Topic 27": "Relaxing",
                 "Topic 28": "Remake",
                 "Topic 30": "Animals/Simulation",
                 "Topic 32": "Emotion Evoking",
                 "Topic 33": "Cooking/Simulation",
                 "Topic 34": "Level Design/Exploration",
                 "Topic 35": "Microtransactions/Value",
                 "Topic 37": "Additional Content/DLCs/Mods",
                 "Topic 38": "Updates",
                 "Topic 40": "Party Game",
                 "Topic 42": "Cars/Driving/Racing",
                 "Topic 43": "Recommended/Worth",
                 "Topic 44": "Survival/Combat/Progression",
                 "Topic 45": "Bugs/Problems",
                 "Topic 47": "Nostalgia",
                 "Topic 48": "Hunting/Fishing",
                 "Topic 50": "Building"}
    
    positive_topics = [topicDict.get(posTopicList[i]) for i in range(min(3, len(posTopicList)))]
    negative_topics = [topicDict.get(negTopicList[i]) for i in range(min(3, len(negTopicList)))]
    
    return positive_topics, negative_topics