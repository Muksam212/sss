from typing_extensions import runtime
from flask.helpers import url_for
from flask_sqlalchemy import SQLAlchemy
from flask import Flask, render_template, request, redirect,flash


app = Flask(__name__)
app.config['SECRET_KEY']='e44ed30969ca77afe43107d90b157943'

app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///site.db'

db=SQLAlchemy(app)

class Data(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    name=db.Column(db.String(100))
    email=db.Column(db.String(100))
    info=db.Column(db.String(100))

    def __init__(self, name, email, info):
        self.name=name
        self.email=email
        self.info=info



@app.route('/')
def home():
    all_data=Data.query.all()
    return render_template('home.html', employees=all_data)

@app.route('/insert',methods=['POST'])
def insert():
    if request.method=='POST':
        name=request.form['name']
        email=request.form['email']
        info=request.form['info']

        my_data=Data(name, email, info)
        db.session.add(my_data)
        db.session.commit()
        flash('Data is successfully Inserted')

    return redirect(url_for('home'))

@app.route('/update', methods=['GET','POST'])
def update():
    if request.method=="POST":
        my_data=Data.query.get(request.form.get('id'))

        my_data.name=request.form['name']
        my_data.email=request.form['email']
        my_data.info=request.form['info']

        db.session.commit()
        flash('Data is updated successfully')
        return redirect(url_for('home'))


@app.route('/delete/<id>/', methods=['GET','POST'])
def delete(id):
    my_data=Data.query.get(id)
    db.session.delete(my_data)
    db.session.commit()
    flash('Data delete successfully')
    return redirect(url_for('home'))
    
if __name__ == '__main__':
    app.run(debug=True)
