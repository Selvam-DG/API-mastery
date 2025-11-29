import uuid
from datetime import datetime
from app import db, bcrypt
import enum

    

class Project(db.Model):
    """Project model for organizing tasks."""
    
    __tablename__ = 'projects'
    
    id = db.Column( db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()) )
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    color = db.Column(db.String(7), nullable=True, default='#3B82F6')  # Hex color code
    is_active = db.Column(db.Boolean, default=True, nullable=False)
    is_archived = db.Column(db.Boolean, default=False, nullable=False)
    user_id = db.Column(db.String(36),    db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False,  index=True )
    created_at = db.Column( db.DateTime, nullable=False, default=datetime.utcnow )
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow )
    tasks = db.relationship( 'Task', backref='project', lazy='dynamic', cascade='all, delete-orphan',  order_by='Task.created_at.desc()' )
    
    def __init__(self, name, user_id, description=None, color=None):
        """
        Initialize project.
        """
        self.name = name
        self.user_id = user_id
        self.description = description
        if color:
            self.color = color
    
    def to_dict(self, include_tasks=False, include_stats=False):
        """Convert project object to dictionary."""
        data = {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'color': self.color,
            'is_active': self.is_active,
            'is_archived': self.is_archived,
            'user_id': self.user_id,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
        
        if include_stats:
            data['stats'] = self.get_stats()
        
        if include_tasks:
            data['tasks'] = [task.to_dict() for task in self.tasks.all()]
        
        return data
    
    def get_stats(self):
        """Get project statistics."""
        from .task import TaskStatus, Task
        
        total_tasks = self.tasks.count()
        completed_tasks = self.tasks.filter_by(status=TaskStatus.COMPLETED).count()
        pending_tasks = self.tasks.filter_by(status=TaskStatus.PENDING).count()
        in_progress_tasks = self.tasks.filter_by(status=TaskStatus.IN_PROGRESS).count()
        
        return {
            'total_tasks': total_tasks,
            'completed_tasks': completed_tasks,
            'pending_tasks': pending_tasks,
            'in_progress_tasks': in_progress_tasks,
            'completion_rate': round((completed_tasks / total_tasks * 100), 2) if total_tasks > 0 else 0
        }
    
    def archive(self):
        """Archive the project."""
        self.is_archived = True
        self.is_active = False
        db.session.commit()
    
    def unarchive(self):
        """Unarchive the project."""
        self.is_archived = False
        self.is_active = True
        db.session.commit()
    
    def __repr__(self):
        """String representation of Project."""
        return f'<Project {self.name}>'
    
    @staticmethod
    def find_by_id(project_id):
        """Find project by ID."""
        return Project.query.get(project_id)
    
    @staticmethod
    def find_by_user(user_id, include_archived=False):
        """Find all projects for a user."""
        query = Project.query.filter_by(user_id=user_id)
        
        if not include_archived:
            query = query.filter_by(is_archived=False)
        
        return query.order_by(Project.created_at.desc()).all()
    
    @staticmethod
    def find_user_project(project_id, user_id):
        """Find project by ID and verify ownership."""
        return Project.query.filter_by(id=project_id, user_id=user_id).first()
    
    
