import uuid
from datetime import datetime
from app import db, bcrypt
import enum

    
class User(db.Model):
    """
    User model for authentication and task ownership.
    """
    
    __tablename__ = 'users'

    id = db.Column( db.String(36), primary_key=True, default=lambda: str(uuid.uuid4())  )
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    username = db.Column(db.String(80), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    first_name = db.Column(db.String(50), nullable=True)
    last_name = db.Column(db.String(50), nullable=True)
    is_active = db.Column(db.Boolean, default=True, nullable=False)
    is_verified = db.Column(db.Boolean, default=False, nullable=False)
    created_at = db.Column( db.DateTime, nullable=False, default=datetime.utcnow  )
    updated_at = db.Column( db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow  )
    last_login = db.Column(db.DateTime, nullable=True)
    projects = db.relationship( 'Project', backref='owner', lazy='dynamic', cascade='all, delete-orphan' )
    tasks = db.relationship('Task', backref='owner', lazy='dynamic', cascade='all, delete-orphan'  )
    
    def __init__(self, email, username, password, first_name=None, last_name=None):
        """
        Initialize user with hashed password.
        """
        self.email = email.lower()
        self.username = username
        self.first_name = first_name
        self.last_name = last_name
        self.set_password(password)
    
    def set_password(self, password):
        """Hash and set user password."""
        self.password_hash = bcrypt.generate_password_hash(password).decode('utf-8')
    
    def check_password(self, password):
        """Verify password against hash."""
        return bcrypt.check_password_hash(self.password_hash, password)
    
    def update_last_login(self):
        """Update last login timestamp."""
        self.last_login = datetime.utcnow()
        db.session.commit()
    
    def to_dict(self, include_email=False):
        """Convert user object to dictionary."""
        data = {
            'id': self.id,
            'username': self.username,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'is_active': self.is_active,
            'is_verified': self.is_verified,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'last_login': self.last_login.isoformat() if self.last_login else None
        }
        
        if include_email:
            data['email'] = self.email
        
        return data
    
    def __repr__(self):
        """String representation of User."""
        return f'<User {self.username}>'
    
    @staticmethod
    def find_by_email(email):
        """Find user by email address."""
        return User.query.filter_by(email=email.lower()).first()
    
    @staticmethod
    def find_by_username(username):
        """Find user by username."""
        return User.query.filter_by(username=username).first()
    
    @staticmethod
    def find_by_id(user_id):
        """Find user by ID."""
        return User.query.get(user_id)
    
