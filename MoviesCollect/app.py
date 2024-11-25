from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = \
    'mysql+pymysql://root:114514@localhost/MoviesCollect'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
# 定义用户与电影的关联表
user_movie = db.Table('user_movie',
                       db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
                       db.Column('movie_id', db.Integer, db.ForeignKey('movie.id'), primary_key=True)
                       )
# 用户表 = 'user'
class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)
    collected_movies = db.relationship('Movie', secondary=user_movie,
                                    backref=db.backref('collectors', lazy='dynamic'))
# 电影表 = 'movies'
class Movie(db.Model):
    __tablename__ = 'movie'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    type = db.Column(db.String(80),  nullable=False)
    director = db.Column(db.String(80),  nullable=False)
    year = db.Column(db.String(80), nullable=False)
    actors = db.Column(db.String(80),nullable=False)
    img_path = db.Column(db.String(255), nullable=True)
    descripe = db.Column(db.String(255), nullable=True)


with app.app_context():
    db.create_all()

@app.route('/')# 主页
def index():
    movies = Movie.query.all()
    return render_template("index.html", movies=movies)

@app.route('/detail/<int:id>')# 详情页
def detail(id):
    movie = Movie.query.get(id)
    return render_template("movieDetail.html", movie=movie)

if __name__ == '__main__':
    app.run("0.0.0.0",41834,debug=True)
