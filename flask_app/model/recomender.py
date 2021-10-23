from numpy import DataSource
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
import pickle
from sklearn.metrics.pairwise import cosine_similarity
# from flask_app.model.helpers import ogdataset
# from flask_app.model.helpers import compare_input, extract_feature, get_recommendations

# from flask_app.model.helpers import dataset
from helpers import ogdataset, dataset, compare_input, extract_feature, get_recommendations


def recomend(RECIPES_PATH, TFIDF_MODEL_PATH, TFIDF_ENCODING_PATH, ingredients, N):
    og_df = ogdataset(RECIPES_PATH)
    new_df = dataset(og_df)
    extract_feature(new_df,TFIDF_MODEL_PATH, TFIDF_ENCODING_PATH )
    scores = compare_input(ingredients,TFIDF_MODEL_PATH, TFIDF_ENCODING_PATH )
    recomendations = get_recommendations(og_df, N, scores)
    print(recomendations.head())
    return recomendations

if __name__ == "__main__":
    TFIDF_ENCODING_PATH = '../../data/models/tfidf_encodings.pkl'
    TFIDF_MODEL_PATH = '../../data/models/tfidf.pkl'
    RECIPES_PATH = '../../data/kaggle/RAW_recipes.csv'
    PARSED_PATH = '../../data/kaggle/df_parsed.csv'
    ingredients = '["bacon", "eggs", "bread"]'
    N = 100
    recomend(RECIPES_PATH, TFIDF_MODEL_PATH, TFIDF_ENCODING_PATH, ingredients , N)
