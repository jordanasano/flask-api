from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# Example user model
class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(
        db.Integer,
        primary_key=True,
        autoincrement=True
    )
    first_name = db.Column(
        db.String(20),
        nullable=False
    )
    last_name = db.Column(
        db.String(20),
        nullable=False
    )
    # user.posts get's a list of posts made by user
    # connected by foreign key of user_id in Post model
    posts = db.relationship('Post', 
        backref='user')
    
    # Needed to return as JSON, can't return obj, needs to be dict
    def serialize(self):
        id = self.id
        first_name = self.first_name
        last_name = self.last_name

        # Needs to have keys be string, can't do {id, fn, ln}, 
        # will register as set
        return {"id":id,"first_name":first_name,"last_name":last_name}

# Example post model
class Post(db.Model):
    __tablename__ = 'posts'

    id = db.Column(
        db.Integer,
        primary_key=True,
        autoincrement=True
    )
    title = db.Column(
        db.String(100),
        nullable=False
    )
    content = db.Column(
        db.Text,
        nullable=False
    )
    # Set's to current time if there is no time given
    created_at = db.Column(
        db.DateTime,
        nullable=False,
        default=db.func.now()
    )
    # Connects to User model using users.id
    user_id = db.Column(
        db.Integer,
        db.ForeignKey('users.id')
    )

def connect_db(app):
    """ Connects to database """
    db.app = app
    return db.init_app(app)