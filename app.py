from flask import Flask, render_template
from flask import Flask, render_template
from markdown_it import MarkdownIt
from mdit_py_plugins.tasklists import tasklists_plugin
from mdit_py_plugins.footnote import footnote_plugin
from mdit_py_plugins.deflist import deflist_plugin
from mdit_py_plugins.subscript import sub_plugin
import bleach

app = Flask(__name__)

def md_to_html(md_string):
    # MarkdownをHTMLに変換する関数

    md = (
        MarkdownIt("commonmark", {
            "html": True,
            "breaks": True,
            }
        )
        .use(tasklists_plugin, enabled=True)
        .use(footnote_plugin) # 例：これは脚注付きの文章です。[1]
        .use(deflist_plugin)
        .use(sub_plugin)
        .enable('table')
        .enable("strikethrough")
    )

    raw_html = md.render(md_string)
    
    with open("outputs/raw_html.html", "w", encoding="utf-8") as f:
        f.write(raw_html)

    allowed_tags = bleach.sanitizer.ALLOWED_TAGS.union({
        "h1", "h2", "h3", "h4", "h5", "h6",
        "p", "br",
        "ul", "ol", "li",
        "strong", "em", "del", "s",
        "blockquote",
        "pre", "code",
        "table", "thead", "tbody", "tr", "th", "td",
        "a",
        "hr",
        "input",
        "label",
        "sub", "sup"
    })

    allowed_attrs = {
        "*": ["class", "id"],
        "a": ["href", "title"],
        "img": ["src", "alt"],
        "input": ["type", "checked", "disabled"],
    }

    safe_html = bleach.clean(
        raw_html,
        tags=allowed_tags,
        attributes=allowed_attrs,
        strip=True
    )

    with open("outputs/sanitized_html.html", "w", encoding="utf-8") as f:
        f.write(safe_html)

    return safe_html

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
