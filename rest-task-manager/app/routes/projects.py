from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity

from app import db
from app.models.project import Project
from app.schemas.project import (
    ProjectCreateSchema,
    ProjectUpdateSchema,
    ProjectResponseSchema,
    ProjectListResponseSchema
)
from app.utils.decorators import validate_request, owner_required
from app.utils.helpers import create_error_response, create_response


# Create blueprint
projects_bp = Blueprint('projects', __name__)


@projects_bp.route('', methods=['GET'])
@jwt_required()
def get_projects():
    """
    Get all projects for the current user.
    
    Query Parameters:
        include_archived: Include archived projects (default: false)
        include_stats: Include project statistics (default: false)
    
    Headers:
        Authorization: Bearer <access_token>
    
    Returns:
        200: List of projects
    """
    try:
        current_user_id = get_jwt_identity()
        
        # Get query parameters
        include_archived = request.args.get('include_archived', 'false').lower() == 'true'
        include_stats = request.args.get('include_stats', 'false').lower() == 'true'
        
        # Get user's projects
        projects = Project.find_by_user(current_user_id, include_archived)
        
        # Serialize projects
        projects_data = [
            project.to_dict(include_stats=include_stats) 
            for project in projects
        ]
        
        return create_response(
            data=projects_data,
            status=200
        )
        
    except Exception as e:
        return create_error_response(
            'Internal Server Error',
            str(e),
            500
        )


@projects_bp.route('', methods=['POST'])
@jwt_required()
@validate_request(ProjectCreateSchema)
def create_project(validated_data):
    """
    Create a new project.
    
    Headers:
        Authorization: Bearer <access_token>
    
    Request Body:
        name: Project name (required)
        description: Project description (optional)
        color: Hex color code (optional, default: #3B82F6)
    
    Returns:
        201: Project created successfully
        400: Invalid request data
    """
    try:
        current_user_id = get_jwt_identity()
        
        # Create new project
        project = Project(
            name=validated_data['name'],
            user_id=current_user_id,
            description=validated_data.get('description'),
            color=validated_data.get('color')
        )
        
        db.session.add(project)
        db.session.commit()
        
        # Serialize project data
        project_data = project.to_dict(include_stats=True)
        
        return create_response(
            data=project_data,
            message='Project created successfully',
            status=201
        )
        
    except Exception as e:
        db.session.rollback()
        return create_error_response(
            'Internal Server Error',
            str(e),
            500
        )


@projects_bp.route('/<string:id>', methods=['GET'])
@jwt_required()
@owner_required(Project, 'id')
def get_project(id, resource):
    """
    Get a specific project by ID.
    
    Headers:
        Authorization: Bearer <access_token>
    
    URL Parameters:
        id: Project ID
    
    Query Parameters:
        include_tasks: Include project tasks (default: false)
        include_stats: Include project statistics (default: true)
    
    Returns:
        200: Project details
        403: Not authorized to access this project
        404: Project not found
    """
    try:
        # Get query parameters
        include_tasks = request.args.get('include_tasks', 'false').lower() == 'true'
        include_stats = request.args.get('include_stats', 'true').lower() == 'true'
        
        # Serialize project data
        project_data = resource.to_dict(
            include_tasks=include_tasks,
            include_stats=include_stats
        )
        
        return create_response(
            data=project_data,
            status=200
        )
        
    except Exception as e:
        return create_error_response(
            'Internal Server Error',
            str(e),
            500
        )


@projects_bp.route('/<string:id>', methods=['PUT'])
@jwt_required()
@owner_required(Project, 'id')
@validate_request(ProjectUpdateSchema)
def update_project(id, resource, validated_data):
    """
    Update a project.
    
    Headers:
        Authorization: Bearer <access_token>
    
    URL Parameters:
        id: Project ID
    
    Request Body:
        name: Project name (optional)
        description: Project description (optional)
        color: Hex color code (optional)
        is_active: Project active status (optional)
    
    Returns:
        200: Project updated successfully
        403: Not authorized to update this project
        404: Project not found
    """
    try:
        project = resource
        
        # Update fields if provided
        if 'name' in validated_data:
            project.name = validated_data['name']
        
        if 'description' in validated_data:
            project.description = validated_data['description']
        
        if 'color' in validated_data:
            project.color = validated_data['color']
        
        if 'is_active' in validated_data:
            project.is_active = validated_data['is_active']
        
        db.session.commit()
        
        # Serialize updated project
        project_data = project.to_dict(include_stats=True)
        
        return create_response(
            data=project_data,
            message='Project updated successfully',
            status=200
        )
        
    except Exception as e:
        db.session.rollback()
        return create_error_response(
            'Internal Server Error',
            str(e),
            500
        )


@projects_bp.route('/<string:id>', methods=['DELETE'])
@jwt_required()
@owner_required(Project, 'id')
def delete_project(id, resource):
    """
    Delete a project and all its tasks.
    
    Headers:
        Authorization: Bearer <access_token>
    
    URL Parameters:
        id: Project ID
    
    Returns:
        200: Project deleted successfully
        403: Not authorized to delete this project
        404: Project not found
    """
    try:
        project = resource
        
        db.session.delete(project)
        db.session.commit()
        
        return create_response(
            message='Project deleted successfully',
            status=200
        )
        
    except Exception as e:
        db.session.rollback()
        return create_error_response(
            'Internal Server Error',
            str(e),
            500
        )


@projects_bp.route('/<string:id>/archive', methods=['POST'])
@jwt_required()
@owner_required(Project, 'id')
def archive_project(id, resource):
    """
    Archive a project.
    
    Headers:
        Authorization: Bearer <access_token>
    
    URL Parameters:
        id: Project ID
    
    Returns:
        200: Project archived successfully
        403: Not authorized to archive this project
        404: Project not found
    """
    try:
        project = resource
        project.archive()
        
        project_data = project.to_dict()
        
        return create_response(
            data=project_data,
            message='Project archived successfully',
            status=200
        )
        
    except Exception as e:
        db.session.rollback()
        return create_error_response(
            'Internal Server Error',
            str(e),
            500
        )


@projects_bp.route('/<string:id>/unarchive', methods=['POST'])
@jwt_required()
@owner_required(Project, 'id')
def unarchive_project(id, resource):
    """
    Unarchive a project.
    
    Headers:
        Authorization: Bearer <access_token>
    
    URL Parameters:
        id: Project ID
    
    Returns:
        200: Project unarchived successfully
        403: Not authorized to unarchive this project
        404: Project not found
    """
    try:
        project = resource
        project.unarchive()
        
        project_data = project.to_dict()
        
        return create_response(
            data=project_data,
            message='Project unarchived successfully',
            status=200
        )
        
    except Exception as e:
        db.session.rollback()
        return create_error_response(
            'Internal Server Error',
            str(e),
            500
        )