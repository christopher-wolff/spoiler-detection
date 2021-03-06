"""Data cleaning for movie text data.

The overall data cleaning process invloves removing punctuation, making
everything lower case, and tokenizing the text from titles and the actual
reviews themselves. num_helpful_yes gets rid of commas and numbers and replace
with empty character. This is because the numerical values sometimes have commas
in them. It also converts dates from the movies into standardized date syntax —
ISO 8601. An example of this would be changing 24 July 2008 into 2008-07-24.
Cleaner word tokenizes the entire text with NLTK and then filters out all of the
tokens that are alphabetic. We then convert everything to lowercase and then
join all of the tokens together to one string separated by spaces.

"""


__version__ = '0.1'
__date__ = '3/19/2018'


import csv
import json
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

from helper import export_to_csv
from helper import export_to_json


def clean_reviews_temp(reviews, debug=False):
    """Clean the provided list of reviews.

    Mutates the list passed as a parameter.

    """
    for k, review in enumerate(reviews):
        # get rid of commas in numeric values
        review['num_helpful_yes'] = review['num_helpful_yes'].replace(',', '')
        review['num_helpful_total'] = review['num_helpful_total'].replace(',', '')
        # tokenize title and remove punctuation
        title_tokens = word_tokenize(review['title'])
        title_words = [word.lower() for word in title_tokens if word.isalpha()]
        review['title'] = ' '.join(title_words)
        # tokenize text and remove stopwords
        # text_tokens = word_tokenize(review['text'])
        # text_words = [word.lower() for word in text_tokens if word.isalpha()]
        # review['text'] = ' '.join(text_words)
        # standardize date
        month_to_num = {'January': '01', 'February': '02', 'March': '03',
                        'April': '04', 'May': '05', 'June': '06', 'July': '07',
                        'August': '08', 'September': '09', 'October': '10',
                        'November': '11', 'December': '12'}
        (day, month, year) = review['date'].split(' ')
        if len(day) == 1:
            day = '0' + day
        month = month_to_num[month]
        review['date'] = year + '-' + month + '-' + day
        review['review_id'] = k

        if debug and (k + 1) % 100 == 0:
            print('Finished cleaning %d reviews' % (k + 1))


def clean_reviews(reviews, debug=False):
    """Clean the provided list of reviews.

    Mutates the list passed as a parameter.

    """
    for k, review in enumerate(reviews):
        # tokenize title and remove punctuation
        title_tokens = word_tokenize(review['title'])
        title_words = [word.lower() for word in title_tokens if word.isalpha()]
        review['title'] = ' '.join(title_words)
        # tokenize text and remove stopwords
        text_tokens = word_tokenize(review['text'])
        text_words = [word.lower() for word in text_tokens if word.isalpha()]
        review['text'] = ' '.join(text_words)

        if debug and (k + 1) % 100 == 0:
            print('Finished cleaning %d reviews' % (k + 1))


def remove_stopwords(reviews, debug=False):
    """Remove stopwords from reviews."""
    stop_words = set(stopwords.words('english'))
    for k, review in enumerate(reviews):
        text = review['text']
        rev = [word for word in text.split(' ') if word not in stop_words]
        review['text'] = ' '.join(rev)
        if debug and (k + 1) % 100 == 0:
            print('Finished cleaning %d reviews' % (k + 1))

def clean_movies(movies, debug=False):
    """Clean movies."""
    for k, movie in enumerate(movies):
        movie['genres'] = movie['genres'].split(' $$$ ')
        movie['keyWords'] = movie['keyWords'].split(' $$$ ')


if __name__ == '__main__':
    with open('data/movies_raw.csv', 'r') as input_file:
       reader = csv.DictReader(input_file)
       header = reader.fieldnames
       movies = list(reader)
       clean_movies(movies, debug=True)
       export_to_json(movies, 'data/movies_clean.json')
