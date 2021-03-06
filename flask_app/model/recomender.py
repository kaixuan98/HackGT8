import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
import pickle
from sklearn.metrics.pairwise import cosine_similarity
from model.helpers import ogdataset
from model.helpers import compare_input, extract_feature, get_recommendations

from model.helpers import dataset
# from helpers import ogdataset, dataset, compare_input, extract_feature, get_recommendations

def recomend(RECIPES_PATH, TFIDF_MODEL_PATH, TFIDF_ENCODING_PATH, ingredients, N):
    og_df = ogdataset(RECIPES_PATH)
    print("Getting Dataset...")
    new_df = dataset(og_df)
    print("Extracting Feature...")
    extract_feature(new_df,TFIDF_MODEL_PATH, TFIDF_ENCODING_PATH )
    print("Counting Score...")
    scores = compare_input(ingredients,TFIDF_MODEL_PATH, TFIDF_ENCODING_PATH )
    print("Getting your recommendation...")
    recomendations = get_recommendations(og_df, N, scores)
    return recomendations

# if __name__ == "__main__":
#     TFIDF_ENCODING_PATH = '../data/models/tfidf_encodings.pkl'
#     TFIDF_MODEL_PATH = '../data/models/tfidf.pkl'
#     RECIPES_PATH = '../data/kaggle/RAW_recipes.csv'
#     PARSED_PATH = '../data/kaggle/df_parsed.csv'
#     ingredients = '["bacon", "eggs", "bread"]'
#     N = 100
#     result = recomend(RECIPES_PATH, TFIDF_MODEL_PATH, TFIDF_ENCODING_PATH, ingredients , N)
#     print("Done\n")
#     print(result)

