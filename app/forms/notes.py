from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    TextAreaField,
    FormField,
    FieldList,
    SubmitField,
)
from wtforms.validators import DataRequired, Length, Optional


# タグ入力フォーム（サブフォーム）
class TagForm(FlaskForm):
    tagname = StringField(
        "タグ名（空欄可）",
        validators=[Optional()],  # タグ入力なしを許容するためOptional
        render_kw={"placeholder": "タグ名"},
    )


class NewNoteForm(FlaskForm):
    title = StringField(
        "タイトル",
        validators=[
            DataRequired(message="タイトルは必須です"),
            Length(max=200, message="タイトルは200文字以内で入力してください"),
        ],
        render_kw={"placeholder": "実験タイトル"},
    )
    content_md = TextAreaField(
        "ノート (Markdown)",
        render_kw={
            "rows": 20,
            "placeholder": "Markdownで実験内容を記述してください",
        },
    )

    # タグを複数入力できるフォーム
    tags = FieldList(FormField(TagForm), min_entries=1, max_entries=10)
    submit = SubmitField("保存")


class EditNoteForm(FlaskForm):
    title = StringField(
        "タイトル", validators=[DataRequired(message="タイトルは必須です")]
    )
    content_md = TextAreaField("ノート (Markdown)", render_kw={"rows": 20})

    # タグを複数入力できるフォーム
    tags = FieldList(FormField(TagForm), min_entries=1, max_entries=10)
    submit = SubmitField("保存")


class SearchForm(FlaskForm):
    class Meta:
        csrf = False  # getリクエストのためcsrfトークンを生成しない

    q = StringField(
        "タイトル検索",
        validators=[Optional(), Length(max=200)],
    )
    submit = SubmitField("検索")
