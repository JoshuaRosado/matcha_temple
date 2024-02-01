from unittest import result
from flask_app import app
from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app.models import review
from flask_app.models import user
from flask_bcrypt import Bcrypt
import re

DB = "matcha_verde"
class Review:
    def __init__(self, review):
        self.id = review["id"]
        self.name = review["name"]
        self.stars = review["stars"]
        self.review_title = review["review_title"]
        self.message = review["message"]
        self.created_at = review["created_at"]
        self.updated_at = review["updated_at"]
        
        
# =================== LEAVE REVIEW ==========================
@classmethod
def create_review(cls, review_dict):
    if not cls.is_valid(review_dict):
        return False
    
    query = """ INSERT INTO reviews (name, stars, review_title, message, user_id, matcha_id)
    VALUES (%(name)s, %(stars)s, %(review_title)s, %(message)s, %(user_id)s, %(matcha_id)s);"""
    
    review = connectToMySQL(DB).query_db(query, review_dict)
    return review


# =================== DELETE REVIEW ==========================

@classmethod
def delete_review(cls, review_id):
    
    data = {"id": review_id}
    query = """DELETE FROM reviews WHERE id = %(id)s;"""
    connectToMySQL(DB).query_db(query, data)
    
    return review_id


# =================== UPDATE REVIEW ==========================
@classmethod
def update_review(cls, review_dict):
    
    review = cls.get_by_id(review_dict["id"])
    
    query = """UPDATE reviews
            SET name = %(name)s, stars = %(stars)s, review_title = %(review_title)s, message = %(message)s
            WHERE id = %(id)s;"""
    result = connectToMySQL(DB).query_db(query, review_dict)
    
    return review
    
# =================== GET ALL REVIEWS ==========================
@classmethod
def get_all(cls):
    query = """SELECT
            reviews.id, reviews.created_at, reviews.updated_at,name, stars, review_title, message, users.id as user_id, users.first_name, users.last_name, users.email, users.created_at, users.updated_at 
            FROM reviews
            JOIN users ON users.id = reviews.user_id;
            JOIN users ON """
    review_data = connectToMySQL(DB).query_db(query)
    
    reviews = []
    
    for review in review_data:
        
        review_obj = cls(review)
        
        review_obj.user = user.User(
            {
                "id": review["id"],
                "first_name": review["first_name"],
                "last_name": review["last_name"],
                "email": review["email"],
                "password": False,
                "created_at": review["created_at"],
                "updated_at": review["updated_at"]
                
            }
        )
        reviews.append(review_obj)
        
        return reviews
        


# =================== GET REVIEW BY ID ==========================
@classmethod
def get_by_id(cls, review_dict):
    data = {"id": review_dict}
    query = """SELECT * FROM reviews
            JOIN users on users.id = reviews.user_id
            WHERE  reviews.id = %(id)s;"""
            
    result = connectToMySQL(DB).query_db(query, data)
    review = cls(result)
    
    review.user = user.User(
        {
            "id": result["user_id"],
            "first_name": result["first_name"],
            "last_name": result["last_name"],
            "email": result["email"],
            "password": False,
            "created_at": result["created_at"],
            "updated_at": result["updated_at"]
        }
    )
    return review


# =================== VALIDATE REVIEW'S INPUT ==========================
@staticmethod
def is_valid(matcha_dict):
    valid = True
    if len(matcha_dict["name"])< 1 :
        flash("Name should be at least 2 characters")
        valid = False
        
    if len(matcha_dict["stars"])< 0:
        flash("Choose a star rate")
        valid = False
        
    if len(matcha_dict["review_title"]) < 3:
        flash ("Review title should be at least 3 characters")
        valid = False
        
    if len(matcha_dict["message"]) < 10:
        flash("Review content should be at least 10 characters")
        valid = False
    
    return valid