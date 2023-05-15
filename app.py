from flask import Flask,render_template,redirect,url_for
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired
import confidential

app=Flask(__name__)
app.config['SECRET_KEY']=confidential.SECRET_KEY
app.config["SQLALCHEMY_DATABASE_URI"]=confidential.SQLALCHEMY_DATABASE_URI
db=SQLAlchemy(app)
app.app_context().push()


class Todo(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String,nullable=False)
    state=db.Column(db.String,nullable=False)

    def __repr__(self):
        return "<NAME %r>" %self.name
    
ttodo=Todo.query.order_by(Todo.id)

class TodoForm(FlaskForm):
    name=StringField("Todo Name: ",validators=[DataRequired()])

@app.route('/',methods=["POST","GET"])
def index():
    form=TodoForm()
    if form.validate_on_submit():
        todo=Todo(name=form.name.data,state="Have To Do")
        db.session.add(todo)
        db.session.commit()
        return redirect(url_for('index'))
    count=Todo.query.filter_by(state="Have To Do").count()
    return render_template('index.html',Ttodo=ttodo,Count=count,Form=form)

@app.route('/update/<s>')
def update(s):
    todo = db.session.execute(db.select(Todo).filter_by(name=s)).scalar_one()
    if todo.state=="Have To Do":
        todo.state="Done"
    else:
        todo.state="Have To Do"
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/delete/<i>')
def delete(i):
    todo = db.session.execute(db.select(Todo).filter_by(name=i)).scalar_one()
    db.session.delete(todo)
    db.session.commit()
    return redirect(url_for('index'))

if __name__=="__main__":
    app.run(debug=True)