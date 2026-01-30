from flask import Flask, render_template
from flask import Flask, render_template

from utils import md_to_html

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/note")
def note():
    with open("markdowns/sample.md", "r") as f:
        md_text = f.read()
    html_text = md_to_html(md_text)
    return render_template("note.html", markdown=html_text)

if __name__ == "__main__":
    app.run(debug=True, port=8000)
