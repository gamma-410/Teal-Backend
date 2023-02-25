# copyright (c) 2022 @gamma410 All rights reserved.

from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from json_serializable import JSONSerializable  # SpecialThanks...!
import datetime
import pytz
import hashlib

app = Flask(__name__)

CORS(
    app,
    supports_credentials=True
)

JSONSerializable(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tealDB.db'
app.config['SCRET_KEY'] = '5730292743938474948439320285857603'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    postdate = db.Column(db.Text, nullable=False)
    username = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(20), nullable=False)
    tweet = db.Column(db.Text, nullable=False)

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/tweet')
def tweetAll():
    timeline = Post.query.order_by(Post.id.desc()).all()
    return jsonify(timeline)


@app.route('/tweet/<int:id>')
def tweetDetail(id):
    tweet = Post.query.filter_by(id=id).order_by(Post.id.desc()).all()
    return jsonify(tweet)


@app.route('/post', methods=['GET', 'POST'])
def post():
    postdate = datetime.datetime.now(pytz.timezone('Asia/Tokyo')).strftime('%Y/%m/%d - %H:%M:%S')
    username = request.args['username']
    email = request.args['email']
    email = email.encode()
    tweet = request.args['tweet']

    createPost = Post(
        postdate = postdate,
        email = hashlib.md5(email).hexdigest(),
        username = username,
        tweet = tweet
    )

    db.session.add(createPost)
    db.session.commit()
    return "post"


@app.route('/delete/<int:id>', methods=['GET', 'POST'])
def delete(id):
    removePost = Post.query.get(id)
    db.session.delete(removePost)
    db.session.commit()
    return "delete"


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=80)