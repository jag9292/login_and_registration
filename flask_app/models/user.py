from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
import re


EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
FIRST_NAME_REGEX = re.compile(r'^[a-zA-Z]+$')
LAST_NAME_REGEX = re.compile(r'^[a-zA-Z]+$')


class User:
    def __init__(self,data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @classmethod
    def add(cls,data):
        query = "INSERT INTO users (first_name, last_name, email, password) VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s);"
        
        return connectToMySQL('login_and_registration').query_db(query, data)

    @staticmethod
    def validate_create(data):
        is_valid = True
        if len(data['first_name']) < 1:
            flash("Must have first name!")
            is_valid = False
        if not FIRST_NAME_REGEX.match(data['first_name']):
            flash("First name must be a valid format!")
            is_valid = False
        if len(data['last_name']) < 1:
            flash("Must have last name!")
            is_valid = False
        if not LAST_NAME_REGEX.match(data['last_name']):
            flash("Last name must be a valid format!")
            is_valid = False
        if not EMAIL_REGEX.match(data['email']):
            flash("Email must be a valid format!")
            is_valid = False
        if len(data['password']) < 8:
            flash("Must be at least 8 characters!")
            is_valid = False
        return is_valid

    @staticmethod
    def validate_login(data):
        is_valid = True
        if not EMAIL_REGEX.match(data['email']):
            flash("Email must be a valid format!")
            is_valid = False
        if len(data['password']) < 8:
            flash("Must be at least 8 characters!")
            is_valid = False
        return is_valid

    @classmethod
    def get_by_email(cls,data):
        query = "SELECT * FROM users WHERE email = %(email)s;"
        result = connectToMySQL("login_and_registration").query_db(query,data)
        if len(result) < 1:
            return False
        return cls(result[0])