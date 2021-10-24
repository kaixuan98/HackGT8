from flask import Flask, render_template, request, url_for , jsonify, redirect , json
import pandas as pd
from model.filters import allergy
from model.filters import nutrition_range, transformed_nutrition
from model.recomender import recomend


app = Flask(__name__)

model_input = ""
TFIDF_ENCODING_PATH = './data/models/tfidf_encodings.pkl'
TFIDF_MODEL_PATH = './data/models/tfidf.pkl'
RECIPES_PATH = './data/kaggle/RAW_recipes.csv'
PARSED_PATH = './data/kaggle/df_parsed.csv'
RESULT_PATH = './data/result/recommendation.csv'
N = 100

# home: show all the interface we have, can take in input
@app.route("/")
def home():
    return render_template('homepage.html')

@app.route('/submit', methods=['POST'])
def submit():
    grocery_list = request.form.get('groceryList')
    # clean up grocery list in to an array string for our model 
    grocery_arr = grocery_list.split(',')
    model_input = "["
    for i in range(len(grocery_arr)):
        if(i == len(grocery_arr) -1):
            model_input = model_input + grocery_arr[i]+ "]"
        else: 
            model_input = model_input + grocery_arr[i] + ","
    return redirect((url_for('result', model_input=model_input)))

@app.route('/result', methods=['GET'])
def result():
    model_input = request.args["model_input"] 
    recipe = recomend(RECIPES_PATH, TFIDF_MODEL_PATH, TFIDF_ENCODING_PATH, model_input , N)
    # write the recipe in a file so that we dont need to load it again in the filtering
    recipe.to_csv(RESULT_PATH)
    json_data = (json.dumps(recipe.to_dict(orient="records")))
    loaded_r = json.loads(json_data)
    return render_template('result.html', items=loaded_r)

@app.route('/filter_nutrition', methods=['POST'])
def filter_nutrition():
    nutrition = request.form.get('nutrition')
    compare = request.form.get('comparison')
    print(nutrition)
    range_val = request.form.get('range')
    result_df = pd.read_csv(RESULT_PATH)
    new_result_df = transformed_nutrition(result_df)
    if compare == ">=":
        compare = "more than or equal to"
    else:
        compare = "less than or equal to"
    range_val = float(range_val)
    result = nutrition_range(compare,range_val, nutrition, new_result_df)
    json_data = (json.dumps(result.to_dict(orient="records")))
    loaded_r = json.loads(json_data)
    return render_template('filter.html', items=loaded_r)

@app.route('/filter_allergy', methods=['POST'])
def filter_allergy():
    allergen = request.form.get('allergy')
    result_df = pd.read_csv(RESULT_PATH)
    new_result_df = transformed_nutrition(result_df)
    result = allergy(allergen,new_result_df)
    json_data = (json.dumps(result.to_dict(orient="records")))
    loaded_r = json.loads(json_data)
    return render_template('filter.html', items=loaded_r)


