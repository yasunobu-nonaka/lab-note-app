from flask import Flask, render_template
import markdown
import bleach

app = Flask(__name__)

def md_to_html(md_string):
    # MarkdownをHTMLに変換する関数
    raw_html = markdown.markdown(
        md_string,
        extensions=[
        "extra",        # 基本拡張セット（重要）
        "fenced_code",  # ``` コードブロック
        "tables",       # テーブル
        "toc",          # 目次
        "footnotes",    # 脚注
        "attr_list",    # 属性指定
        "def_list",     # 定義リスト
        ]
    )

    allowed_tags = bleach.sanitizer.ALLOWED_TAGS.union({
        "h1", "h2", "h3", "h4", "h5", "h6",
        "p", "br",
        "ul", "ol", "li",
        "strong", "em", "del",
        "blockquote",
        "pre", "code",
        "table", "thead", "tbody", "tr", "th", "td",
        "a",
        "hr"
    })

    allowed_attrs = {
        "*": ["class", "id"],
        "a": ["href", "title"],
        "img": ["src", "alt"]
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
    return render_template("index.html")


@app.route("/note")
def note():
    with open("markdowns/sample.md", "r") as f:
        md_text = f.read()
    html_text = md_to_html(md_text)
    return render_template("note.html", markdown=html_text)

if __name__ == "__main__":
    app.run(debug=True, port=8000)
