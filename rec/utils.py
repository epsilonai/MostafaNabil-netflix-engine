import pandas as pd
import numpy as np
import random
from rake_nltk import Rake
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import CountVectorizer

data = pd.read_csv("netflix_titles.csv")

data=data[['title','director','cast','listed_in','description']]
data.dropna(inplace=True)


data['Key_words'] = ""

for index, row in data.iterrows():
    description = row['description']
    
    r = Rake()

    r.extract_keywords_from_text(description)

    key_words_dict_scores = r.get_word_degrees()
    
    row['Key_words'] = list(key_words_dict_scores.keys())

data.drop(columns = ['description'], inplace = True)



data['listed_in'] = data['listed_in'].map(lambda x: x.lower().split(','))

data['cast']=data['cast'].map(lambda x : x.lower().split(','))

data['director'] = data['director'].map(lambda x: x.split(' '))


for index, row in data.iterrows():
    row['director'] = ''.join(row['director']).lower()
data.set_index('title', inplace = True)


data['bag_of_words'] = ''
columns = data.columns
for index, row in data.iterrows():
    words = ''
    for col in columns:
        if col != 'director':
            words = words + ' '.join(row[col])+ ' '
        else:
            words = words + row[col]+ ' '
    row['bag_of_words'] = words
    
data.drop(columns = [col for col in data.columns if col!= 'bag_of_words'], inplace = True)


count = CountVectorizer()
count_matrix = count.fit_transform(data['bag_of_words'])

indices = pd.Series(data.index)
cosine_sim = cosine_similarity(count_matrix, count_matrix)


def recommendations(Title, cosine_sim = cosine_sim):
    recommended_movies = []
    
    idx = indices[indices == Title].index[0]

    score_series = pd.Series(cosine_sim[idx]).sort_values(ascending = False)

    top_10_indexes = list(score_series.iloc[1:11].index)
    
    for i in top_10_indexes:
        recommended_movies.append(list(data.index)[i])
        
    return recommended_movies

def generate():
    x = list(data.index)
    value = random.choices( x , k= 5)
    return (value)