# DTO Design Pattern Demo

Ứng dụng web Python sử dụng Flask, SQLite và áp dụng DTO (Data Transfer Object) design pattern để bảo vệ core entities và cung cấp validation dữ liệu.

## 🚀 Tính năng chính

- **DTO Pattern Implementation**: Sử dụng Marshmallow để implement DTO pattern
- **RESTful API**: Cung cấp REST API endpoints với validation đầy đủ
- **Web Interface**: Giao diện web responsive với Bootstrap
- **User Management**: Quản lý người dùng (CRUD operations)
- **Post Management**: Quản lý bài viết với author permissions
- **SQLite Database**: Sử dụng SQLite với SQLAlchemy ORM
- **Data Validation**: Validation dữ liệu đầu vào và đầu ra
- **Error Handling**: Xử lý lỗi comprehensive

## 🏗️ Kiến trúc ứng dụng

```
📁 app/
├── 📄 __init__.py          # Flask app factory
├── 📄 models.py            # Core entities (User, Post)
├── 📄 dto.py               # DTO schemas với Marshmallow
├── 📄 services.py          # Business logic layer
├── 📄 routes.py            # REST API endpoints
└── 📁 templates/           # HTML templates
    ├── 📄 base.html
    ├── 📄 index.html
    ├── 📄 users.html
    └── 📄 posts.html
```

## 🔧 Cài đặt và chạy

### 1. Cài đặt dependencies

```bash
pip install -r requirements.txt
```

### 2. Seed dữ liệu mẫu

```bash
python seed_data.py
```

### 3. Chạy ứng dụng

```bash
python main.py
```

Ứng dụng sẽ chạy tại: http://localhost:5000

## 📖 DTO Pattern Implementation

### Core Entities (models.py)
```python
class User(db.Model):
    # Core entity chứa tất cả thông tin của user
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    # ... other fields
```

### DTO Schemas (dto.py)
```python
class UserCreateDTO(Schema):
    # DTO cho việc tạo user mới - chỉ cho phép fields cần thiết
    username = fields.Str(required=True, validate=lambda x: len(x) >= 3)
    email = fields.Email(required=True)
    password = fields.Str(required=True, validate=lambda x: len(x) >= 6)
    # ... validation rules

class UserResponseDTO(Schema):
    # DTO cho response - loại bỏ sensitive data như password
    id = fields.Int()
    username = fields.Str()
    email = fields.Str()
    # ... safe fields only
```

### Service Layer (services.py)
```python
class UserService:
    @staticmethod
    def create_user(data):
        # Validate input với DTO
        validated_data = user_create_schema.load(data)
        
        # Business logic
        user = User(**validated_data)
        db.session.add(user)
        db.session.commit()
        
        # Return safe DTO response
        return user_response_schema.dump(user), None
```

## 🌐 API Endpoints

### User Management
- `POST /api/users` - Tạo user mới
- `GET /api/users` - Lấy danh sách users
- `GET /api/users/{id}` - Lấy thông tin user
- `PUT /api/users/{id}` - Cập nhật user
- `DELETE /api/users/{id}` - Xóa user

### Post Management
- `POST /api/users/{id}/posts` - Tạo bài viết mới
- `GET /api/posts` - Lấy danh sách bài viết
- `GET /api/posts/{id}` - Lấy thông tin bài viết
- `PUT /api/posts/{id}/user/{uid}` - Cập nhật bài viết
- `DELETE /api/posts/{id}/user/{uid}` - Xóa bài viết

### Authentication
- `POST /api/auth/login` - Đăng nhập

## 💡 Lợi ích của DTO Pattern

1. **Bảo vệ Core Entities**: DTO ngăn chặn việc thay đổi trực tiếp core entities
2. **Data Validation**: Validation dữ liệu đầu vào trước khi xử lý
3. **Security**: Kiểm soát dữ liệu được expose (ẩn password, sensitive info)
4. **Flexibility**: Dễ dàng thay đổi API response format mà không ảnh hưởng core entities
5. **Separation of Concerns**: Tách biệt presentation layer với business logic

## 🎨 Giao diện Web

- **Trang chủ**: Giới thiệu về DTO pattern và kiến trúc ứng dụng
- **Quản lý Users**: CRUD operations cho users với validation
- **Quản lý Posts**: CRUD operations cho posts với author permissions
- **Responsive Design**: Sử dụng Bootstrap 5 với custom styling

## 🛠️ Technologies Used

- **Backend**: Python, Flask, SQLAlchemy
- **Database**: SQLite
- **Validation**: Marshmallow
- **Frontend**: HTML, CSS, JavaScript, Bootstrap 5
- **HTTP Client**: Axios

## 📝 Sample Data

Ứng dụng đi kèm với dữ liệu mẫu:
- 4 users (3 active, 1 inactive)
- 5 posts với nhiều trạng thái khác nhau
- Relationships giữa users và posts

## ⚡ Quick Start Guide

1. **Tạo user mới**:
   ```bash
   curl -X POST http://localhost:5000/api/users \
     -H "Content-Type: application/json" \
     -d '{"username":"testuser","email":"test@example.com","password":"password123","full_name":"Test User"}'
   ```

2. **Lấy danh sách users**:
   ```bash
   curl http://localhost:5000/api/users
   ```

3. **Tạo bài viết**:
   ```bash
   curl -X POST http://localhost:5000/api/users/1/posts \
     -H "Content-Type: application/json" \
     -d '{"title":"My First Post","content":"This is my first post content","is_published":true}'
   ```

## 🔒 Security Features

- Password hashing với Werkzeug
- Input validation với Marshmallow
- SQL injection protection với SQLAlchemy ORM
- XSS protection trong templates
- Authorization checks cho post operations

---

**Lưu ý**: Đây là ứng dụng demo để minh họa DTO pattern. Trong production, cần thêm authentication middleware, rate limiting, và các security measures khác.
