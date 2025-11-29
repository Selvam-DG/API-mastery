from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from app.models.task import Task, TaskStatus, TaskPriority
from app.models.project import Project
from app.schemas.task import TaskCreateSchema, TaskUpdateSchema, TaskStatusUpdateSchema, TaskFilterSchema
from app.utils.decorators import validate_request, validate_query_params, owner_required
from app.utils.helpers import create_response, create_error_response, get_pagination_params

# Create blueprint
tasks_bp = Blueprint('tasks', __name__)


@tasks_bp.route('', methods=['GET'])
@jwt_required()
@validate_query_params(TaskFilterSchema)
def get_tasks(filters):
    """
    Get all tasks for the current user with optional filters.
    
    Headers:
        Authorization: Bearer <access_token>
    
    Query Parameters:
        status: Filter by status (pending, in_progress, completed, archived)
        priority: Filter by priority (low, medium, high, urgent)
        project_id: Filter by project ID
        overdue: Filter overdue tasks (true/false)
        page: Page number (default: 1)
        per_page: Items per page (default: 20, max: 100)
    
    Returns:
        200: List of tasks with pagination
    """
    try:
        current_user_id = get_jwt_identity()
        
        # Get pagination parameters from filters
        page = filters.get('page', 1)
        per_page = filters.get('per_page', 20)
        
        # Remove pagination from filters
        query_filters = {k: v for k, v in filters.items() if k not in ['page', 'per_page']}
        
        # Get paginated tasks
        pagination = Task.find_by_user(
            current_user_id,
            filters=query_filters,
            page=page,
            per_page=per_page
        )
        
        # Serialize tasks
        tasks_data = [task.to_dict(include_project=True) for task in pagination.items]
        
        # Build response with pagination metadata
        response_data = {
            'tasks': tasks_data,
            'pagination': {
                'page': pagination.page,
                'per_page': pagination.per_page,
                'total_pages': pagination.pages,
                'total_items': pagination.total,
                'has_next': pagination.has_next,
                'has_prev': pagination.has_prev
            }
        }
        
        return create_response(
            data=response_data,
            status=200
        )
        
    except Exception as e:
        return create_error_response(
            'Internal Server Error',
            str(e),
            500
        )


@tasks_bp.route('', methods=['POST'])
@jwt_required()
@validate_request(TaskCreateSchema)
def create_task(validated_data):
    """
    Create a new task.
    
    Headers:
        Authorization: Bearer <access_token>
    
    Request Body:
        title: Task title (required)
        description: Task description (optional)
        status: Task status (optional, default: pending)
        priority: Task priority (optional, default: medium)
        due_date: Due date in YYYY-MM-DD format (optional)
        project_id: Project ID (required)
    
    Returns:
        201: Task created successfully
        400: Invalid request data
        403: Not authorized to add task to this project
        404: Project not found
    """
    try:
        current_user_id = get_jwt_identity()
        
        # Verify project exists and belongs to user
        project = Project.find_user_project(
            validated_data['project_id'],
            current_user_id
        )
        
        if not project:
            return create_error_response(
                'Not Found',
                'Project not found or you do not have permission to access it',
                404
            )
        
        # Create task
        task = Task(
            title=validated_data['title'],
            user_id=current_user_id,
            project_id=validated_data['project_id'],
            description=validated_data.get('description'),
            status=TaskStatus(validated_data.get('status', 'pending')),
            priority=TaskPriority(validated_data.get('priority', 'medium')),
            due_date=validated_data.get('due_date')
        )
        
        db.session.add(task)
        db.session.commit()
        
        # Serialize task data
        task_data = task.to_dict(include_project=True)
        
        return create_response(
            data=task_data,
            message='Task created successfully',
            status=201
        )
        
    except Exception as e:
        db.session.rollback()
        return create_error_response(
            'Internal Server Error',
            str(e),
            500
        )


@tasks_bp.route('/<string:id>', methods=['GET'])
@jwt_required()
@owner_required(Task, 'id')
def get_task(id, resource):
    """
    Get a specific task by ID.
    
    Headers:
        Authorization: Bearer <access_token>
    
    URL Parameters:
        id: Task ID
    
    Returns:
        200: Task details
        403: Not authorized to access this task
        404: Task not found
    """
    try:
        task = resource
        task_data = task.to_dict(include_project=True)
        
        return create_response(
            data=task_data,
            status=200
        )
        
    except Exception as e:
        return create_error_response(
            'Internal Server Error',
            str(e),
            500
        )


