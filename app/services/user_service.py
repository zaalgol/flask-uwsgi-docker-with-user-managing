import app
from app.repositories.user_repository import UserRepository
from app.services.hassing_service import PasswordHasher
from app.services.token_serivce import TokenService
from flask import jsonify, make_response

class UsersService:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        self.user_repository = UserRepository()
        self.token_service = TokenService()

    def login(self, email, password):
        user = self.user_repository.get_user_by_email(email)
        if user:
            is_valid_password = PasswordHasher.check_password(user.password, password)
            if is_valid_password:
                access_token = self.token_service.create_jwt_token(user.user_id)
                response = make_response(jsonify({"message": "Login successful", "access_token": access_token}), 200)
                return response
        return jsonify({'message': 'Invalid credentials'}), 401
    
    def seed_admin_user(self):
        email=f'admin@{app.config.config.Config.EMAIL_DOMAIN}'
        password=app.config.config.Config.ADMIN_PASSWORD
        self.create_user(email, password)

    def create_user(self, email, password):
        hashed_password = PasswordHasher.hash_password(password)
        user = self.user_repository.create_user(email, hashed_password) 