from flask import Flask, render_template
import markdown
import bleach

app = Flask(__name__)

def md_to_html(md_string):
    # MarkdownをHTMLに変換する関数
    raw_html = markdown.markdown(
        md_string,
        extensions=["fenced_code", "tables"]
    )

    allowed_tags = bleach.sanitizer.ALLOWED_TAGS.union({
        "h1", "h2", "h3",
        "p",
        "ul", "ol", "li",
        "pre", "code",
        "a"
    })

    allowed_attrs = {
        "*": ["class"],
        "a": ["href", "title"]
    }

    safe_html = bleach.clean(
        raw_html,
        tags=allowed_tags,
        attributes=allowed_attrs,
        strip=True
    )

    return safe_html

@app.route("/")
def index():
    with open("markdowns/sample.md", "r") as f:
        md_text = f.read()
    html_text = md_to_html(md_text)
    return render_template("index.html", markdown=html_text)

if __name__ == "__main__":
    app.run(debug=True, port=8000)
