# IMPORTS
from time import time

import nltk

import matplotlib.pyplot as plt

from sklearn.decomposition import NMF, LatentDirichletAllocation, MiniBatchNMF
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer





#DATA CLEANING
nltk.download('stopwords') # get english stopwords
stop_words = set(stopwords.words('english')) # set them as the chosen stopwords

comments = pd.read_csv('C:/Users/aidan/OneDrive/Documents/GitHub/PIC16BProject/steam_scraper/reviews.csv') # import the dataset

comments['date'] = comments['comment'].apply(lambda d: d[8:d.find('\n')]) # set comment column to content excluding the first 8 characters: "Posted:"
comments['comment'] = comments['comment'].apply(lambda x: x[x.find('\n')+1:] if '\n' in x else x) # remove the date from the comment by finding first line break
comments['comment'] = comments['comment'].apply(lambda x: x.replace('\n', ' ') if '\n' in x else x) # replace newlines with spaces so words aren't considered as word + \n

le = LabelEncoder()
comments["is_Recommended"] = le.fit_transform(comments["is_Recommended"]) # map recommended/not recommended to 1/0

comments = comments.drop(["game", "hours_players","date"], axis=1) # drop data irrelevant to topic modeling
comments = comments.sample(frac = 1) # shuffle all rows in comments





#TOPIC MODELING
# set features of the model
n_samples = 2000
n_features = 1000
n_components = 10
n_top_words = 20
batch_size = 128
init = "nndsvda"

# vectorize the comments
# Use tf-idf features for NMF.
print("Extracting tf-idf features for NMF...")
tfidf_vectorizer = TfidfVectorizer(
    max_df=0.95, min_df=2, max_features=n_features, stop_words="english"
)
t0 = time()
tfidf = tfidf_vectorizer.fit_transform(comments["comment"])
print("done in %0.3fs." % (time() - t0))

# Use tf (raw term count) features for LDA.
print("Extracting tf features for LDA...")
tf_vectorizer = CountVectorizer(
    max_df=0.95, min_df=2, max_features=n_features, stop_words="english"
)
t0 = time()
tf = tf_vectorizer.fit_transform(comments["comment"])
print("done in %0.3fs." % (time() - t0))
print()


# Fit the MiniBatchNMF model
#USING MINIBATCH KULLBACK-LEIBLER AS IT WAS BEST SUITED FOR LIMITED INFORMAITON CLASSIFICATION IN OUR CONTEXT OF LIMITED COMMENTS
print(
    "\n" * 2,
    "Fitting the MiniBatchNMF model (generalized Kullback-Leibler "
    "divergence) with tf-idf features, n_samples=%d and n_features=%d, "
    "batch_size=%d..." % (n_samples, n_features, batch_size),
)
t0 = time()
mbnmfkl = MiniBatchNMF(
    n_components=n_components,
    random_state=1,
    batch_size=batch_size,
    init=init,
    beta_loss="kullback-leibler",
    alpha_W=0.00005,
    alpha_H=0.00005,
    l1_ratio=0.5,
).fit(tfidf)
print("done in %0.3fs." % (time() - t0))

tfidf_feature_names = tfidf_vectorizer.get_feature_names_out()
plot_top_words(
    mbnmfkl,
    tfidf_feature_names,
    n_top_words,
    "Topics in MiniBatchNMF model (generalized Kullback-Leibler divergence)",
)

print(
    "\n" * 2,
    "Fitting LDA models with tf features, n_samples=%d and n_features=%d..."
    % (n_samples, n_features),
)
lda = LatentDirichletAllocation(
    n_components=n_components,
    max_iter=5,
    learning_method="online",
    learning_offset=50.0,
    random_state=0,
)
t0 = time()
lda.fit(tf)
print("done in %0.3fs." % (time() - t0))

tf_feature_names = tf_vectorizer.get_feature_names_out()
plot_top_words(lda, tf_feature_names, n_top_words, "Topics in LDA model")






#GETTING TOPICS FROM NEW GAME'S COMMENTS
# New piece of text
new_text = ("I hate this game way too expensive and so many dlcs", 0)

# Preprocess the new text
# You need to perform the same preprocessing steps you did for the training data
# Assuming the same preprocessing steps as in your code

# Vectorize the new text using the same vectorizer used for training
new_text_tfidf = tfidf_vectorizer.transform([new_text[0]])

# Infer topics with the MBNMFKL model
new_text_topics_mbnmfkl = mbnmfkl.transform(new_text_tfidf)

# Infer topics with the LDA model
new_text_topics_lda = lda.transform(tf_vectorizer.transform([new_text[0]]))

#create list of zeros to tally comment contribution to each topic
MBNMFKLtopics = np.zeros((10,), dtype=int)
LDAtopics = np.zeros((10,), dtype=int)

if new_text[1] == 0:
    MBNMFKLtopics[np.argmax(new_text_topics_mbnmfkl[0])] -= 1
    LDAtopics[np.argmax(new_text_topics_lda[0])] -= 1
elif new_text[1] == 1:
    MBNMFKLtopics[np.argmax(new_text_topics_mbnmfkl[0])] += 1
    LDAtopics[np.argmax(new_text_topics_lda[0])] += 1

print(MBNMFKLtopics)
print(LDAtopics)