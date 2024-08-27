import os

import click
from flask import Flask, url_for, render_template, flash, redirect, request
from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'+os.path.join(app.root_path,'test.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'dev'
db=SQLAlchemy(app)
@app.cli.command()
@click.option('--drop', is_flag=True, help='Delete database if exists')
def initdb(drop):
    if drop:
        db.drop_all()
        click.echo('Dropped database')
    elif None:
        db.create_all()
        click.echo('Initialized database')
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name=db.Column(db.String(20))
class Movie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title=db.Column(db.String(60))
    year=db.Column(db.String(4))
@app.cli.command()
def forge():
    db.create_all()
    name='Mr.li'
    movies=[
        {'title': 'My Neighbor Totoro', 'year': '1988'},
        {'title': 'Dead Poets Society', 'year': '1989'},
        {'title': 'A Perfect World', 'year': '1993'},
        {'title': 'Leon', 'year': '1994'},
        {'title': 'Mahjong', 'year': '1996'},
        {'title': 'Swallowtail Butterfly', 'year': '1996'},
        {'title': 'King of Comedy', 'year': '1999'},
        {'title': 'Devils on the Doorstep', 'year': '1999'},
        {'title': 'WALL-E', 'year': '2008'},
        {'title': 'The Pork of Music', 'year': '2012'},
    ]
    user=User(name=name)
    db.session.add(user)
    for m in movies:
        movie=Movie(title=m['title'], year=m['year'])
        db.session.add(movie)
    db.session.commit()
    click.echo('Forged successfully')
@app.route('/',methods=['GET','POST'])
def index():  # put application's code here
    if request.method == 'POST':
        title=request.form.get('title')
        year=request.form.get('year')
        if not title or not year or len(year)>4 or len(title)>60:
            print(title,year)
            flash("invalid input")
            return redirect(url_for('index'))
        movie=Movie(title=title, year=year)
        db.session.add(movie)
        db.session.commit()
        flash("item created")
    movies=Movie.query.all()
    return render_template('index.html',movies=movies)
@app.route('/movie/edit/<int:movie_id>',methods=['GET','POST'])
def edit(movie_id):
    movie=Movie.query.get_or_404(movie_id)
    if request.method=='POST':
        title=request.form['title']
        year=request.form['year']
        if not title or not year or len(year)!=4 or len(title)>60:
            flash("invalid input")
            return redirect(url_for('index'))
        movie.title=title
        movie.year=year
        db.session.commit()
        flash("item updated")
        return redirect(url_for('index'))
    return render_template('edit.html',movie=movie)
@app.route('/movie/delete/<int:movie_id>',methods=['POST'])
def delete(movie_id):
    movie=Movie.query.get_or_404(movie_id)
    db.session.delete(movie)
    db.session.commit()
    flash("item deleted")
    return redirect(url_for('index'))
@app.route('/user/<name>')
def user_page(name):
    return f'User:{name}'
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404
@app.context_processor
def inject_user():
    user=User.query.first()
    return {'user':user}
if __name__ == '__main__':
    app.run(debug=True)
