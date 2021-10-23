import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
import pickle
from sklearn.metrics.pairwise import cosine_similarity

def ogdataset(RECIPES_PATH):
     recipe_df = pd.read_csv(RECIPES_PATH) 
     return recipe_df

def dataset(recipe_df): 
     new_recipe_df = recipe_df.copy()
     new_columns = ['name' ,'id' , 'ingredients']
     new_recipe_df = new_recipe_df.drop([c for c in new_recipe_df.columns if c not in new_columns], axis='columns')
     return new_recipe_df

def extract_feature(new_recipe_df , TFIDF_MODEL_PATH, TFIDF_ENCODING_PATH):
     new_recipe_df['ingredients'] = new_recipe_df.ingredients.values.astype('U')
     # TF-IDF feature extractor
     tfidf = TfidfVectorizer()
     tfidf.fit(new_recipe_df['ingredients'])
     tfidf_recipe = tfidf.transform(new_recipe_df['ingredients'])
     # save the tfidf model and encodings
     with open(TFIDF_MODEL_PATH , "wb") as f:
          pickle.dump(tfidf, f)
     with open(TFIDF_ENCODING_PATH, "wb") as f:
          pickle.dump(tfidf_recipe, f)


def compare_input(ingredients, TFIDF_MODEL_PATH, TFIDF_ENCODING_PATH):
     with open(TFIDF_ENCODING_PATH, 'rb') as f:
          tfidf_encodings = pickle.load(f)
     with open(TFIDF_MODEL_PATH, "rb") as f:
          tfidf = pickle.load(f)

     # use our pretrained tfidf model to encode our input ingredients
     ingredients_tfidf = tfidf.transform([ingredients])
     # calculate cosine similarity between actual recipe ingreds and test ingreds 
     cos_sim = map(lambda x: cosine_similarity(ingredients_tfidf, x), tfidf_encodings)
     scores = list(cos_sim)
     return scores


def get_recommendations(recipe_df, N, scores):
    # load in recipe dataset
    # df_recipes = pd.read_csv(PARSED_PATH)
    # order the scores with and filter to get the highest N scores
    top = sorted(range(len(scores)), key=lambda i: scores[i], reverse=True)[:N]
    # create dataframe to load in recommendations
    recommendation = pd.DataFrame(columns = [])
    count = 0
    for i in top:
        recommendation.at[count, 'name'] = recipe_df['name'][i]
        recommendation.at[count, 'id'] = recipe_df['id'][i]
        recommendation.at[count, 'ingredients'] = recipe_df['ingredients'][i]
        recommendation.at[count, 'nutrition'] = recipe_df['nutrition'][i]
        recommendation.at[count, 'score'] = "{:.3f}".format(float(scores[i]))
        count += 1
    return recommendation