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

@app.route("/dashboard",methods=["GET","POST"])
def dashbaord():   
    return(render_template("dashboard.html"))

@app.route("/end",methods=["GET","POST"])
def end():  
    return(render_template("end.html"))

if __name__ == "__main__":
    app.run()
