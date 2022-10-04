from flask import Flask, request, redirect, jsonify
from models import connect_db, User, db,  Post

app = Flask(__name__)

# Database URI needs to be changed to the name of your database
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///flask-api' # Here
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

app.config['SECRET_KEY'] = "SECRET!"

connect_db(app)
db.create_all()

@app.get('/')
def redirect_to_users():
    """Redirects to the users endpoint"""

    return redirect('/users')

@app.get('/users')
def list_users():
    """Get's a list of all users and returns as JSON like:
        {"users": [{
            id,
            first_name,
            last_name,
            posts:[{id,title,content,created_at,user_id},...]
        }
    """

    users = User.query.all()
    # Need to serialize to normal dict instead of obj if returning as JSON
    users = [user.serialize() for user in users]

    return jsonify(users)

@app.post('/users')
def create_user():
    """ Takes first_name and last_name sent in body of request.
        Creates a new user. Returns JSON of {"post_user":"successful"}
        with status code of 201.
    """
    print("request =",request.json)
    first_name = request.json['first_name']
    last_name = request.json['last_name']

    user = User(
        first_name=first_name,
        last_name=last_name
    )

    db.session.add(user)
    db.session.commit()

    return jsonify({"post_user":"successful"}), 201

@app.delete('/users/<int:id>')
def delete_user(id):
    """ Takes user's id in the pathway. Deletes user.
        If successful, returns JSON of {"deleted":id}
        If unsuccessful, returns a 404 status code and error message
    """

    user = User.query.get_or_404(id)

    db.session.delete(user)
    db.session.commit()

    return jsonify({"deleted":id})