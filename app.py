from flask import Flask, redirect, url_for, request, render_template
from plotly.io import from_json as graph_read_json
from plotly.utils import PlotlyJSONEncoder
import json
from cahedv.heuristic_eval import heuristic_eval

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/showgraphfromjson', methods = ['POST', 'GET'])
def showGraphFromJson():
    if request.method == 'POST':
        userJSON = request.form['plot_json']
        error = ""
        graphJSON = ""
        try:
            fig = graph_read_json(userJSON)
            graphJSON = fig.to_json()
        except:
            error = "Please provide a valid json"
        
        return render_template('showgraph.html', graphJSON = graphJSON, error = error)
    else:
        return render_template('form.html', title="Show Graph of JSON")

@app.route('/evaluatejson', methods = ['GET', 'POST'])
def evaluatejson():
    if request.method == 'POST':
        userJSON = request.form['plot_json']
        error = ""
        vals = []
        try:
            fig = graph_read_json(userJSON)
            vals = heuristic_eval(userJSON)
            print(vals)
        except:
            error = "Please provide a valid json"
        
        return render_template('evaluatejson.html', evaluations = vals, error = error)
    else:
        return render_template('form.html', title="Evaluate JSON")

if __name__ == '__main__':
    app.run(debug = True)
