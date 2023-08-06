from flask import Flask, request
from flask_cors import CORS #, cross_origin

app = Flask(__name__)
CORS(app)
#cors = CORS(app)
#app.config['CORS_HEADERS'] = 'Content-Type'

@app.route("/")
def hello():
    return "Hello World!"

@app.route("/accounts")
def accounts():
    params = "accounts"
    result = ledger(params)
    
    return f"accounts: {result}"

@app.route("/balance")
def balance():
    params = "b --flat --no-total"
    result = ledger(params)
    
    return result

@app.route("/currentValues")
def currentValues():
    root = request.args.get('root')
    currency = request.args.get('currency')
    params = f"b ^{root} -X {currency} --flat --no-total"
    result = ledger(params)
    
    #return f"current values for {root} in {currency}: {result}"
    return result

@app.route('/about')
def about():
    ''' display some diagnostics '''
    import os
    cwd = os.getcwd()
    return f"cwd: {cwd}"

###################################

def ledger(parameters):
    ''' Execute ledger command '''
    import subprocess
    from cashiersync.config import Configuration

    cfg = Configuration()

    command = f"ledger {parameters}"
    result = subprocess.run(command, shell=True, encoding="utf-8", capture_output=True)
    # cwd=cfg.ledger_working_dir

    if result.returncode != 0:
        output = result.stderr
    else:
        output = result.stdout
    
    return output

def run_server():
    """ Available to be called from outside """
    # use_reloader=False port=23948
    app.run(host='0.0.0.0', threaded=True, use_reloader=False)
    # host='127.0.0.1' host='0.0.0.0'
    # , debug=True
    # Prod setup: 
    # debug=False


##################################################################################
if __name__ == '__main__':
    # Use debug=True to enable template reloading while the app is running.
    # debug=True <= this is now controlled in config.py.
    run_server()