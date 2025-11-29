from functools import wraps
from flask import request, jsonify
from flask_jwt_extended import get_jwt_identity
from marshmallow import ValidationError


def validate_request(schema):
    """
    Decorator to validate request data using Marshmallow schema.
    
    Args:
        schema: Marshmallow schema class to validate against
    
    Returns:
        Decorated function with validated data
    """
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            try:
                # Get request data
                data = request.get_json()
                
                if data is None:
                    return jsonify({
                        'error': 'Bad Request',
                        'message': 'Request body must be JSON'
                    }), 400
                
                # Validate data
                schema_instance = schema()
                validated_data = schema_instance.load(data)
                
                # Add validated data to kwargs
                kwargs['validated_data'] = validated_data
                
                return f(*args, **kwargs)
                
            except ValidationError as err:
                return jsonify({
                    'error': 'Validation Error',
                    'message': 'Invalid request data',
                    'details': err.messages
                }), 422
            except Exception as e:
                return jsonify({
                    'error': 'Bad Request',
                    'message': str(e)
                }), 400
        
        return decorated_function
    return decorator


def validate_query_params(schema):
    """
    Decorator to validate query parameters using Marshmallow schema.
    
    Args:
        schema: Marshmallow schema class to validate against
    
    Returns:
        Decorated function with validated query parameters
    """
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            try:
                # Get query parameters
                params = request.args.to_dict()
                
                # Validate parameters
                schema_instance = schema()
                validated_params = schema_instance.load(params)
                
                # Add validated params to kwargs
                kwargs['filters'] = validated_params
                
                return f(*args, **kwargs)
                
            except ValidationError as err:
                return jsonify({
                    'error': 'Validation Error',
                    'message': 'Invalid query parameters',
                    'details': err.messages
                }), 422
            except Exception as e:
                return jsonify({
                    'error': 'Bad Request',
                    'message': str(e)
                }), 400
        
        return decorated_function
    return decorator


def owner_required(model_class, id_param='id'):
    """
    Decorator to verify that the current user owns the requested resource.
    
    Args:
        model_class: SQLAlchemy model class
        id_param: Name of the URL parameter containing the resource ID
    
    Returns:
        Decorated function with resource ownership verification
    """
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            try:
                # Get current user ID from JWT
                current_user_id = get_jwt_identity()
                
                # Get resource ID from URL parameters
                resource_id = kwargs.get(id_param)
                
                if not resource_id:
                    return jsonify({
                        'error': 'Bad Request',
                        'message': 'Resource ID is required'
                    }), 400
                
                # Find resource
                resource = model_class.query.get(resource_id)
                
                if not resource:
                    return jsonify({
                        'error': 'Not Found',
                        'message': f'{model_class.__name__} not found'
                    }), 404
                
                # Verify ownership
                if resource.user_id != current_user_id:
                    return jsonify({
                        'error': 'Forbidden',
                        'message': 'You do not have permission to access this resource'
                    }), 403
                
                # Add resource to kwargs
                kwargs['resource'] = resource
                
                return f(*args, **kwargs)
                
            except Exception as e:
                return jsonify({
                    'error': 'Internal Server Error',
                    'message': str(e)
                }), 500
        
        return decorated_function
    return decorator