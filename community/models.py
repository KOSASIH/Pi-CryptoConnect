from pi_cryptoconnect.database import db
from datetime import datetime

class Post(db.Model):
    __tablename__ = 'posts'  # Explicitly define the table name

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship('User ', backref=db.backref('posts', lazy=True))
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)  # Timestamp for creation
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)  # Timestamp for updates

    def __repr__(self):
        return f'<Post {self.id}: {self.title}>'

class Strategy(db.Model):
    __tablename__ = 'strategies'  # Explicitly define the table name

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)  # Ensure unique strategy names
    description = db.Column(db.Text, nullable=False)
    code = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship('User ', backref=db.backref('strategies', lazy=True))
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)  # Timestamp for creation
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)  # Timestamp for updates

    def __repr__(self):
        return f'<Strategy {self.id}: {self.name}>'
