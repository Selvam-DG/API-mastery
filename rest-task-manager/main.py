#!/usr/bin/env python
"""
Application entry point.
Run this file to start the Flask development server.
"""

import os
from app import create_app, db
from app.models.project import Project
from app.models.user import User 
from app.models.task import Task

# Create Flask application
app = create_app()


@app.shell_context_processor
def make_shell_context():
    """
    Create shell context for Flask shell command.
    Makes models available in Flask shell.
    """
    return {
        'db': db,
        'User': User,
        'Project': Project,
        'Task': Task
    }


@app.cli.command()
def init_db():
    """Initialize the database."""
    db.create_all()
    print('Database initialized successfully!')


@app.cli.command()
def drop_db():
    """Drop all database tables."""
    if input('Are you sure you want to drop all tables? (yes/no): ').lower() == 'yes':
        db.drop_all()
        print('Database tables dropped successfully!')
    else:
        print('Operation cancelled.')


@app.cli.command()
def seed_db():
    """Seed database with sample data for testing."""
    from datetime import datetime, timedelta
    from app.models.task import TaskStatus, TaskPriority
    
    print('Seeding database...')
    
    # Create sample user
    user = User(
        email='demo@example.com',
        username='demouser',
        password='Demo123!',
        first_name='Demo',
        last_name='User'
    )
    db.session.add(user)
    db.session.flush()  # Flush to get user.id
    
    # Create sample projects
    project1 = Project(
        name='Website Redesign',
        description='Complete overhaul of company website',
        color='#3B82F6',
        user_id=user.id
    )
    
    project2 = Project(
        name='Mobile App Development',
        description='Build iOS and Android apps',
        color='#10B981',
        user_id=user.id
    )
    
    db.session.add_all([project1, project2])
    db.session.flush()
    
    # Create sample tasks
    tasks = [
        Task(
            title='Design homepage mockup',
            description='Create initial design concepts for the new homepage',
            status=TaskStatus.IN_PROGRESS,
            priority=TaskPriority.HIGH,
            due_date=(datetime.utcnow() + timedelta(days=7)).date(),
            project_id=project1.id,
            user_id=user.id
        ),
        Task(
            title='Set up development environment',
            description='Configure local dev environment with all necessary tools',
            status=TaskStatus.COMPLETED,
            priority=TaskPriority.MEDIUM,
            project_id=project1.id,
            user_id=user.id
        ),
        Task(
            title='Research UI frameworks',
            description='Compare React, Vue, and Angular for the project',
            status=TaskStatus.PENDING,
            priority=TaskPriority.LOW,
            due_date=(datetime.utcnow() + timedelta(days=14)).date(),
            project_id=project2.id,
            user_id=user.id
        ),
        Task(
            title='Create database schema',
            description='Design and implement the database structure',
            status=TaskStatus.IN_PROGRESS,
            priority=TaskPriority.URGENT,
            due_date=(datetime.utcnow() + timedelta(days=3)).date(),
            project_id=project2.id,
            user_id=user.id
        )
    ]
    
    db.session.add_all(tasks)
    db.session.commit()
    
    print('Database seeded successfully!')
    print(f'\nDemo User Credentials:')
    print(f'Email: demo@example.com')
    print(f'Password: Demo123!')


if __name__ == '__main__':
    # Get configuration from environment
    host = os.getenv('HOST', '0.0.0.0')
    port = int(os.getenv('PORT', 5000))
    debug = os.getenv('FLASK_DEBUG', 'True').lower() == 'true'
    
    # Run the application
    app.run(host=host, port=port, debug=debug)