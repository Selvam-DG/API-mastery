from flask import Blueprint, jsonify
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    jwt_required,
    get_jwt_identity,
    get_jwt
)
from sqlalchemy.exc import IntegrityError

from app import db, limiter
from app.models.user import User
from app.schemas.user import (
    UserRegistrationSchema,
    UserLoginSchema,
    UserResponseSchema,
    UserUpdateSchema,
    ChangePasswordSchema
)
from app.utils.decorators import validate_request
from app.utils.helpers import  create_response, create_error_response

# Create blueprint
auth_bp = Blueprint('auth', __name__)

# Token blacklist set (in production, use Redis)
token_blacklist = set()


@auth_bp.route('/register', methods=['POST'])
@limiter.limit("5 per minute")
@validate_request(UserRegistrationSchema)
def register(validated_data):
    """
    Register a new user.
    
    Request Body:
        email: User email address
        username: Unique username
        password: User password (min 8 chars, must contain uppercase, lowercase, number)
        first_name: Optional first name
        last_name: Optional last name
    
    Returns:
        201: User created successfully
        400: Invalid request data
        409: User already exists
    """
    try:
        # Check if user already exists
        existing_user = User.find_by_email(validated_data['email'])
        if existing_user:
            return create_error_response(
                'Conflict',
                'User with this email already exists',
                409
            )
        
        existing_user = User.find_by_username(validated_data['username'])
        if existing_user:
            return create_error_response(
                'Conflict',
                'Username already taken',
                409
            )
        
        # Create new user
        user = User(
            email=validated_data['email'],
            username=validated_data['username'],
            password=validated_data['password'],
            first_name=validated_data.get('first_name'),
            last_name=validated_data.get('last_name')
        )
        
        db.session.add(user)
        db.session.commit()
        
        # Serialize user data
        schema = UserResponseSchema()
        user_data = schema.dump(user)
        
        return create_response(
            data=user_data,
            message='User registered successfully',
            status=201
        )
        
    except IntegrityError:
        db.session.rollback()
        return create_error_response(
            'Conflict',
            'User with this email or username already exists',
            409
        )
    except Exception as e:
        db.session.rollback()
        return create_error_response(
            'Internal Server Error',
            str(e),
            500
        )


@auth_bp.route('/login', methods=['POST'])
@limiter.limit("10 per minute")
@validate_request(UserLoginSchema)
def login(validated_data):
    """
    Login user and return access and refresh tokens.
    
    Request Body:
        email: User email address
        password: User password
    
    Returns:
        200: Login successful with tokens
        401: Invalid credentials
    """
    try:
        # Find user by email
        user = User.find_by_email(validated_data['email'])
        
        if not user or not user.check_password(validated_data['password']):
            return create_error_response(
                'Unauthorized',
                'Invalid email or password',
                401
            )
        
        if not user.is_active:
            return create_error_response(
                'Forbidden',
                'Account is deactivated',
                403
            )
        
        # Update last login
        user.update_last_login()
        
        # Create tokens
        access_token = create_access_token(identity=user.id)
        refresh_token = create_refresh_token(identity=user.id)
        
        # Serialize user data
        schema = UserResponseSchema()
        user_data = schema.dump(user)
        
        return create_response(
            data={
                'user': user_data,
                'access_token': access_token,
                'refresh_token': refresh_token
            },
            message='Login successful',
            status=200
        )
        
    except Exception as e:
        return create_error_response(
            'Internal Server Error',
            str(e),
            500
        )


@auth_bp.route('/refresh', methods=['POST'])
@jwt_required(refresh=True)
def refresh():
    """
    Refresh access token using refresh token.
    
    Headers:
        Authorization: Bearer <refresh_token>
    
    Returns:
        200: New access token
        401: Invalid or expired refresh token
    """
    try:
        current_user_id = get_jwt_identity()
        new_access_token = create_access_token(identity=current_user_id)
        
        return create_response(
            data={'access_token': new_access_token},
            message='Token refreshed successfully',
            status=200
        )
        
    except Exception as e:
        return create_error_response(
            'Internal Server Error',
            str(e),
            500
        )