@tasks_bp.route('/<string:id>', methods=['PUT'])
@jwt_required()
@owner_required(Task, 'id')
@validate_request(TaskUpdateSchema)
def update_task(id, resource, validated_data):
    """
    Update a task.
    
    Headers:
        Authorization: Bearer <access_token>
    
    URL Parameters:
        id: Task ID
    
    Request Body:
        title: Task title (optional)
        description: Task description (optional)
        status: Task status (optional)
        priority: Task priority (optional)
        due_date: Due date (optional, null to remove)
        project_id: Project ID (optional)
    
    Returns:
        200: Task updated successfully
        403: Not authorized to update this task
        404: Task or project not found
    """
    try:
        current_user_id = get_jwt_identity()
        task = resource
        
        # If changing project, verify new project belongs to user
        if 'project_id' in validated_data:
            new_project = Project.find_user_project(
                validated_data['project_id'],
                current_user_id
            )
            
            if not new_project:
                return create_error_response(
                    'Not Found',
                    'Project not found or you do not have permission to access it',
                    404
                )
            
            task.project_id = validated_data['project_id']
        
        # Update other fields
        if 'title' in validated_data:
            task.title = validated_data['title']
        
        if 'description' in validated_data:
            task.description = validated_data['description']
        
        if 'status' in validated_data:
            task.update_status(validated_data['status'])
        
        if 'priority' in validated_data:
            task.priority = TaskPriority(validated_data['priority'])
        
        if 'due_date' in validated_data:
            task.due_date = validated_data['due_date']
        
        db.session.commit()
        
        # Serialize updated task
        task_data = task.to_dict(include_project=True)
        
        return create_response(
            data=task_data,
            message='Task updated successfully',
            status=200
        )
        
    except Exception as e:
        db.session.rollback()
        return create_error_response(
            'Internal Server Error',
            str(e),
            500
        )


@tasks_bp.route('/<string:id>/status', methods=['PATCH'])
@jwt_required()
@owner_required(Task, 'id')
@validate_request(TaskStatusUpdateSchema)
def update_task_status(id, resource, validated_data):
    """
    Update only the task status.
    
    Headers:
        Authorization: Bearer <access_token>
    
    URL Parameters:
        id: Task ID
    
    Request Body:
        status: New task status (required)
    
    Returns:
        200: Task status updated successfully
        403: Not authorized to update this task
        404: Task not found
    """
    try:
        task = resource
        task.update_status(validated_data['status'])
        
        task_data = task.to_dict(include_project=True)
        
        return create_response(
            data=task_data,
            message='Task status updated successfully',
            status=200
        )
        
    except Exception as e:
        db.session.rollback()
        return create_error_response(
            'Internal Server Error',
            str(e),
            500
        )


@tasks_bp.route('/<string:id>', methods=['DELETE'])
@jwt_required()
@owner_required(Task, 'id')
def delete_task(id, resource):
    """
    Delete a task.
    
    Headers:
        Authorization: Bearer <access_token>
    
    URL Parameters:
        id: Task ID
    
    Returns:
        200: Task deleted successfully
        403: Not authorized to delete this task
        404: Task not found
    """
    try:
        task = resource
        
        db.session.delete(task)
        db.session.commit()
        
        return create_response(
            message='Task deleted successfully',
            status=200
        )
        
    except Exception as e:
        db.session.rollback()
        return create_error_response(
            'Internal Server Error',
            str(e),
            500
        )


@tasks_bp.route('/project/<string:project_id>', methods=['GET'])
@jwt_required()
def get_project_tasks(project_id):
    """
    Get all tasks for a specific project.
    
    Headers:
        Authorization: Bearer <access_token>
    
    URL Parameters:
        project_id: Project ID
    
    Query Parameters:
        page: Page number (default: 1)
        per_page: Items per page (default: 20)
    
    Returns:
        200: List of project tasks
        403: Not authorized to access this project
        404: Project not found
    """
    try:
        current_user_id = get_jwt_identity()
        
        # Verify project exists and belongs to user
        project = Project.find_user_project(project_id, current_user_id)
        
        if not project:
            return create_error_response(
                'Not Found',
                'Project not found or you do not have permission to access it',
                404
            )
        
        # Get pagination parameters
        page, per_page = get_pagination_params()
        
        # Get paginated tasks
        pagination = Task.find_by_project(
            project_id,
            current_user_id,
            page=page,
            per_page=per_page
        )
        
        # Serialize tasks
        tasks_data = [task.to_dict() for task in pagination.items]
        
        # Build response
        response_data = {
            'tasks': tasks_data,
            'project': {
                'id': project.id,
                'name': project.name,
                'color': project.color
            },
            'pagination': {
                'page': pagination.page,
                'per_page': pagination.per_page,
                'total_pages': pagination.pages,
                'total_items': pagination.total,
                'has_next': pagination.has_next,
                'has_prev': pagination.has_prev
            }
        }
        
        return create_response(
            data=response_data,
            status=200
        )
        
    except Exception as e:
        return create_error_response(
            'Internal Server Error',
            str(e),
            500
        )