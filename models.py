from uuid import uuid4
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from sqlalchemy.dialects.postgresql import UUID, JSONB

db = SQLAlchemy()

# Association table for User roles
user_roles = db.Table('user_roles',
    db.Column('user_id', UUID(as_uuid=True), db.ForeignKey('user.id')),
    db.Column('role', db.String(50))
)

class User(db.Model):
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    roles = db.relationship('Role', secondary=user_roles, backref='users')
    datasets = db.relationship('Dataset', backref='publisher', lazy=True)

    def login(self):
        pass  # Implement login logic

    def publish_dataset(self, title, description):
        dataset = Dataset(title=title, description=description, publisher=self)
        db.session.add(dataset)
        db.session.commit()
        return dataset

class Dataset(db.Model):
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    publisher_id = db.Column(UUID(as_uuid=True), db.ForeignKey('user.id'), nullable=False)
    files = db.relationship('File', backref='dataset', lazy=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    metadata = db.Column(JSONB, default=dict)

    def add_file(self, url, format, size):
        file = File(url=url, format=format, size=size, dataset=self)
        db.session.add(file)
        db.session.commit()
        return file

    def update_metadata(self, title=None, description=None):
        if title:
            self.title = title
        if description:
            self.description = description
        db.session.commit()

class File(db.Model):
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    url = db.Column(db.String(500), nullable=False)
    format = db.Column(db.String(50))
    size = db.Column(db.Integer)
    dataset_id = db.Column(UUID(as_uuid=True), db.ForeignKey('dataset.id'), nullable=False)
    uploaded_at = db.Column(db.DateTime, default=datetime.now) 