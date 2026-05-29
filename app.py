from flask import Flask, render_template, request
from groq_client import generate_mongo_query
from mongo_client import execute_query

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():

    if request.method == "POST":

        user_input = request.form["query"]

        generated_query = generate_mongo_query(user_input)

        results = execute_query(generated_query)

        return render_template(
            "results.html",
            user_input=user_input,
            generated_query=generated_query,
            results=results
        )

    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True)