from flask import Flask, render_template, request, redirect, url_for
from Master import Master
import json

app = Flask(__name__)


@app.route("/", methods=['GET', 'POST'])
def home():
    discipline = None
    rho = None
    k = 1_280
    seed = "-1"
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

        if(request.form['k'] is not ''):
          try:
            k = int(request.form['k'])
          except:
            pass
        if(request.form['seed'] is not ''):          
          try:
            seed = int(request.form['seed'])
          except:
            pass
        return redirect(url_for('simul', discipline=discipline, rho=rho, k=k, seed=seed))

    elif request.method == 'GET':
        return render_template("home.html")


@app.route("/simul/d<int:discipline>u<float:rho>k<int:k>s<string:seed>")
def simul(discipline, rho, k, seed):
    if seed == "-1":
      seed = None
    master = Master()
    results_w, results_w_icl, results_w_icu, \
        results_w_vars, results_w_vars_icl, results_w_vars_icu, \
        results_nq, results_nq_icl, results_nq_icu, \
        results_nq_vars, results_nq_vars_icl, results_nq_vars_icu, \
        execution_time = master.webmain(discipline, rho, k, seed)
    execution_time = "Execution time: {0:.2f} seconds".format(execution_time)
    discipline = "FCFS" if discipline == 1 else "LCFS"
    return render_template("simulation.html", discipline=discipline, rho=rho,
                           results_w=json.dumps(results_w),
                           results_w_icl=json.dumps(results_w_icl),
                           results_w_icu=json.dumps(results_w_icu),
                           results_w_vars=json.dumps(results_w_vars),
                           results_w_vars_icl=json.dumps(results_w_vars_icl),
                           results_w_vars_icu=json.dumps(results_w_vars_icu),
                           results_nq=json.dumps(results_nq),
                           results_nq_icl=json.dumps(results_nq_icl),
                           results_nq_icu=json.dumps(results_nq_icu),
                           results_nq_vars=json.dumps(results_nq_vars),
                           results_nq_vars_icl=json.dumps(results_nq_vars_icl),
                           results_nq_vars_icu=json.dumps(results_nq_vars_icu),
                           execution_time=execution_time)


if __name__ == "__main__":
    app.run(debug=True)
