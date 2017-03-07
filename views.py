from flask import render_template, request
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
    print(request.form["url"])
    data1 = pop_bias(request.form['url'])
    print(data1)
    data = tester(request.form["url"])
    return render_template("bias_buster_results.html", data = data)