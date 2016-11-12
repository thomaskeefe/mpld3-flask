from flask import Flask, render_template
from flask_wtf import FlaskForm
from wtforms import RadioField

import numpy as np

import matplotlib
import json
import random

matplotlib.use('Agg')
import matplotlib.pyplot as plt
plt.ioff()

from threading import Lock
lock = Lock()
import datetime
import mpld3
from mpld3 import plugins

# Setting up matplotlib sytles using BMH
s = json.load(open("./static/bmh_matplotlibrc.json"))
matplotlib.rcParams.update(s)

x = range(100)
y = [a * 2 + random.randint(-20, 20) for a in x]

pie_fracs = [20, 30, 40, 10]
pie_labels = ["A", "B", "C", "D"]


def draw_fig(fig_type):
    """Returns html equivalent of matplotlib figure

    Parameters
    ----------
    fig_type: string, type of figure
            one of following:
                    * line
                    * bar

    Returns
    --------
    d3 representation of figure
    """

    with lock:
        fig, ax = plt.subplots()
        if fig_type == "line":
            ax.plot(x, y)
        elif fig_type == "bar":
            ax.bar(x, y)
        elif fig_type == "pie":
            ax.pie(pie_fracs, labels=pie_labels)
        elif fig_type == "scatter":
            ax.scatter(x, y)
        elif fig_type == "hist":
            ax.hist(y, 10, normed=1)
        elif fig_type == "area":
            ax.plot(x, y)
            ax.fill_between(x, 0, y, alpha=0.2)


    return mpld3.fig_to_html(fig)

app = Flask(__name__)
app.secret_key = "foo"

class ChartTypeForm(FlaskForm):
    choices = [('line', 'Line'), ('bar', 'Bar'), ('pie', 'Pie'), ('scatter', 'Scatter'), ('hist', 'Histogram'), ('area', 'Area')]
    chart_type = RadioField('Chart Type', choices=choices)

@app.route('/', methods=["GET", "POST"])
def home():
    form = ChartTypeForm()

    if form.is_submitted():
        chart_choice = form.chart_type.data
        plot_html = draw_fig(chart_choice)
        return render_template('index.html', form=form, plot=plot_html)

    return render_template('index.html', form=form)




if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
