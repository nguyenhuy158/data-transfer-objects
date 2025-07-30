from werkzeug.security import generate_password_hash, check_password_hash
from app.models import db, User, Post
from app.dto import (
    user_create_schema, user_update_schema, user_response_schema,
    user_list_response_schema, user_single_list_response_schema,
    post_create_schema, post_update_schema, post_response_schema,
    post_list_response_schema, post_single_list_response_schema
)
from marshmallow import ValidationError
from sqlalchemy.exc import IntegrityError

class UserService:
    @staticmethod
    def create_user(data):
        """Create a new user using DTO"""
        try:
            # Validate input data using DTO
            validated_data = user_create_schema.load(data)
            
            # Hash password
            validated_data['password_hash'] = generate_password_hash(validated_data.pop('password'))
            
            # Create user entity
            user = User(**validated_data)
            db.session.add(user)
            db.session.commit()
            
            # Return response DTO
            return user_response_schema.dump(user), None
        except ValidationError as e:
            return None, {'validation_errors': e.messages}
        except IntegrityError as e:
            db.session.rollback()
            return None, {'error': 'Username or email already exists'}
        except Exception as e:
            db.session.rollback()
            return None, {'error': str(e)}
    
    @staticmethod
    def get_user_by_id(user_id):
        """Get user by ID and return DTO response"""
        user = User.query.get(user_id)
        if not user:
            return None, {'error': 'User not found'}
        
        # Add posts count
        user_data = user_response_schema.dump(user)
        user_data['posts_count'] = len(user.posts)
        
        return user_data, None
    
    @staticmethod
    def get_all_users():
        """Get all users with minimal information"""
        users = User.query.all()
        users_data = []
        
        for user in users:
            user_data = user_single_list_response_schema.dump(user)
            user_data['posts_count'] = len(user.posts)
            users_data.append(user_data)
        
        return users_data, None
    
    @staticmethod
    def update_user(user_id, data):
        """Update user using DTO"""
        try:
            user = User.query.get(user_id)
            if not user:
                return None, {'error': 'User not found'}
            
            # Validate update data using DTO
            validated_data = user_update_schema.load(data)
            
            # Update user fields
            for key, value in validated_data.items():
                if value is not None:
                    setattr(user, key, value)
            
            db.session.commit()
            
            # Return updated user DTO
            user_data = user_response_schema.dump(user)
            user_data['posts_count'] = len(user.posts)
            
            return user_data, None
        except ValidationError as e:
            return None, {'validation_errors': e.messages}
        except Exception as e:
            db.session.rollback()
            return None, {'error': str(e)}
    
    @staticmethod
    def delete_user(user_id):
        """Delete user"""
        user = User.query.get(user_id)
        if not user:
            return False, {'error': 'User not found'}
        
        try:
            db.session.delete(user)
            db.session.commit()
            return True, None
        except Exception as e:
            db.session.rollback()
            return False, {'error': str(e)}
    
    @staticmethod
    def authenticate_user(username, password):
        """Authenticate user for login"""
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password_hash, password):
            return user_response_schema.dump(user), None
        return None, {'error': 'Invalid credentials'}

class PostService:
    @staticmethod
    def create_post(user_id, data):
        """Create a new post using DTO"""
        try:
            # Check if user exists
            user = User.query.get(user_id)
            if not user:
                return None, {'error': 'User not found'}
            
            # Validate input data using DTO
            validated_data = post_create_schema.load(data)
            validated_data['user_id'] = user_id
            
            # Create post entity
            post = Post(**validated_data)
            db.session.add(post)
            db.session.commit()
            
            # Return response DTO with author info
            post_data = post_response_schema.dump(post)
            post_data['author'] = user_single_list_response_schema.dump(user)
            
            return post_data, None
        except ValidationError as e:
            return None, {'validation_errors': e.messages}
        except Exception as e:
            db.session.rollback()
            return None, {'error': str(e)}
    
    @staticmethod
    def get_post_by_id(post_id):
        """Get post by ID and increment view count"""
        post = Post.query.get(post_id)
        if not post:
            return None, {'error': 'Post not found'}
        
        # Increment view count
        post.view_count += 1
        db.session.commit()
        
        # Return response DTO with author info
        post_data = post_response_schema.dump(post)
        post_data['author'] = user_single_list_response_schema.dump(post.author)
        
        return post_data, None
    
    @staticmethod
    def get_all_posts(published_only=False):
        """Get all posts with minimal information"""
        query = Post.query
        if published_only:
            query = query.filter_by(is_published=True)
        
        posts = query.order_by(Post.created_at.desc()).all()
        posts_data = []
        
        for post in posts:
            post_data = post_single_list_response_schema.dump(post)
            post_data['author_name'] = post.author.full_name
            posts_data.append(post_data)
        
        return posts_data, None
    
    @staticmethod
    def get_posts_by_user(user_id):
        """Get all posts by a specific user"""
        user = User.query.get(user_id)
        if not user:
            return None, {'error': 'User not found'}
        
        posts = Post.query.filter_by(user_id=user_id).order_by(Post.created_at.desc()).all()
        posts_data = []
        
        for post in posts:
            post_data = post_single_list_response_schema.dump(post)
            post_data['author_name'] = user.full_name
            posts_data.append(post_data)
        
        return posts_data, None
    
    @staticmethod
    def update_post(post_id, user_id, data):
        """Update post using DTO (only by author)"""
        try:
            post = Post.query.get(post_id)
            if not post:
                return None, {'error': 'Post not found'}
            
            if post.user_id != user_id:
                return None, {'error': 'Not authorized to update this post'}
            
            # Validate update data using DTO
            validated_data = post_update_schema.load(data)
            
            # Update post fields
            for key, value in validated_data.items():
                if value is not None:
                    setattr(post, key, value)
            
            db.session.commit()
            
            # Return updated post DTO
            post_data = post_response_schema.dump(post)
            post_data['author'] = user_single_list_response_schema.dump(post.author)
            
            return post_data, None
        except ValidationError as e:
            return None, {'validation_errors': e.messages}
        except Exception as e:
            db.session.rollback()
            return None, {'error': str(e)}
    
    @staticmethod
    def delete_post(post_id, user_id):
        """Delete post (only by author)"""
        post = Post.query.get(post_id)
        if not post:
            return False, {'error': 'Post not found'}
        
        if post.user_id != user_id:
            return False, {'error': 'Not authorized to delete this post'}
        
        try:
            db.session.delete(post)
            db.session.commit()
            return True, None
        except Exception as e:
            db.session.rollback()
            return False, {'error': str(e)}
