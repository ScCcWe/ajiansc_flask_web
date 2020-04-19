# instantiated flask
import click
import os
import sys
from flask import Flask, url_for, render_template, request, flash, redirect
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

if sys.platform.startswith('win'):
    prefix = 'sqlite:///'
else:
    prefix = 'sqlite:////'

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'if_not_secret_key_use_this')
app.config['SQLALCHEMY_DATABASE_URI'] = prefix + os.path.join(app.root_path, os.getenv('DATABASE_FILE', 'data.db'))
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


@app.route('/', methods=['GET', 'POST'])  # 修改视图函数，使其能够处理POST请求；默认只处理get
def index():
    if request.method == 'POST':
        title = request.form.get('title')
        year = request.form.get('year')
        if not title or not year or len(year) > 4 or len(title) > 60:
            flash('Invalid input.')
            return redirect(url_for('index'))  # 重定向回主页
        movie = Movie(title=title, year=year)
        db.session.add(movie)
        db.session.commit()
        flash('Item created.')
        return redirect(url_for('index'))
    # user = User.query.first()  # the below decorator provides
    movies = Movie.query.all()
    return render_template('index.html', movies=movies)


@app.route('/movie/edit/<int:movie_id>', methods=['GET', 'POST'])  # 修改视图函数，使其能够处理POST请求；默认只处理get
def edit(movie_id):
    movie = Movie.query.get_or_404(movie_id)
    if request.method == 'POST':
        title = request.form['title']
        year = request.form['year']
        if not title or not year or len(year) > 4 or len(title) > 60:
            flash('Invalid input.')
            return redirect(url_for('edit', movie_id=movie_id))  # 重定向回主页
        movie.title = title
        movie.year = year
        db.session.commit()
        flash('Item updated.')
        return redirect(url_for('index'))
    return render_template('edit.html', movie=movie)


@app.route('/movie/delete/<int:movie_id>', methods=['POST'])
def delete(movie_id):
    movie = Movie.query.get_or_404(movie_id)
    db.session.delete(movie)
    db.session.commit()
    flash('Item deleted.')
    return redirect(url_for('index'))


class User(db.Model):  # 表名将会是user(自动生成，小写处理)
    # 类属性字段实例化 db.Column
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20))
    username = db.Column(db.String(20))  # 用户名
    password_hash = db.Column(db.String(128))  # 密码散列值

    def set_password(self, password):  # 设置密码
        self.password_hash = generate_password_hash(password)

    def validate_password(self, password):  # 验证密码
        return check_password_hash(self.password_hash, password)


class Movie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(60))
    year = db.Column(db.String(4))


@app.cli.command()
@click.option('--drop', is_flag=True, help='Create after drop.')
# use_like_this: $ flask initdb --drop
def initdb(drop):
    if drop:
        db.drop_all()
    db.create_all()
    click.echo('Init database success!')


@app.cli.command()
def forge():
    """
    增加一些数据
    :return:
    """
    db.create_all()
    
    name = 'AJianSc'
    movies = [
        {"title": "nihao", 'year': "1999"},
        {"title": "nihao2", 'year': "2009"},
    ]
    
    user = User(name=name)
    db.session.add(user)
    for m in movies:
        movie = Movie(title=m['title'], year=m['year'])
        db.session.add(movie)
    
    db.session.commit()
    click.echo('Done.')


@app.cli.command()
@click.option('--username', prompt=True, help='The username used to login.')
@click.option('--password', prompt=True, hide_input=True, confirmation_prompt=True, help='The password used to login.')
def admin(username, password):
    """create user"""
    db.create_all()

    user = User.query.first()
    if user is not None:
        click.echo('Updating user...')



@app.errorhandler(404)
def page_not_found(e):
    # user = User.query.first()  # the decorator below provides user
    # return render_template('404.html', user=user)
    return render_template('404.html'), 404


@app.context_processor
def inject_user():
    user = User.query.first()
    return dict(user=user)
