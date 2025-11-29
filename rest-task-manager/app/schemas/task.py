from marshmallow import Schema, fields, validate, validates, ValidationError
import re
from datetime import datetime




class TaskCreateSchema(Schema):
    """Schema for creating a new task."""
    
    title = fields.Str(
        required=True,
        validate=validate.Length(min=1, max=200, error='Task title must be between 1 and 200 characters'),
        error_messages={'required': 'Task title is required'}
    )
    description = fields.Str(
        required=False,
        validate=validate.Length(max=2000, error='Description must be less than 2000 characters')
    )
    status = fields.Str(
        required=False,
        validate=validate.OneOf(
            ['pending', 'in_progress', 'completed', 'archived'],
            error='Invalid status. Must be one of: pending, in_progress, completed, archived'
        )
    )
    priority = fields.Str(
        required=False,
        validate=validate.OneOf(
            ['low', 'medium', 'high', 'urgent'],
            error='Invalid priority. Must be one of: low, medium, high, urgent'
        )
    )
    due_date = fields.Date(
        required=False,
        format='%Y-%m-%d',
        error_messages={'invalid': 'Invalid date format. Use YYYY-MM-DD'}
    )
    project_id = fields.Str(
        required=True,
        error_messages={'required': 'Project ID is required'}
    )
    
    @validates('due_date')
    def validate_due_date(self, value):
        """Validate that due date is not in the past."""
        if value and value < datetime.utcnow().date():
            raise ValidationError('Due date cannot be in the past')


class TaskUpdateSchema(Schema):
    """Schema for updating a task."""
    
    title = fields.Str(
        required=False,
        validate=validate.Length(min=1, max=200, error='Task title must be between 1 and 200 characters')
    )
    description = fields.Str(
        required=False,
        validate=validate.Length(max=2000, error='Description must be less than 2000 characters')
    )
    status = fields.Str(
        required=False,
        validate=validate.OneOf(
            ['pending', 'in_progress', 'completed', 'archived'],
            error='Invalid status. Must be one of: pending, in_progress, completed, archived'
        )
    )
    priority = fields.Str(
        required=False,
        validate=validate.OneOf(
            ['low', 'medium', 'high', 'urgent'],
            error='Invalid priority. Must be one of: low, medium, high, urgent'
        )
    )
    due_date = fields.Date(
        required=False,
        format='%Y-%m-%d',
        allow_none=True,
        error_messages={'invalid': 'Invalid date format. Use YYYY-MM-DD'}
    )
    project_id = fields.Str(required=False)


class TaskStatusUpdateSchema(Schema):
    """Schema for updating task status only."""
    
    status = fields.Str(
        required=True,
        validate=validate.OneOf(
            ['pending', 'in_progress', 'completed', 'archived'],
            error='Invalid status. Must be one of: pending, in_progress, completed, archived'
        ),
        error_messages={'required': 'Status is required'}
    )


class TaskResponseSchema(Schema):
    """Schema for task response."""
    
    id = fields.Str(dump_only=True)
    title = fields.Str(dump_only=True)
    description = fields.Str(dump_only=True)
    status = fields.Str(dump_only=True)
    priority = fields.Str(dump_only=True)
    due_date = fields.Date(dump_only=True)
    completed_at = fields.DateTime(dump_only=True)
    project_id = fields.Str(dump_only=True)
    user_id = fields.Str(dump_only=True)
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)
    is_overdue = fields.Bool(dump_only=True)
    project = fields.Dict(dump_only=True)


class TaskListResponseSchema(Schema):
    """Schema for task list response."""
    
    id = fields.Str(dump_only=True)
    title = fields.Str(dump_only=True)
    description = fields.Str(dump_only=True)
    status = fields.Str(dump_only=True)
    priority = fields.Str(dump_only=True)
    due_date = fields.Date(dump_only=True)
    project_id = fields.Str(dump_only=True)
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)
    is_overdue = fields.Bool(dump_only=True)


class TaskFilterSchema(Schema):
    """Schema for task filtering parameters."""
    
    status = fields.Str(
        required=False,
        validate=validate.OneOf(
            ['pending', 'in_progress', 'completed', 'archived'],
            error='Invalid status'
        )
    )
    priority = fields.Str(
        required=False,
        validate=validate.OneOf(
            ['low', 'medium', 'high', 'urgent'],
            error='Invalid priority'
        )
    )
    project_id = fields.Str(required=False)
    overdue = fields.Bool(required=False)
    page = fields.Int(
        required=False,
        validate=validate.Range(min=1, error='Page must be at least 1'),
        missing=1
    )
    per_page = fields.Int(
        required=False,
        validate=validate.Range(min=1, max=100, error='Per page must be between 1 and 100'),
        missing=20
    )