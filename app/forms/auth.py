from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, EqualTo

class RegistrationForm(FlaskForm):
    username = StringField(
            'Username', 
            validators=[
                DataRequired(message='ユーザー名は必須です'),
                Length(max=100, message="ユーザー名は100文字以内で入力してください")
            ]
        )
    password = PasswordField(
            'Password', 
            validators=[
                DataRequired(message='パスワードは必須です'),
                Length(min=12, max=64, message='パスワードは12文字以上64字以下で入力してください')
            ]
        )
    confirm = PasswordField(
            "Confirm Password", 
            validators=[
                DataRequired(message='パスワードは必須です'),
                EqualTo('password', message='パスワードが一致しません')
            ]
        )
    submit = SubmitField('登録')


class LoginForm(FlaskForm):
    username = StringField(
        'Username',
        validators=[
            DataRequired(message="ユーザー名は必須です")
        ]
    )
    password = PasswordField(
        'Password',
        validators=[
            DataRequired(message='パスワードは必須です'),
        ]
    )
    submit = SubmitField('ログイン')
    
