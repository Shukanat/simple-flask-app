import json
import pyodbc
from flask import Flask, render_template, make_response
from utils import get_data, do_plot, graph_request, genre_by_year, get_countplot

with open('config.json', 'r') as f:
    config = json.load(f)

cnx = pyodbc.connect(
    driver='/usr/local/lib/libmsodbcsql.17.dylib',
    #driver=[item for item in pyodbc.drivers()][-1],
    server=config['connection']['server'],
    port =config['connection']['port'],
    database=config['connection']['database'],
    user=config['connection']['user'],
    password=config['connection']['password'])
        
app = Flask(__name__)
app.config['SECRET_KEY'] = config['secret-key']

@app.route('/', methods=['GET', 'POST'])
def home():
    form = graph_request()
    if form.validate_on_submit():
        year = form.year.data
        df = genre_by_year(year, cnx)
        bytes_obj1 = get_countplot(df,year)
        return render_template('genre_by_year.html', graph1 = bytes_obj1, form=form)
    
    return render_template('index.html', form=form)

@app.route('/female_proportion')
def barplot():
    df = get_data(cnx)
    bytes_obj2 = do_plot(df)
    return render_template('female_proportion.html', graph2 = bytes_obj2)

if __name__ == "__main__":
    app.run(debug = True)
