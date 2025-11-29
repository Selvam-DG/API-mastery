from marshmallow import Schema, fields, validate, validates, ValidationError
import re
from datetime import datetime


class UserRegistrationSchema(Schema):
    """Schema for user registration."""
    
    email = fields.Email(
        required=True, 
        error_messages={ 'required': 'Email is required',  'invalid': 'Invalid email address' } )
    username = fields.Str(
        required=True,
        validate=[
            validate.Length(min=3, max=80, error='Username must be between 3 and 80 characters'),
            validate.Regexp(
                r'^[a-zA-Z0-9_]+$',
                error='Username can only contain letters, numbers, and underscores'
            )
        ],
        error_messages={'required': 'Username is required'}
    )
    password = fields.Str(
        required=True,
        validate=validate.Length(min=8, error='Password must be at least 8 characters long'),
        error_messages={'required': 'Password is required'},
        load_only=True
    )
    first_name = fields.Str(
        required=False,
        validate=validate.Length(max=50, error='First name must be less than 50 characters')
    )
    last_name = fields.Str(
        required=False,
        validate=validate.Length(max=50, error='Last name must be less than 50 characters')
    )
    
    @validates('password')
    def validate_password(self, value):
        """Validate password strength."""
        if not re.search(r'[A-Z]', value):
            raise ValidationError('Password must contain at least one uppercase letter')
        if not re.search(r'[a-z]', value):
            raise ValidationError('Password must contain at least one lowercase letter')
        if not re.search(r'[0-9]', value):
            raise ValidationError('Password must contain at least one number')


class UserLoginSchema(Schema):
    """Schema for user login."""
    
    email = fields.Email(
        required=True,
        error_messages={
            'required': 'Email is required',
            'invalid': 'Invalid email address'
        }
    )
    password = fields.Str(
        required=True,
        error_messages={'required': 'Password is required'},
        load_only=True
    )


class UserUpdateSchema(Schema):
    """Schema for updating user profile."""
    
    username = fields.Str(
        required=False,
        validate=[
            validate.Length(min=3, max=80, error='Username must be between 3 and 80 characters'),
            validate.Regexp(
                r'^[a-zA-Z0-9_]+$',
                error='Username can only contain letters, numbers, and underscores'
            )
        ]
    )
    first_name = fields.Str(
        required=False,
        validate=validate.Length(max=50, error='First name must be less than 50 characters')
    )
    last_name = fields.Str(
        required=False,
        validate=validate.Length(max=50, error='Last name must be less than 50 characters')
    )


class UserResponseSchema(Schema):
    """Schema for user response."""
    
    id = fields.Str(dump_only=True)
    email = fields.Email(dump_only=True)
    username = fields.Str(dump_only=True)
    first_name = fields.Str(dump_only=True)
    last_name = fields.Str(dump_only=True)
    is_active = fields.Bool(dump_only=True)
    is_verified = fields.Bool(dump_only=True)
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)
    last_login = fields.DateTime(dump_only=True)


class ChangePasswordSchema(Schema):
    """Schema for changing password."""
    
    current_password = fields.Str(
        required=True,
        error_messages={'required': 'Current password is required'},
        load_only=True
    )
    new_password = fields.Str(
        required=True,
        validate=validate.Length(min=8, error='New password must be at least 8 characters long'),
        error_messages={'required': 'New password is required'},
        load_only=True
    )
    
    @validates('new_password')
    def validate_new_password(self, value):
        """Validate new password strength."""
        if not re.search(r'[A-Z]', value):
            raise ValidationError('Password must contain at least one uppercase letter')
        if not re.search(r'[a-z]', value):
            raise ValidationError('Password must contain at least one lowercase letter')
        if not re.search(r'[0-9]', value):
            raise ValidationError('Password must contain at least one number')
        
