from flask import Flask, render_template, request, redirect, url_for
from Master import Master
import json

app = Flask(__name__)


@app.route("/", methods=['GET', 'POST'])
def home():
    discipline = None
    rho = None
    if request.method == 'POST':
        if request.form['discipline'] == 'fcfs':
            discipline = 1
        elif request.form['discipline'] == 'lcfs':
            discipline = 2
        if request.form['util'] == 'util2':
            rho = 0.2
        elif request.form['util'] == 'util4':
            rho = 0.4
        elif request.form['util'] == 'util6':
            rho = 0.6
        elif request.form['util'] == 'util8':
            rho = 0.8
        elif request.form['util'] == 'util9':
            rho = 0.9
        return redirect(url_for('simul', discipline=discipline, rho=rho))

    elif request.method == 'GET':
        return render_template("home.html")


@app.route("/simul/disc<int:discipline>util<float:rho>")
def simul(discipline, rho):
    master = Master()
    results_w, results_w_vars, results_nq, results_nq_vars = master.webmain(discipline, rho)
    discipline = "FCFS" if discipline == 1 else "LCFS"
    return render_template("simulation.html", discipline=discipline, rho=rho, results_w=json.dumps(results_w),
                           results_w_vars=json.dumps(results_w_vars), results_nq=json.dumps(results_nq),
                           results_nq_vars=json.dumps(results_nq_vars))


if __name__ == "__main__":
    app.run(debug=True)
