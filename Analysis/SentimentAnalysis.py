#IMPORTS
import numpy as np
import pandas as pd
import tensorflow as tf
import re
import string

from tensorflow.keras import layers
from tensorflow.keras import losses

from tensorflow.keras.layers import TextVectorization
from tensorflow.keras.layers import StringLookup

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder





#DATA CLEANING
comments = pd.read_csv('C:/Users/aidan/OneDrive/Documents/GitHub/PIC16BProject/steam_scraper/reviews.csv')

comments['comment'] = comments['comment'].apply(lambda x: x[x.find('\n')+1:] if '\n' in x else x) # remove the date from the comment
comments['comment'] = comments['comment'].apply(lambda x: x.replace('\n', ' ') if '\n' in x else x) # replace newlines with spaces so words aren't considered as word + \n
comments = comments.drop(["game","hours_players"], axis=1)


le = LabelEncoder()
comments["is_Recommended"] = le.fit_transform(comments["is_Recommended"])

data = tf.data.Dataset.from_tensor_slices((comments["comment"], comments["is_Recommended"]))

data = data.shuffle(buffer_size = len(data))

train_size = int(0.7*len(data))
val_size   = int(0.1*len(data))

train = data.take(train_size)
val   = data.skip(train_size).take(val_size)
test  = data.skip(train_size + val_size)

#ADD FUNCTIONALITY TO REMOVE STOP WORDS HERE?
def standardization(input_data):
    lowercase = tf.strings.lower(input_data)
    no_punctuation = tf.strings.regex_replace(lowercase,
                                  '[%s]' % re.escape(string.punctuation),'')
    return no_punctuation






#MODEL CONSTRUCTION
# only the top distinct words will be tracked
max_tokens = 2000

# each headline will be a vector of length 50
sequence_length = 50

vectorize_layer = TextVectorization(
    standardize=standardization,
    max_tokens=max_tokens, # only consider this many words
    output_mode='int',
    output_sequence_length=sequence_length)

comments = train.map(lambda x, y: x)
vectorize_layer.adapt(comments)

def vectorize_comment(text, label):
    text = tf.expand_dims(text, -1)
    return vectorize_layer(text), [label]

train_vec = train.map(vectorize_comment)
val_vec   = val.map(vectorize_comment)
test_vec  = test.map(vectorize_comment)

model = tf.keras.Sequential([
  layers.Embedding(max_tokens, output_dim = 3, name="embedding"),
  layers.Dropout(0.2),
  layers.GlobalAveragePooling1D(),
  layers.Dropout(0.2),
  layers.Dense(64),
  layers.Dense(2)]
)

model.compile(loss=losses.SparseCategoricalCrossentropy(from_logits=True),
              optimizer='adam',
              metrics=['accuracy'])

model.fit(train_vec, epochs = 20, validation_data = val_vec)

model.evaluate(test_vec)