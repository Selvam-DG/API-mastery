from marshmallow import Schema, fields, validate, validates, ValidationError
import re
from datetime import datetime


class ProjectCreateSchema(Schema):
    """Schema for creating a new project."""
    
    name = fields.Str(
        required=True,
        validate=validate.Length(min=1, max=100, error='Project name must be between 1 and 100 characters'),
        error_messages={'required': 'Project name is required'}
    )
    description = fields.Str(
        required=False,
        validate=validate.Length(max=1000, error='Description must be less than 1000 characters')
    )
    color = fields.Str(
        required=False,
        validate=validate.Length(equal=7, error='Color must be a valid hex code (e.g., #3B82F6)')
    )
    
    @validates('color')
    def validate_color(self, value):
        """Validate hex color code format."""
        if value and not re.match(r'^#[0-9A-Fa-f]{6}$', value):
            raise ValidationError('Color must be a valid hex code (e.g., #3B82F6)')


class ProjectUpdateSchema(Schema):
    """Schema for updating a project."""
    
    name = fields.Str(
        required=False,
        validate=validate.Length(min=1, max=100, error='Project name must be between 1 and 100 characters')
    )
    description = fields.Str(
        required=False,
        validate=validate.Length(max=1000, error='Description must be less than 1000 characters')
    )
    color = fields.Str(
        required=False,
        validate=validate.Length(equal=7, error='Color must be a valid hex code (e.g., #3B82F6)')
    )
    is_active = fields.Bool(required=False)
    
    @validates('color')
    def validate_color(self, value):
        """Validate hex color code format."""
        if value and not re.match(r'^#[0-9A-Fa-f]{6}$', value):
            raise ValidationError('Color must be a valid hex code (e.g., #3B82F6)')


class ProjectResponseSchema(Schema):
    """Schema for project response."""
    
    id = fields.Str(dump_only=True)
    name = fields.Str(dump_only=True)
    description = fields.Str(dump_only=True)
    color = fields.Str(dump_only=True)
    is_active = fields.Bool(dump_only=True)
    is_archived = fields.Bool(dump_only=True)
    user_id = fields.Str(dump_only=True)
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)
    stats = fields.Dict(dump_only=True)


class ProjectListResponseSchema(Schema):
    """Schema for project list response."""
    
    id = fields.Str(dump_only=True)
    name = fields.Str(dump_only=True)
    description = fields.Str(dump_only=True)
    color = fields.Str(dump_only=True)
    is_active = fields.Bool(dump_only=True)
    is_archived = fields.Bool(dump_only=True)
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)
    stats = fields.Dict(dump_only=True)
    
    
