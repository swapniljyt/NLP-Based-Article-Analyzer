#LIBRARIES
import urllib
import pandas as pd
import requests
from bs4 import BeautifulSoup
from IPython.display import display
import os
import re
import nltk
from nltk.tokenize import sent_tokenize, word_tokenize
import syllables
from nltk.corpus import stopwords
import string

def get_article_text(url):
    res = requests.get(url)
    if res.status_code == 200:
        html_page = res.content
        soup = BeautifulSoup(html_page, features='html.parser')
        article_element = soup.find("article")
        if article_element:
            article_text = ' '.join(article_element.stripped_strings)
            return article_text
        else:
            print("Article element not found.")
            return None
    else:
        print(f"Failed to retrieve the page. Status code: {res.status_code}")
        return None

def url_to_dataframe(url):
    article_text = get_article_text(url)
    if article_text:
        df = pd.DataFrame(data={'Article': [article_text]})
        return df
    else:
        return pd.DataFrame()

#Sentimental Analysis

nltk.download('punkt')
stopwords_directory = '/root/src/NLP-Based-Article-Analyzer/StopWords'
master_dictionary_directory = '/root/src/NLP-Based-Article-Analyzer/MasterDictionary'
def read_stopwords_from_directory(directory):
    stopword_strings = []
    encodings = ['utf-8', 'latin-1', 'cp1252']  # List of possible encodings
    for filename in os.listdir(directory):
        filepath = os.path.join(directory, filename)
        for encoding in encodings:
            try:
                with open(filepath, 'r', encoding=encoding) as file:
                    stopword_strings.append(file.read())
                break  
            except UnicodeDecodeError:
                continue  # Try the next encoding
    return stopword_strings
stopword_strings = read_stopwords_from_directory(stopwords_directory)
def calculate_sentiment_scores(dataframe):
    link_pattern = re.compile(r'https?://[^\s]+|www\.[^\s]+')
    final_stopword_list = []
    for stopword_string in stopword_strings:
        stopword_string_lower = stopword_string.lower()
        stopwords_from_string = stopword_string_lower.split()
        filtered_words = [word for word in stopwords_from_string if not link_pattern.match(word) and not re.match(r'\W+', word)]
        final_stopword_list.extend(filtered_words)
    final_stopword_list = list(set(final_stopword_list))
    def remove_stopwords(text):
        words = text.split()
        filtered_words = [word for word in words if word.lower() not in final_stopword_list]
        return ' '.join(filtered_words)
    dataframe['Cleaned_Article'] = dataframe['Article'].apply(lambda x: remove_stopwords(x))
    with open(os.path.join(master_dictionary_directory, 'positive-words.txt'), 'r', encoding='utf-8') as file:
        positive_word_list = re.findall(r'\b\w+\b', file.read())
    
    with open(os.path.join(master_dictionary_directory, 'negative-words.txt'), 'r', encoding='latin-1') as file:
        negative_word_list = re.findall(r'\b\w+\b', file.read())
    df_words = word_tokenize(dataframe['Cleaned_Article'].iloc[0])
    found_positive_word_list = [word for word in df_words if word in positive_word_list]
    found_negative_word_list = [word for word in df_words if word in negative_word_list]
    positive_score = sum(1 for word in df_words if word in found_positive_word_list)
    negative_score = sum(-1 for word in df_words if word in found_negative_word_list) * -1
    polarity_score = (positive_score - negative_score) / ((positive_score + negative_score) + 0.000001)
    subjectivity_score = (positive_score + negative_score) / (len(df_words) + 0.000001)

    return {
        'Positive Score': positive_score,
        'Negative Score': negative_score,
        'Polarity Score': polarity_score,
        'Subjectivity Score': subjectivity_score
    } 

#Analysis of Readability
def calculate_sentence_complexity_metrics(dataframe):
    cleaned_articles = dataframe['Article'].apply(str) 
    sentences = cleaned_articles.apply(sent_tokenize)
    words = cleaned_articles.apply(word_tokenize)
    average_sentence_length = words.apply(len) / sentences.apply(len)

    complex_words = words.apply(lambda w: [word for word in w if len(word) > 6]) 
    percentage_complex_words = complex_words.apply(len) / words.apply(len)
    fog_index = 0.4 * (average_sentence_length + percentage_complex_words)

    return {
        'Average Sentence Length': average_sentence_length.mean(),
        'Percentage of Complex Words': percentage_complex_words.mean(),
        'Fog Index': fog_index.mean()
    }


#Average Number of Words Per Sentence

def calculate_average_words_per_sentence(dataframe):
    sentences = [sent_tokenize(text) for text in dataframe['Article']]
    words = [word_tokenize(text) for text in dataframe['Article']]

    average_words_per_sentence = len(words[0]) /len(sentences[0])
    return average_words_per_sentence
          

#Complex Word Count

def calculate_complex_word_count(dataframe):

    words = [word_tokenize(text) for text in dataframe['Article']]

    flattened_words = [word for sublist in words for word in sublist]

    complex_words_count = sum(1 for word in flattened_words if syllables.estimate(word) > 2)

    return complex_words_count

# Word Count

nltk.download('stopwords')

def calculate_total_cleaned_words(dataframe):
    words = [word_tokenize(text) for text in dataframe['Article']]
    flattened_words = [word for sublist in words for word in sublist]
    stop_words = set(stopwords.words('english'))
    filtered_words = [word.lower() for word in flattened_words if word.lower() not in stop_words and word.lower() not in string.punctuation]
    filtered_words = [''.join(char for char in word if char.isalnum()) for word in filtered_words if any(char.isalnum() for char in word)]
    total_cleaned_words = len(filtered_words)

    return total_cleaned_words



#Syllable Count Per Word
nltk.download('punkt')
def count_syllables(word):
    vowels = "aeiouy"
    count = 0
    prev_char = ''
    for char in word:
        char_lower = char.lower()
        if char_lower in vowels and prev_char not in vowels:
            count += 1
        prev_char = char_lower
    if word.endswith(("es", "ed")) and count > 1:
        count -= 1  
    return max(count, 1)  

def calculate_syllable_counts(dataframe):
    words = [word_tokenize(text) for text in dataframe['Article']]
    flattened_words = [word for sublist in words for word in sublist]

    syllables_per_word = [count_syllables(word) for word in flattened_words]

    total_syllables = sum(syllables_per_word)
    average_syllables_per_word = total_syllables / len(flattened_words)


    return syllables_per_word, total_syllables, average_syllables_per_word



#Personal Pronouns
def count_personal_pronouns(dataframe):

    personal_pronouns_pattern = re.compile(r'\b(?:I|we|my|ours|us)\b', flags=re.IGNORECASE)

    personal_pronouns_matches = personal_pronouns_pattern.findall(dataframe['Article'].iloc[0])
    personal_pronouns_count = len(personal_pronouns_matches)

    return personal_pronouns_count


#Average Word Length
nltk.download('punkt')

def calculate_average_word_length(dataframe):
    words = [word_tokenize(text) for text in dataframe['Article']]
    flattened_words = [word for sublist in words for word in sublist]
    total_characters = sum(len(word) for word in flattened_words)
    total_words = len(flattened_words)
    average_word_length = total_characters / total_words if total_words > 0 else 0

    return average_word_length



