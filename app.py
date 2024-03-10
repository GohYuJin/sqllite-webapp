from flask import Flask, request, render_template, redirect
import datetime
import sqlite3
import pandas as pd
from dash import Dash, html, dcc, callback, Output, Input
import dash_bootstrap_components as dbc
import plotly.express as px

currentDateTime = datetime.datetime.now()
app = Flask(__name__)

@app.route("/",methods=["GET","POST"])
def index():
    return(render_template("index.html"))

@app.route("/main",methods=["GET","POST"])
def main():
    name = request.form.get("name")
    conn = sqlite3.connect('database1.db')
    c = conn.cursor()
    c.execute('INSERT INTO employee (name,timestamp) VALUES(?,?)',(name,currentDateTime))
    conn.commit()
    c.close()
    conn.close()
    return(render_template("main.html",name=name))

@app.route("/ethical_test",methods=["GET","POST"])
def ethical_test():   
    return(render_template("ethical_test.html"))

@app.route("/answer",methods=["GET","POST"])
def answer():
    a = request.form["options"]
    print(a)
    if a == "true":
        print("wrong answer")
    elif a=="false":
        print("right answer")
    return(render_template("end.html"))

@app.route("/query",methods=["GET","POST"])
def query():   
    conn = sqlite3.connect('database1.db')
    c = conn.execute('''select *
        from employee''')
    r=""
    for row in c:
        print(row)
        r = r + str(row)
    c.close()
    conn.close()
    return(render_template("query.html",r=r))

@app.route("/clear",methods=["GET","POST"])
def clear():   
    conn = sqlite3.connect('database1.db')
    c = conn.cursor()
    c.execute('DELETE FROM employee;',);
    conn.commit()
    c.close()
    conn.close()
    return(render_template("clear.html"))


def query_count_employees():
    conn = sqlite3.connect('database1.db')
    cursor = conn.cursor()
    table_name = 'employee'
    query = f"SELECT COUNT(*) FROM {table_name}"
    cursor.execute(query)
    employee_count = cursor.fetchone()[0]
    cursor.close()
    conn.close()
    return employee_count


@callback(Output('live-update-text', 'children'),
          Input('interval-component', 'n_intervals'))
def update_metrics(n):
    count = query_count_employees()
    return [
        dbc.Card(
            dbc.CardBody([
                 html.H2("Name Count", className="card-title", style={'textAlign': 'center'}),
                 html.H1('{0}'.format(count), className="card-text", style={'textAlign': 'center', "fontSize": "100px"}),
            ])
        ),        
    ]

@callback(
    Output("graph", "figure"), 
    Input("TimeScale", "value"))
def update_line_chart(timescale):
    conn = sqlite3.connect('database1.db')
    cursor = conn.cursor()
    table_name = 'employee'
    query = f"SELECT * FROM {table_name}"
    cursor.execute(query)
    table = cursor.fetchall()
    cursor.close()
    conn.close()

    df = pd.DataFrame(table, columns=["name", "datetime"])
    df["datetime"] = pd.to_datetime(df["datetime"])

    if timescale == 'Hour':
        df["time"] = df["datetime"].dt.round('H')
    elif timescale == 'Day':
        df["time"] = df["datetime"].dt.date
    
    counts_by_time_df = df.groupby("time").count().reset_index()
    counts_by_time_df["counts"] = counts_by_time_df["datetime"]
    fig = px.line(counts_by_time_df, x='time', y="counts", title="Counts vs time")
    return fig


dashboard = Dash(__name__, server=app, url_base_pathname="/dash/", external_stylesheets=[dbc.themes.CYBORG])
dashboard.layout = html.Div([
        html.Div([
            html.Div(id='live-update-text', style={"width": "40%"}),
            dcc.Graph(id="graph", style={'width': '50%', 'height': '30%', "margin-left": "20px"}),
            dcc.RadioItems(['Day', 'Hour'], 'Hour', id="TimeScale"),
        ], style={"display": "flex", "justify-content": "center", "align-items": "center", "width": "100%"}),
        html.Div([
            dbc.Button("Go Back", id="back", className="back", external_link=True, href="/main", style={"margin-left": "50px", "margin-right": "50px"})
        ], style={"display": "flex", "justify-content": "right", "align-items": "center", "width": "100%", "margin-top": "50px", "margin-bottom": "50px"}),
        dcc.Interval(
            id='interval-component',
            interval=5*1000, # in milliseconds
            n_intervals=0
        )
    ], style={"display": "inline-block", "justify-content": "center", "align-items": "center", "margin-top": "100px", "width": "100%"})

@app.route("/end",methods=["GET","POST"])
def end():  
    return(render_template("end.html"))

@app.route('/dashboard',methods=["GET","POST"]) 
def dashboard():
    return redirect('/dash')

if __name__ == "__main__":
    app.run()
    
