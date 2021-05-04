from flask import Flask, render_template, request
import json
from nutritionix import Nutritionix
import http.client
from urllib.parse import urlencode

nix = Nutritionix(app_id="c1955429",
                  api_key="4e8e629653b6d84fda5ad79b71b805f2")

app = Flask(__name__)

@app.route("/", methods = ['POST', 'GET'])
def index():
    if request.method == 'GET':
        return render_template("foods.html")
    if request.method == 'POST':
        food = request.form.get("foods")
        results = nix.search(food, results="0:1").json()
        value = results['hits']
        temp = value[0]
        info = nix.item(id = temp['_id']).json()
        iname = info['item_name']
        water = info['nf_water_grams']
        calories = info['nf_calories']
        calories_from_fat = info['nf_calories_from_fat']
        total_fat = info['nf_total_fat']
        # print(info)
        return render_template("infofood.html", iname=iname, water=water, calories=calories, calories_from_fat=calories_from_fat, total_fat=total_fat)

@app.route("/exercise", methods = ['POST', 'GET'])
def exercise():
    if request.method == 'GET':
        return render_template("exercise.html")
    if request.method == 'POST':
        conn = http.client.HTTPSConnection("trackapi.nutritionix.com")
        exercise = request.form.get("exercise")
        payload = urlencode({'query': exercise})
        headers = {
            'x-app-id': 'c1955429',
            'x-app-key': '4e8e629653b6d84fda5ad79b71b805f2',
            'content': 'application/json',
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        conn.request("POST", "/v2/natural/exercise", payload, headers)
        res = conn.getresponse()
        data = res.read()
        info = data.decode("utf-8")
        info = json.loads(info)
        temp = info["exercises"]
        temp2 = temp[0]
        calories = temp2['nf_calories']
        inp = temp2['user_input']
        image = temp2['photo']['highres']
        return render_template("info.html", calories = calories, inp = inp, image = image)