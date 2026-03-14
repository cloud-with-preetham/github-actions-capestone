from flask import Flask, jsonify, render_template
import os
import platform
import socket
import datetime
import psutil
import time
import requests

app = Flask(__name__)

start_time = time.time()
request_count = 0


@app.before_request
def count_requests():
    global request_count
    request_count += 1


@app.route("/")
def dashboard():
    return render_template("index.html")


@app.route("/health")
def health():
    return jsonify(status="healthy")


@app.route("/pipeline")
def pipeline():

    repo = "cloud-with-preetham/github-actions-capestone"

    url = f"https://api.github.com/repos/{repo}/actions/runs"

    r = requests.get(url)

    data = r.json()

    latest = data["workflow_runs"][0]

    return {
        "status": latest["status"],
        "conclusion": latest["conclusion"],
        "run_number": latest["run_number"],
        "branch": latest["head_branch"],
    }


@app.route("/metrics")
def metrics():

    uptime = int(time.time() - start_time)

    return jsonify(
        {
            "hostname": socket.gethostname(),
            "platform": platform.system(),
            "python": platform.python_version(),
            "time": datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S"),
            "service": "github-actions-capestone",
            "environment": os.getenv("ENVIRONMENT", "production"),
            "commit": os.getenv("BUILD_COMMIT", "unknown"),
            "build": os.getenv("BUILD_NUMBER", "unknown"),
            "image": os.getenv("IMAGE_TAG", "latest"),
            "cpu": psutil.cpu_percent(),
            "memory": psutil.virtual_memory().percent,
            "uptime": uptime,
            "requests": request_count,
        }
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
