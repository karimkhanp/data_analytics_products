import plotly
import plotly.graph_objs as go
import json
import pandas as pd
import numpy as np

dd = pd.read_csv("submission.csv", index_col=False)

def template():
    templateDate = {
        'categories' : getCategory(),
        'deptids' : getDeptid(),
        'states' : getState(),
        'storeids' : getStoreid(),
        'selected_tvalue' : -1
    }
    return templateDate

def getDeptid():
    return (1, 2, 3)

def getStoreid():
    return (1, 2, 3) 

def getState():
    return ('CA', 'TX', 'WI')

def getCategory():
    return ('HOBBIES', 'HOUSEHOLD', 'FOODS')


def plot(category, deptid, item, state, storeid):

    idx = category +'_'+ deptid +'_'+ item +'_'+ state +'_'+ storeid + '_validation'
    ww = dd.loc[dd['id'] == idx]
    e = pd.DataFrame(ww.T.values)

    fig = go.Figure(go.Scatter(
        x = np.arange(1, 29, 1.0),
        y = e[1:].values.T[0]
    ))

    fig.update_layout(
        xaxis = dict(tick0 = 1, dtick = 1.0),
        yaxis = dict(tick0 = 0.8, dtick = 0.02),
        plot_bgcolor="white",
        width=1000,
        height=700,
        title="Prediction for item id " + str(item) + " from "+str(category)+ "(" + str(deptid) + ") " + ", State " +str(state)+ " with Store id " + str(storeid) ,
        xaxis_title="Days",
        yaxis_title="Sales",
        margin=dict(
            l=50,
            r=50,
            b=100,
            t=100,
            pad=4
            )
    )

    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return graphJSON
