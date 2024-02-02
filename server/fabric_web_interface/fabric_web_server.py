from flask import Flask, render_template, request, redirect, url_for, flash, session
import requests
import json
from flask import send_from_directory
import os

##################################################
##################################################
#
# ⚠️ CAUTION: This is an HTTP-only server!
#
# If you don't know what you're doing, don't run
#
##################################################
##################################################


def send_request(prompt, endpoint, pattern):
    base_url = "http://127.0.0.1:3000"
    url = f"{base_url}{endpoint}"
    headers = {
        "Content-Type": "application/json",
        "Authorization": "eJ4f1e0b-25wO-47f9-97ec-6b5335b2",
    }
    data = json.dumps({"input": prompt, "pattern": pattern})
    response = requests.post(url, headers=headers, data=data, verify=False)

    try:
        return response.json()["response"]
    except KeyError:
        return f"Error: You're not authorized for this application."


app = Flask(__name__)
app.secret_key = "mainoo"


@app.route("/favicon.ico")
def favicon():
    return send_from_directory(
        os.path.join(app.root_path, "static"),
        "favicon.ico",
        mimetype="image/vnd.microsoft.icon",
    )


@app.route("/", methods=["GET", "POST"])
def index():
    patterns = os.listdir('../../patterns/')  # Get the list of directories in 'patterns'
    if request.method == "POST":
        prompt = request.form.get("prompt")
        endpoint = request.form.get("api")
        pattern = request.form.get("pattern")
        response = send_request(prompt=prompt, endpoint=endpoint, pattern=pattern)
        return render_template("index.html", response=response, patterns=patterns)
    return render_template("index.html", response=None, patterns=patterns)


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8000, debug=True)
