from flask import Flask, render_template, request, url_for , jsonify
from model.recomendation import recommend

app = Flask(__name__)

model_input = ""

# home: show all the interface we have, can take in input
@app.route("/")
def home():
    return render_template('homepage.html')

@app.route('/submit', methods=['POST' , 'GET'])
def submit():
    if request.method == "POST":
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
        return "Your List:" + model_input
    else: 
        recipe = recommend(model_input)
        
        # We need to turn output into JSON. 
        response = {}
        count = 0    
        for index, row in recipe.iterrows():
            response[count] = {
                                'recipe': str(row['recipe']),
                                'score': str(row['score']),
                                'ingredients': str(row['ingredients']),
                                'url': str(row['url'])
                            }
            count += 1
        return jsonify(response)

