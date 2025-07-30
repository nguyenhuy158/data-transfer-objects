from marshmallow import Schema, fields, post_load, validates, ValidationError
from datetime import datetime
import re

class UserCreateDTO(Schema):
    """DTO for creating a new user"""
    username = fields.Str(required=True, validate=lambda x: len(x) >= 3)
    email = fields.Email(required=True)
    password = fields.Str(required=True, validate=lambda x: len(x) >= 6)
    full_name = fields.Str(required=True)
    phone = fields.Str(allow_none=True)
    date_of_birth = fields.Date(allow_none=True)
    
    @validates('username')
    def validate_username(self, value):
        if not re.match(r'^[a-zA-Z0-9_]+$', value):
            raise ValidationError('Username can only contain letters, numbers, and underscores')

class UserUpdateDTO(Schema):
    """DTO for updating user information"""
    full_name = fields.Str(allow_none=True)
    phone = fields.Str(allow_none=True)
    date_of_birth = fields.Date(allow_none=True)
    is_active = fields.Bool(allow_none=True)

class UserResponseDTO(Schema):
    """DTO for user response (excludes sensitive information)"""
    id = fields.Int()
    username = fields.Str()
    email = fields.Str()
    full_name = fields.Str()
    phone = fields.Str()
    date_of_birth = fields.Date()
    is_active = fields.Bool()
    created_at = fields.DateTime()
    posts_count = fields.Int()

class UserListResponseDTO(Schema):
    """DTO for user list response (minimal information)"""
    id = fields.Int()
    username = fields.Str()
    full_name = fields.Str()
    is_active = fields.Bool()
    posts_count = fields.Int()

class PostCreateDTO(Schema):
    """DTO for creating a new post"""
    title = fields.Str(required=True, validate=lambda x: len(x.strip()) >= 5)
    content = fields.Str(required=True, validate=lambda x: len(x.strip()) >= 10)
    summary = fields.Str(allow_none=True)
    is_published = fields.Bool(missing=False)

class PostUpdateDTO(Schema):
    """DTO for updating post information"""
    title = fields.Str(allow_none=True, validate=lambda x: len(x.strip()) >= 5 if x else True)
    content = fields.Str(allow_none=True, validate=lambda x: len(x.strip()) >= 10 if x else True)
    summary = fields.Str(allow_none=True)
    is_published = fields.Bool(allow_none=True)

class PostResponseDTO(Schema):
    """DTO for post response"""
    id = fields.Int()
    title = fields.Str()
    content = fields.Str()
    summary = fields.Str()
    is_published = fields.Bool()
    view_count = fields.Int()
    created_at = fields.DateTime()
    updated_at = fields.DateTime()
    author = fields.Nested(UserListResponseDTO)

class PostListResponseDTO(Schema):
    """DTO for post list response (minimal information)"""
    id = fields.Int()
    title = fields.Str()
    summary = fields.Str()
    is_published = fields.Bool()
    view_count = fields.Int()
    created_at = fields.DateTime()
    author_name = fields.Str()

# Instantiate schemas for reuse
user_create_schema = UserCreateDTO()
user_update_schema = UserUpdateDTO()
user_response_schema = UserResponseDTO()
user_list_response_schema = UserListResponseDTO(many=True)
user_single_list_response_schema = UserListResponseDTO()

post_create_schema = PostCreateDTO()
post_update_schema = PostUpdateDTO()
post_response_schema = PostResponseDTO()
post_list_response_schema = PostListResponseDTO(many=True)
post_single_list_response_schema = PostListResponseDTO()
