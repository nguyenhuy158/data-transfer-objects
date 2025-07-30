from flask import Blueprint, request, jsonify
from app.services import UserService, PostService

api = Blueprint('api', __name__, url_prefix='/api')

def create_response(success=True, data=None, message=None, status_code=200):
    """Helper function to create consistent API responses"""
    response = {
        'success': success,
        'data': data,
        'message': message
    }
    return jsonify(response), status_code

# User Routes
@api.route('/users', methods=['POST'])
def create_user():
    """Create a new user"""
    data = request.get_json()
    if not data:
        return create_response(False, None, 'No data provided', 400)
    
    user_data, error = UserService.create_user(data)
    if error:
        return create_response(False, None, error, 400)
    
    return create_response(True, user_data, 'User created successfully', 201)

@api.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    """Get user by ID"""
    user_data, error = UserService.get_user_by_id(user_id)
    if error:
        return create_response(False, None, error, 404)
    
    return create_response(True, user_data, 'User retrieved successfully')

@api.route('/users', methods=['GET'])
def get_all_users():
    """Get all users"""
    users_data, error = UserService.get_all_users()
    if error:
        return create_response(False, None, error, 500)
    
    return create_response(True, users_data, 'Users retrieved successfully')

@api.route('/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    """Update user"""
    data = request.get_json()
    if not data:
        return create_response(False, None, 'No data provided', 400)
    
    user_data, error = UserService.update_user(user_id, data)
    if error:
        return create_response(False, None, error, 400)
    
    return create_response(True, user_data, 'User updated successfully')

@api.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    """Delete user"""
    success, error = UserService.delete_user(user_id)
    if not success:
        return create_response(False, None, error, 404)
    
    return create_response(True, None, 'User deleted successfully')

@api.route('/auth/login', methods=['POST'])
def login():
    """Authenticate user"""
    data = request.get_json()
    if not data or 'username' not in data or 'password' not in data:
        return create_response(False, None, 'Username and password required', 400)
    
    user_data, error = UserService.authenticate_user(data['username'], data['password'])
    if error:
        return create_response(False, None, error, 401)
    
    return create_response(True, user_data, 'Login successful')

# Post Routes
@api.route('/users/<int:user_id>/posts', methods=['POST'])
def create_post(user_id):
    """Create a new post for a user"""
    data = request.get_json()
    if not data:
        return create_response(False, None, 'No data provided', 400)
    
    post_data, error = PostService.create_post(user_id, data)
    if error:
        return create_response(False, None, error, 400)
    
    return create_response(True, post_data, 'Post created successfully', 201)

@api.route('/posts/<int:post_id>', methods=['GET'])
def get_post(post_id):
    """Get post by ID"""
    post_data, error = PostService.get_post_by_id(post_id)
    if error:
        return create_response(False, None, error, 404)
    
    return create_response(True, post_data, 'Post retrieved successfully')

@api.route('/posts', methods=['GET'])
def get_all_posts():
    """Get all posts"""
    published_only = request.args.get('published', 'false').lower() == 'true'
    posts_data, error = PostService.get_all_posts(published_only)
    if error:
        return create_response(False, None, error, 500)
    
    return create_response(True, posts_data, 'Posts retrieved successfully')

@api.route('/users/<int:user_id>/posts', methods=['GET'])
def get_posts_by_user(user_id):
    """Get all posts by a specific user"""
    posts_data, error = PostService.get_posts_by_user(user_id)
    if error:
        return create_response(False, None, error, 404)
    
    return create_response(True, posts_data, 'User posts retrieved successfully')

@api.route('/posts/<int:post_id>/user/<int:user_id>', methods=['PUT'])
def update_post(post_id, user_id):
    """Update post (only by author)"""
    data = request.get_json()
    if not data:
        return create_response(False, None, 'No data provided', 400)
    
    post_data, error = PostService.update_post(post_id, user_id, data)
    if error:
        return create_response(False, None, error, 400)
    
    return create_response(True, post_data, 'Post updated successfully')

@api.route('/posts/<int:post_id>/user/<int:user_id>', methods=['DELETE'])
def delete_post(post_id, user_id):
    """Delete post (only by author)"""
    success, error = PostService.delete_post(post_id, user_id)
    if not success:
        return create_response(False, None, error, 404)
    
    return create_response(True, None, 'Post deleted successfully')

# Health check endpoint
@api.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return create_response(True, {'status': 'healthy'}, 'API is running')
