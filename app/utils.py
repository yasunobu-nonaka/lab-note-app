from markdown_it import MarkdownIt
from mdit_py_plugins.tasklists import tasklists_plugin
from mdit_py_plugins.footnote import footnote_plugin
from mdit_py_plugins.deflist import deflist_plugin
from mdit_py_plugins.subscript import sub_plugin
import re
import bleach

def md_to_html(md_string):
    # MarkdownをHTMLに変換する関数

    md = (
        MarkdownIt("commonmark", {
            "html": False, # markdownに直接書かれたHTMLをエスケープ
            "breaks": True,
            }
        )
        .use(tasklists_plugin, enabled=True)
        .use(footnote_plugin) # 例：これは脚注付きの文章です。[1]
        .use(deflist_plugin)
        .use(sub_plugin)
        .enable('table')
        .enable("strikethrough") # 打ち消し線の表示
    )

    # markdown表記をHTMLに変換、直書きHTMLはエスケープ
    raw_html = md.render(md_string)
    
    # sub / sup だけエスケープされた状態からタグに戻す
    raw_html = re.sub(
        r"&lt;(\/?(?:sub|sup))&gt;",
        r"<\1>",
        raw_html,
        flags=re.IGNORECASE
    )

    allowed_tags = bleach.sanitizer.ALLOWED_TAGS.union({
        "h1", "h2", "h3", "h4", "h5", "h6",
        "p", "a", "img", "br", "hr",
        "ul", "ol", "li",
        "strong", "em", "del", "s", # （左から）太字、イタリック、打ち消し線、打ち消し線
        "blockquote", # 引用
        "pre", "code",
        "table", "thead", "tbody", "tr", "th", "td",
        "input", # チェックボックス付きリストで使用
        "sub", "sup", # 上付き文字、下付き文字
        "dl", "dt", "dd" # 定義リスト
    })

    allowed_attrs = {
        "ul": ["class"],
        "li": ["class"],
        "a": ["href", "title"],
        "img": ["src", "alt"],
        "input": ["type", "checked", "disabled"],
    }

    allowed_protocols = ["http", "https", "mailto"]

    safe_html = bleach.clean(
        raw_html,
        tags=allowed_tags,
        attributes=allowed_attrs,
        protocols=allowed_protocols,
    )

    return safe_html
