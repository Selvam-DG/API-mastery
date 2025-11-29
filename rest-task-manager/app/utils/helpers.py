from flask import jsonify, request, url_for


def create_response(data=None, message=None, status=200):
    """
    Create a standardized JSON response.
    
    Args:
        data: Response data
        message: Response message
        status: HTTP status code
    
    Returns:
        Flask JSON response
    """
    response = {}
    
    if message:
        response['message'] = message
    
    if data is not None:
        response['data'] = data
    
    return jsonify(response), status


def create_error_response(error, message, status=400, details=None):
    """
    Create a standardized error response.
    
    Args:
        error: Error type/title
        message: Error message
        status: HTTP status code
        details: Additional error details
    
    Returns:
        Flask JSON response
    """
    response = {
        'error': error,
        'message': message
    }
    
    if details:
        response['details'] = details
    
    return jsonify(response), status


def paginate_results(query, page, per_page, endpoint=None, **kwargs):
    """
    Paginate query results and create response with pagination metadata.
    
    Args:
        query: SQLAlchemy query object
        page: Current page number
        per_page: Items per page
        endpoint: Flask endpoint for generating pagination links
        **kwargs: Additional URL parameters
    
    Returns:
        Dictionary with results and pagination metadata
    """
    pagination = query.paginate(
        page=page,
        per_page=per_page,
        error_out=False
    )
    
    # Build pagination metadata
    meta = {
        'page': pagination.page,
        'per_page': pagination.per_page,
        'total_pages': pagination.pages,
        'total_items': pagination.total,
        'has_next': pagination.has_next,
        'has_prev': pagination.has_prev
    }
    
    # Add pagination links if endpoint provided
    if endpoint:
        base_url = request.base_url.split('?')[0]
        
        if pagination.has_next:
            meta['next_page'] = f"{base_url}?page={pagination.next_num}&per_page={per_page}"
        
        if pagination.has_prev:
            meta['prev_page'] = f"{base_url}?page={pagination.prev_num}&per_page={per_page}"
    
    return {
        'items': pagination.items,
        'meta': meta
    }


def get_pagination_params():
    """
    Get pagination parameters from request query string.
    
    Returns:
        Tuple of (page, per_page)
    """
    try:
        page = int(request.args.get('page', 1))
        per_page = int(request.args.get('per_page', 20))
        
        # Ensure valid values
        page = max(1, page)
        per_page = min(max(1, per_page), 100)  # Max 100 items per page
        
        return page, per_page
    except (ValueError, TypeError):
        return 1, 20


def extract_filters_from_request():
    """
    Extract filter parameters from request query string.
    
    Returns:
        Dictionary of filter parameters
    """
    filters = {}
    
    # Common filter parameters
    valid_filters = ['status', 'priority', 'project_id', 'overdue', 'search']
    
    for key in valid_filters:
        value = request.args.get(key)
        if value is not None:
            # Convert boolean strings
            if value.lower() in ['true', 'false']:
                filters[key] = value.lower() == 'true'
            else:
                filters[key] = value
    
    return filters


def serialize_model(model, schema_class):
    """
    Serialize a SQLAlchemy model using a Marshmallow schema.
    
    Args:
        model: SQLAlchemy model instance
        schema_class: Marshmallow schema class
    
    Returns:
        Serialized dictionary
    """
    schema = schema_class()
    return schema.dump(model)


def serialize_model_list(models, schema_class):
    """
    Serialize a list of SQLAlchemy models using a Marshmallow schema.
    
    Args:
        models: List of SQLAlchemy model instances
        schema_class: Marshmallow schema class
    
    Returns:
        List of serialized dictionaries
    """
    schema = schema_class(many=True)
    return schema.dump(models)