from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates
db = SQLAlchemy()

class Author(db.Model):
    __tablename__ = 'authors'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True, nullable=False)
    phone_number = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    # Add validators
    @validates('name')
    def validate_name(self, key, name):
        if not name:
            raise ValueError("Valid name required")
        if db.session.query(Author).filter(Author.name == name).filter(Author.id != self.id).count() > 0:
            raise ValueError('Name must be unique')
        return name
    
    @validates('phone_number')
    def validate_phone_number(self, key, phone_number):
        if phone_number and (not all(char.isdigit() for char in phone_number) or len(phone_number) != 10):
            raise ValueError('Phone number must be 10 digits')
        return phone_number


    def __repr__(self):
        return f'Author(id={self.id}, name={self.name})'

class Post(db.Model):
    __tablename__ = 'posts'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    content = db.Column(db.String)
    category = db.Column(db.String)
    summary = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    # Add validators
    @validates('content')
    def validate_content(self, key, content):
        if len(content) >= 250:
            raise ValueError('Content must be at least 250 characters long')
        return content
    
    @validates('summary')
    def validate_summary(self, key, summary):
        if len(summary) <= 250:
            raise ValueError('Summary must be at most 250 characters long')
        return summary


    def __repr__(self):
        return f'Post(id={self.id}, title={self.title} content={self.content}, summary={self.summary})'
