from flask import Flask, render_template
import markdown
import bleach

app = Flask(__name__)

def md_to_html(md_string):
    # MarkdownをHTMLに変換する関数
    raw_html = markdown.markdown(md_string)
    safe_html = bleach.clean(
        raw_html,
        tags={"h1", "h2", "p", "ul", "li", "table"},
    )
    return safe_html

@app.route("/")
def index():
    with open("markdowns/sample.md", "r") as f:
        md_text = f.read()
    html_text = md_to_html(md_text)
    return render_template("index.html", markdown=html_text)

if __name__ == "__main__":
    app.run(debug=True)
