# dictionary-api-python-flask/app.py
from flask import Flask, request, jsonify, render_template
from model.dbHandler import match_exact, match_like

app = Flask(__name__)


@app.get("/")
def index():
    """
    DEFAULT ROUTE
    This method will
    1. Provide usage instructions formatted as JSON
    """
    response = {"usage": "/dict?=<word>"}
    # Since this is a website with front-end, we don't need to send the usage instructions
    return render_template("index.html")


@app.get("/dict")
def dictionary():
    """
    DEFAULT ROUTE
    This method will
    1. Accept a word from the request
    2. Try to find an exact match, and return it if found
    3. If not found, find all approximate matches and return
    """
    words = request.args.getlist("word")
    print(f"WORDS are ==>> {words}")
    if not words:
        response = {"status":"Please provide WORD","words":words}
        return jsonify(response)

    response = {"words": []}

    for word in words:
        definitions = match_exact(word)

        if definitions:
            response["words"].append({"status":"Success", "data":f"{definitions}"})
        else:
            alike = match_like(word)

            if alike:
                response["words"].append({"status":"Partial", "data":f"{alike}"})
            else:
                return jsonify({"status":"Error","data":"No definations found!!!"})

    return render_template("results.html", response=jsonify(response))

if __name__ == "__main__":
    app.run()
