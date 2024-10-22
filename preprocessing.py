import re
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
from nltk import word_tokenize
from nltk.corpus import stopwords
import pickle
import pandas as pd

import nltk
nltk.download('punkt')
nltk.download('stopwords')

def remove_emojis(text):
    emoji_pattern = re.compile(
        "["
        "\U0001F600-\U0001F64F"
        "\U0001F300-\U0001F5FF"
        "\U0001F680-\U0001F6FF"
        "\U0001F700-\U0001F77F"
        "\U0001F780-\U0001F7FF"
        "\U0001F800-\U0001F8FF"
        "\U0001F900-\U0001F9FF"
        "\U0001F1E0-\U0001F1FF"
        "\u2600-\u26FF"
        "\u2700-\u27BF"
        "]+"
    )
    return emoji_pattern.sub(r'', text)

def remove_numbers(text):

    return re.sub(r'\d+', '', text)


def preprocessing(comments) :

   factory = StemmerFactory()
   stemmer = factory.create_stemmer()

   comments = re.sub(r'@\w+', '', comments)

   comment = remove_emojis(text = comments)
   no_number = remove_numbers(comment)

   tokens = word_tokenize(no_number)

   lower = [token.lower() for token in tokens]



   stop_words = set(stopwords.words('indonesian'))

   stopword = [word for word in lower if word not in stop_words]

   stemm = [stemmer.stem(word) for word in stopword]

   return " ".join(stemm)


def vectorize_data(data):


    with open(r'complaint\Countvectorizer.pkl', 'rb') as f:
        vectorizer = pickle.load(f)

    Count = vectorizer.transform(data.preprocessing)
    data_count = pd.DataFrame(data=Count.toarray(), columns=vectorizer.get_feature_names_out())
    return data_count

def predict_sentiment(data_before) :

    data_before["text_len"] = data_before['preprocessing'].apply(lambda x: len(x.split()))

    data_count = vectorize_data(data=data_before)

    data = pd.concat([data_count , data_before.text_len] , axis=1)

    with open(r'complaint\LogisticRegression_final_model.pkl', 'rb') as f:
        model = pickle.load(f)

    pred = model.predict(data)
    
    return pred

    

def vectorize_data_cat(data):


    with open(r'Category\Countvectorizer_cat.pkl', 'rb') as f:
        vectorizer = pickle.load(f)

    Count = vectorizer.transform(data.preprocessing)
    data_count = pd.DataFrame(data=Count.toarray(), columns=vectorizer.get_feature_names_out())
    return data_count

def predict_sentiment_cat(data_before) :

    data = vectorize_data_cat(data=data_before)


    with open(r'Category\PassiveAggClassifier.pkl', 'rb') as f:
        model = pickle.load(f)

    pred = model.predict(data)
    
    return pred


def mapping_cat(data) : 
    dict_cat = {0 : "app" , 1 : "Service" , 2 : "Credit" , 3 : "Non-Category"}

    data['Category'] = data["Category"].map(dict_cat)

    
def mapping_sentimen(data) : 
    dict_cat = {0 : "Positive" , 1 : "Negative"}

    data['Sentiment'] = data["Sentiment"].map(dict_cat)

    