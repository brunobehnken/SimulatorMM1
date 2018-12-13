from flask import Flask, render_template, request, redirect, url_for
from Master import Master
import json

from Simulator import SimulatorLCFS, SimulatorFCFS

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
    if discipline == 1:
        sim_fcfs = SimulatorFCFS(rho)
        means, variance = sim_fcfs.transient_phase()
        return render_template("simulation.html", discipline="FCFS", rho=rho,
                               variance=json.dumps(variance), means=json.dumps(means))
    else:
        sim_lcfs = SimulatorLCFS(rho)
        means, variance = sim_lcfs.transient_phase()
        return render_template("simulation.html", discipline="LCFS", rho=rho,
                               variance=json.dumps(variance), means=json.dumps(means))


if __name__ == "__main__":
    app.run(debug=True)
