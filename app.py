from flask import Flask, request, render_template
import datetime
import sqlite3

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

#@app.route("/dashboard",methods=["GET","POST"])
#def dashboard():   
#    return(render_template("dashboard.html"))

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
            ]), style={"width": "30rem"}
        ),        
        html.Br(),
        dbc.Button(
            "Go Back", id="back", className="back", external_link=True, href="/main",
        ),
    ]


dashboard = Dash(__name__, server=app, url_base_pathname="/dash/", external_stylesheets=[dbc.themes.CYBORG])
dashboard.layout = html.Div([
        html.Div(id='live-update-text'),
        dcc.Interval(
            id='interval-component',
            interval=5*1000, # in milliseconds
            n_intervals=0
        )
    ], style={"display":"flex", "justify-content": "center", "align-items": "center", "margin-top": "100px"})

@app.route("/end",methods=["GET","POST"])
def end():  
    return(render_template("end.html"))

if __name__ == "__main__":
    app.run()
