from flask import Flask, render_template, jsonify
from modules import tor_proxy_manager

app = Flask(__name__)

@app.route('/')
def dashboard():
    return render_template('dashboard.html')

@app.route('/start-attack/<module>')
def start_attack(module):
    # Execute module via subprocess
    return jsonify({"status": "started", "module": module})

@app.route('/tor/restart')
def restart_tor():
    tor_proxy_manager.restart()
    return jsonify({"status": "restarted"})
