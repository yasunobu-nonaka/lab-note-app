from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired

class NewNoteForm(FlaskForm):
    title = StringField(
        'タイトル',
        validators=[
            DataRequired(message="タイトルは必須です")
        ],
        render_kw={
            "placeholder": "実験タイトル"
        }
    )
    content_md = TextAreaField(
        'ノート (Markdown)',
        render_kw={
            "rows": 20,
            "placeholder": "Markdownで実験内容を記述してください"
        }
    )
    submit = SubmitField('保存')


class EditNoteForm(FlaskForm):
    title = StringField(
        'タイトル',
        validators=[
            DataRequired(message="タイトルは必須です")
        ]
    )
    content_md = TextAreaField(
        'ノート (Markdown)',
        render_kw={
            "rows": 20
        }
    )
    submit = SubmitField('保存')
