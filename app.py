from flask import Flask, render_template, request, redirect
from bokeh.plotting import figure, output_file, show, save
from bokeh.embed import components
import os
import requests
import simplejson as json
import pandas as pd

app = Flask(__name__)
app.vars = {}
app.priceData = None


def get_priceData(ticker, features):
    start_date = '2017-01-01'
    r=requests.get('https://www.quandl.com/api/v3/datatables/WIKI/PRICES.json',params={'api_key':'zpjKLSZPMGiXZuuhwuUx', 'ticker':ticker})
    r=requests.get(r.url+'&date.gte='+start_date)

    datatable=json.loads(r.text)['datatable']
    columns = [_['name'] for _ in datatable['columns']]
    df = pd.DataFrame(datatable['data'], columns=columns)
    df['date1']=pd.to_datetime(df['date'])
    df=df.set_index('date1')[features]
    #return df.loc[start_date:]
    return df

def plot_price():

    #output_file("templates/priceplot.html")
    p = figure(title='Quandl WIKI EOD Stock Prices - 2017', x_axis_label='date', x_axis_type='datetime', tools='pan,box_zoom,wheel_zoom,reset,save')    
    colors = ['blue','green','yellow','red']
    for i,feature in enumerate(app.vars['features']):
        p.line(app.priceData.index, app.priceData[feature], legend=app.vars['ticker']+': '+feature, line_color=colors[i])

    #save(p)
    script, div = components(p)
    return script,div 


@app.route('/index', methods=['GET','POST'])
def index():
    if request.method == 'GET':
        return render_template('index.html')
    else:
        app.vars['ticker'] = request.form['ticker']
        app.vars['features'] = request.form.getlist('features')
        app.priceData = get_priceData(app.vars['ticker'], app.vars['features'])

        script,div = plot_price()

        return render_template('priceplot.html', ticker=app.vars['ticker'], script=script, div=div)







if __name__ == '__main__':
    port = int(os.environ.get('port', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
    #app.run(host='0.0.0.0', port=port, debug=False)
