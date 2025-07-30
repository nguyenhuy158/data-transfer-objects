from app import create_app
from app.models import db, User, Post
from werkzeug.security import generate_password_hash
from datetime import datetime, date

def seed_data():
    """Seed the database with sample data"""
    app = create_app()
    
    with app.app_context():
        # Clear existing data
        Post.query.delete()
        User.query.delete()
        
        # Create sample users
        users_data = [
            {
                'username': 'admin',
                'email': 'admin@example.com',
                'password_hash': generate_password_hash('admin123'),
                'full_name': 'Quản trị viên',
                'phone': '0123456789',
                'date_of_birth': date(1990, 1, 1),
                'is_active': True
            },
            {
                'username': 'john_doe',
                'email': 'john@example.com',
                'password_hash': generate_password_hash('password123'),
                'full_name': 'John Doe',
                'phone': '0987654321',
                'date_of_birth': date(1985, 5, 15),
                'is_active': True
            },
            {
                'username': 'jane_smith',
                'email': 'jane@example.com',
                'password_hash': generate_password_hash('password123'),
                'full_name': 'Jane Smith',
                'phone': '0555123456',
                'date_of_birth': date(1992, 8, 22),
                'is_active': True
            },
            {
                'username': 'inactive_user',
                'email': 'inactive@example.com',
                'password_hash': generate_password_hash('password123'),
                'full_name': 'Người dùng không hoạt động',
                'is_active': False
            }
        ]
        
        users = []
        for user_data in users_data:
            user = User(**user_data)
            db.session.add(user)
            users.append(user)
        
        db.session.commit()
        
        # Create sample posts
        posts_data = [
            {
                'title': 'Giới thiệu về DTO Design Pattern',
                'summary': 'Tìm hiểu về Data Transfer Object pattern và lợi ích của nó trong phát triển ứng dụng.',
                'content': '''DTO (Data Transfer Object) là một design pattern được sử dụng để truyền tải dữ liệu giữa các tầng của ứng dụng.

Lợi ích của DTO pattern:
1. Bảo vệ core entities khỏi việc thay đổi không mong muốn
2. Cung cấp validation dữ liệu đầu vào
3. Kiểm soát dữ liệu được trả về cho client
4. Tách biệt presentation layer với business logic layer
5. Giảm coupling giữa các components

Trong ứng dụng này, chúng ta sử dụng Marshmallow để implement DTO pattern một cách hiệu quả.''',
                'is_published': True,
                'user_id': 1
            },
            {
                'title': 'Flask và SQLAlchemy ORM',
                'summary': 'Hướng dẫn sử dụng Flask với SQLAlchemy để xây dựng web application.',
                'content': '''Flask là một micro web framework cho Python, rất phù hợp để xây dựng web applications và APIs.

SQLAlchemy là một ORM (Object-Relational Mapping) library mạnh mẽ cho Python, giúp tương tác với database một cách dễ dàng.

Trong project này, chúng ta kết hợp Flask và SQLAlchemy để:
- Tạo models cho User và Post
- Thiết lập relationships giữa các entities
- Thực hiện các operations CRUD
- Quản lý database transactions''',
                'is_published': True,
                'user_id': 2
            },
            {
                'title': 'RESTful API Design Best Practices',
                'summary': 'Các nguyên tắc thiết kế RESTful API hiệu quả và dễ sử dụng.',
                'content': '''REST (Representational State Transfer) là một architectural style cho việc thiết kế web services.

Best practices cho RESTful API:
1. Sử dụng HTTP methods đúng mục đích (GET, POST, PUT, DELETE)
2. Sử dụng status codes phù hợp
3. Thiết kế URL structure rõ ràng và nhất quán
4. Implement proper error handling
5. Sử dụng JSON format cho data exchange
6. Implement authentication và authorization
7. Versioning API properly
8. Documentation đầy đủ và chi tiết''',
                'is_published': False,
                'user_id': 2
            },
            {
                'title': 'Validation với Marshmallow',
                'summary': 'Sử dụng Marshmallow để validation và serialization dữ liệu trong Python.',
                'content': '''Marshmallow là một library mạnh mẽ cho việc serialization, validation và deserialization của Python objects.

Các tính năng chính:
1. Schema definition dễ dàng
2. Built-in validators
3. Custom validation functions
4. Nested schemas support
5. Error handling tốt
6. Integration với nhiều frameworks

Trong DTO pattern, Marshmallow giúp chúng ta:
- Validate input data trước khi xử lý
- Transform data giữa các layers
- Serialize objects thành JSON response
- Kiểm soát fields được expose ra ngoài''',
                'is_published': True,
                'user_id': 3
            },
            {
                'title': 'Database Design với SQLite',
                'summary': 'Thiết kế database hiệu quả với SQLite cho ứng dụng nhỏ và vừa.',
                'content': '''SQLite là một database engine nhẹ, self-contained và serverless, rất phù hợp cho development và các ứng dụng nhỏ.

Ưu điểm của SQLite:
1. Không cần server setup
2. File-based database
3. ACID compliant
4. Cross-platform
5. Zero configuration
6. Reliable và fast

Trong project này, chúng ta thiết kế:
- Users table với proper indexing
- Posts table với foreign key relationships
- Appropriate data types và constraints
- Cascading deletes để maintain data integrity''',
                'is_published': True,
                'user_id': 1
            }
        ]
        
        for post_data in posts_data:
            post = Post(**post_data)
            db.session.add(post)
        
        db.session.commit()
        
        print("✅ Sample data has been seeded successfully!")
        print(f"Created {len(users)} users and {len(posts_data)} posts")

if __name__ == '__main__':
    seed_data()
