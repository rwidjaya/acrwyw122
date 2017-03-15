from flask import render_template, request, jsonify
from bias_buster_flask import app
from form import UrlForm
from test import tester
from bias_buster import pop_bias

@app.route("/bias_buster")
@app.route('/')
def homepage():
    print('routed correctly')
    form = UrlForm()
    return render_template('bias_buster_home.html',
                           title="Bias Buster",
                           form=form)



@app.route("/bias_busted", methods=["POST"])
def results():
    #print(request.form["url"])
    try:
        data, bias = pop_bias(request.form['url'])
        #print(data)
    except AssertionError:
        data = {'none': ['The news source is not in our database; please enter another article from different news source.']} 
    #data = {'source name': ['center', 'http://thisisafakelink.com', 'title?']}
    # data = tester(request.form["url"])
    return render_template("bias_buster_results.html", data = data)


#create a request routing for the extension to access JSON - NOT FOR GRADING
@app.route('/bias_busted_dataonly', methods = ["POST"])
def biasbust():
    url = request.form["url"]  
    try:
        data, bias = pop_bias(url)
        #print(data)
    except AssertionError:
        data = {'none': ['This site is not in our news source/article database; please click on the pop-up from an article page or another article page from different news source.']} 
    return jsonify(data)
