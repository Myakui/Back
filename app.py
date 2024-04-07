from flask import Flask, request, jsonify, redirect, render_template, url_for
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///changes.db'
db = SQLAlchemy(app)
CORS(app)  # Настройка CORS



class TextChange(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, default=datetime.utcnow)
    title = db.Column(db.String(100),nullable=False)
    intro = db.Column(db.String(300),nullable=False)
    text = db.Column(db.Text,nullable=False)

    def __repr__(self):
        return '<TextChange %r>' % self.id



@app.route('/posts')
def posts():
    scenarios = TextChange.query.order_by(TextChange.date.desc()).all()
    return render_template("posts.html", scenarios = scenarios)



@app.route('/posts/<int:id>')
def post_detail(id):
    scenario = TextChange.query.get(id)
    return render_template("post_detail.html", scenario = scenario)


@app.route('/posts/<int:id>/del')
def post_delete(id):
    scenario = TextChange.query.get_or_404(id)
    try:
        db.session.delete(scenario)
        db.session.commit()
        return redirect('/posts')
    except:
        return "При удалении сценария произошла ошибка"


@app.route("/posts/<int:id>/update", methods=['POST','GET'])
def post_update(id):
    scenario = TextChange.query.get(id)
    if request.method == "POST":
        scenario.title = request.form['title']
        scenario.intro = request.form['intro']
        scenario.text = request.form['text']

        try:
            db.session.commit()
            return redirect('/posts')
        except:
            return "При редактировании сценария произошла ошибка"
    else:
        return render_template("post_update.html", scenario=scenario)



@app.route("/", methods=['POST','GET'])
def create_scenario():
    if request.method == "POST":
        title = request.form['title']
        intro = request.form['intro']
        text = request.form['text']

        Changes = TextChange(title=title,intro=intro,text=text)

        try:
            db.session.add(Changes)
            db.session.commit()
            return redirect('/')
        except:
            return "При загрузке сценария произошла ошибка"
    else:
        return render_template("create-scenario.html")








if __name__ == "__main__":
    app.run(port=8040)