@auth_bp.route('/logout', methods=['POST'])
@jwt_required()
def logout():
    """
    Logout user by blacklisting the token.
    
    Headers:
        Authorization: Bearer <access_token>
    
    Returns:
        200: Logout successful
    """
    try:
        jti = get_jwt()['jti']
        token_blacklist.add(jti)
        
        return create_response(
            message='Logout successful',
            status=200
        )
        
    except Exception as e:
        return create_error_response(
            'Internal Server Error',
            str(e),
            500
        )


@auth_bp.route('/me', methods=['GET'])
@jwt_required()
def get_current_user():
    """
    Get current user information.
    
    Headers:
        Authorization: Bearer <access_token>
    
    Returns:
        200: Current user data
        404: User not found
    """
    try:
        current_user_id = get_jwt_identity()
        user = User.find_by_id(current_user_id)
        
        if not user:
            return create_error_response(
                'Not Found',
                'User not found',
                404
            )
        
        schema = UserResponseSchema()
        user_data = schema.dump(user)
        
        return create_response(
            data=user_data,
            status=200
        )
        
    except Exception as e:
        return create_error_response(
            'Internal Server Error',
            str(e),
            500
        )


@auth_bp.route('/me', methods=['PUT'])
@jwt_required()
@validate_request(UserUpdateSchema)
def update_current_user(validated_data):
    """
    Update current user profile.
    
    Headers:
        Authorization: Bearer <access_token>
    
    Request Body:
        username: New username (optional)
        first_name: New first name (optional)
        last_name: New last name (optional)
    
    Returns:
        200: User updated successfully
        404: User not found
        409: Username already taken
    """
    try:
        current_user_id = get_jwt_identity()
        user = User.find_by_id(current_user_id)
        
        if not user:
            return create_error_response(
                'Not Found',
                'User not found',
                404
            )
        
        # Check if username is being changed and is available
        if 'username' in validated_data and validated_data['username'] != user.username:
            existing_user = User.find_by_username(validated_data['username'])
            if existing_user:
                return create_error_response(
                    'Conflict',
                    'Username already taken',
                    409
                )
            user.username = validated_data['username']
        
        # Update other fields
        if 'first_name' in validated_data:
            user.first_name = validated_data['first_name']
        if 'last_name' in validated_data:
            user.last_name = validated_data['last_name']
        
        db.session.commit()
        
        schema = UserResponseSchema()
        user_data = schema.dump(user)
        
        return create_response(
            data=user_data,
            message='Profile updated successfully',
            status=200
        )
        
    except Exception as e:
        db.session.rollback()
        return create_error_response(
            'Internal Server Error',
            str(e),
            500
        )


@auth_bp.route('/change-password', methods=['POST'])
@jwt_required()
@validate_request(ChangePasswordSchema)
def change_password(validated_data):
    """
    Change user password.
    
    Headers:
        Authorization: Bearer <access_token>
    
    Request Body:
        current_password: Current password
        new_password: New password
    
    Returns:
        200: Password changed successfully
        401: Invalid current password
        404: User not found
    """
    try:
        current_user_id = get_jwt_identity()
        user = User.find_by_id(current_user_id)
        
        if not user:
            return create_error_response(
                'Not Found',
                'User not found',
                404
            )
        
        # Verify current password
        if not user.check_password(validated_data['current_password']):
            return create_error_response(
                'Unauthorized',
                'Invalid current password',
                401
            )
        
        # Update password
        user.set_password(validated_data['new_password'])
        db.session.commit()
        
        return create_response(
            message='Password changed successfully',
            status=200
        )
        
    except Exception as e:
        db.session.rollback()
        return create_error_response(
            'Internal Server Error',
            str(e),
            500
        )


# JWT token check callback
@auth_bp.before_app_request
def check_if_token_revoked():
    """Check if token is in blacklist."""
    try:
        if jwt_required(optional=True):
            jti = get_jwt().get('jti')
            if jti in token_blacklist:
                return create_error_response(
                    'Token Revoked',
                    'The token has been revoked',
                    401
                )
    except:
        pass