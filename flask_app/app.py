from flask import Flask, render_template, request, url_for , jsonify, redirect
import pandas as pd
from model.recomender import recomend


app = Flask(__name__)

model_input = ""
TFIDF_ENCODING_PATH = './data/models/tfidf_encodings.pkl'
TFIDF_MODEL_PATH = './data/models/tfidf.pkl'
RECIPES_PATH = './data/kaggle/RAW_recipes.csv'
PARSED_PATH = './data/kaggle/df_parsed.csv'
N = 100

@app.before_request
def before_request_func():
    print("before_request is running!")

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
            model_input = model_input + grocery_arr[i]
        else: 
            model_input = model_input + grocery_arr[i] + ","
    model_input = model_input + "]"
    return redirect((url_for('result')))

@app.route('/result', methods=['GET'])
def result():
    recipe = recomend(RECIPES_PATH, TFIDF_MODEL_PATH, TFIDF_ENCODING_PATH, model_input , N)
    # write the recipe in a file so that we dont need to load it again in the filtering
    return (recipe.to_json)

