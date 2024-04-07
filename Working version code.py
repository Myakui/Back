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

    def to_dict(self):
        return {
            "id": self.id,
            "text": self.text
        }



@app.route("/", methods=['GET', 'POST'])
def hello_world():
    if request.method == "GET":
        texts = TextChange.query.all()
        response_data = {
            "messages": [text.to_dict() for text in texts]
        }
        return jsonify(response_data)



if __name__ == "__main__":
    app.run(port=5000)