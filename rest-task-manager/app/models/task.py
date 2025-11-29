import uuid
from datetime import datetime
from app import db, bcrypt
import enum



class TaskStatus(enum.Enum):
    """Task status enumeration."""
    PENDING = 'pending'
    IN_PROGRESS = 'in_progress'
    COMPLETED = 'completed'
    ARCHIVED = 'archived'


class TaskPriority(enum.Enum):
    """Task priority enumeration."""
    LOW = 'low'
    MEDIUM = 'medium'
    HIGH = 'high'
    URGENT = 'urgent'


class Task(db.Model):
    """
    Task model for managing individual tasks.
    """
    
    __tablename__ = 'tasks'
    
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=True)
    status = db.Column(db.Enum(TaskStatus), nullable=False, default=TaskStatus.PENDING, index=True)
    priority = db.Column(db.Enum(TaskPriority), nullable=False, default=TaskPriority.MEDIUM,  index=True )
    due_date = db.Column(db.Date, nullable=True, index=True)
    completed_at = db.Column(db.DateTime, nullable=True)
    project_id = db.Column(db.String(36), db.ForeignKey('projects.id', ondelete='CASCADE'), nullable=False, index=True)
    user_id = db.Column(db.String(36), db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False, index=True )
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, index=True )
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow )
    
    def __init__(self, title, user_id, project_id, description=None, 
                 status=TaskStatus.PENDING, priority=TaskPriority.MEDIUM, due_date=None):
        """Initialize task."""
        self.title = title
        self.user_id = user_id
        self.project_id = project_id
        self.description = description
        self.status = status
        self.priority = priority
        self.due_date = due_date
    
    def to_dict(self, include_project=False):
        """Convert task object to dictionary."""
        data = {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'status': self.status.value,
            'priority': self.priority.value,
            'due_date': self.due_date.isoformat() if self.due_date else None,
            'completed_at': self.completed_at.isoformat() if self.completed_at else None,
            'project_id': self.project_id,
            'user_id': self.user_id,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'is_overdue': self.is_overdue()
        }
        
        if include_project and self.project:
            data['project'] = {
                'id': self.project.id,
                'name': self.project.name,
                'color': self.project.color
            }
        
        return data
    
    def update_status(self, new_status):
        """Update task status and handle completion timestamp."""
        if isinstance(new_status, str):
            new_status = TaskStatus(new_status)
        
        self.status = new_status
        
        if new_status == TaskStatus.COMPLETED and not self.completed_at:
            self.completed_at = datetime.utcnow()
        elif new_status != TaskStatus.COMPLETED and self.completed_at:
            self.completed_at = None
        
        db.session.commit()
    
    def is_overdue(self):
        """Check if task is overdue."""
        if self.due_date and self.status not in [TaskStatus.COMPLETED, TaskStatus.ARCHIVED]:
            return datetime.utcnow().date() > self.due_date
        return False
    
    def archive(self):
        """Archive the task."""
        self.status = TaskStatus.ARCHIVED
        db.session.commit()
    
    def __repr__(self):
        """String representation of Task."""
        return f'<Task {self.title}>'
    
    @staticmethod
    def find_by_id(task_id):
        """Find task by ID."""
        return Task.query.get(task_id)
    
    @staticmethod
    def find_user_task(task_id, user_id):
        """Find task by ID and verify ownership."""
        return Task.query.filter_by(id=task_id, user_id=user_id).first()
    
    @staticmethod
    def find_by_user(user_id, filters=None, page=1, per_page=20):
        """Find tasks for a user with optional filters."""
        query = Task.query.filter_by(user_id=user_id)
        
        if filters:
            if 'status' in filters:
                query = query.filter_by(status=TaskStatus(filters['status']))
            
            if 'priority' in filters:
                query = query.filter_by(priority=TaskPriority(filters['priority']))
            
            if 'project_id' in filters:
                query = query.filter_by(project_id=filters['project_id'])
            
            if 'overdue' in filters and filters['overdue']:
                query = query.filter(
                    Task.due_date < datetime.utcnow().date(),
                    Task.status.notin_([TaskStatus.COMPLETED, TaskStatus.ARCHIVED])
                )
        
        # Order by priority and due date
        query = query.order_by(
            Task.priority.desc(),
            Task.due_date.asc().nullslast(),
            Task.created_at.desc()
        )
        
        return query.paginate(page=page, per_page=per_page, error_out=False)
    
    @staticmethod
    def find_by_project(project_id, user_id, page=1, per_page=20):
        """Find tasks for a specific project."""
        query = Task.query.filter_by(project_id=project_id, user_id=user_id)
        query = query.order_by(Task.created_at.desc())
        
        return query.paginate(page=page, per_page=per_page, error_out=False)