from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app.models.user import User
import re

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 


class Post:
    schema = 'dojo_wall'
    def __init__(self, data):
        self.id = data['id']
        self.content = data['content']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user_id = data['user_id']
        self.user = None

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM posts JOIN users on users.id = posts.user_id"
        results = connectToMySQL(cls.schema).query_db(query)
        posts = []
        for row in results:
            post = cls(row)
            user_data = {
                'id': row['users.id'],
                'first_name': row['first_name'],
                'last_name': row['last_name'],
                'email': row['email'],
                'password': row['password'],
                'created_at': row['users.created_at'],
                'updated_at': row['users.updated_at']
            }
            user = User(user_data)
            post.user = user
            posts.append(post)
        return posts

    @classmethod
    def get_one(cls, data):
        query = "SELECT * FROM posts JOIN users ON users.id = posts.user_id WHERE posts.id=%(id)s;"
        results = connectToMySQL(cls.schema).query_db(query, data)
        if len(results) < 1:
            return False
        row = results[0]
        post = cls(row)
        user_data = {
            'id': row['users.id'],
            'first_name': row['first_name'],
            'last_name': row['last_name'],
            'email': row['email'],
            'password': row['password'],
            'created_at': row['users.created_at'],
            'updated_at': row['users.updated_at']
        }
        user = User(user_data)
        post.user = user
        return post

    @classmethod
    def get_all_posts(cls):
        query = "SELECT * FROM posts"
        results = connectToMySQL(cls.schema).query_db(query)
        posts = []
        for row in results:
            posts.append(cls(row))
        return posts

    @classmethod
    def create(cls, data):
        query = "INSERT INTO posts (content, user_id) VALUES (%(content)s, %(user_id)s) "
        results = connectToMySQL(cls.schema).query_db(query,data)
        return results

    @classmethod
    def delete(cls, data):
        query = "DELETE FROM posts WHERE id = %(id)s"
        return connectToMySQL(cls.schema).query_db(query, data)

    @staticmethod
    def validate_post(post):
        is_valid = True
        if len(post['content']) < 1:
            is_valid = False
            flash("Post content must not be blank!")
        return is_valid