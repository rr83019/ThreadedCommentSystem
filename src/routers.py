from flask_restful import Resource
from flask import json, request, jsonify
from handler.comment_handler import CommentHandler

class Comments(Resource):

    def get(self):
        try:
            comment_id = request.args.get("id", None)
            sort_option = request.args.get("sort_option")
            comments = CommentHandler.get_comments(comment_id, sort_option)
            return jsonify(comments)
        except Exception as e:
            raise e

    def post(self):
        try:
            data = request.get_json()
            comment_id = CommentHandler.create_comment(data=data)
            return jsonify(message="comment created", id=comment_id)
        except Exception as e:
            raise e

    def put(self):
        try:
            data = request.get_json()
            result = CommentHandler.update_comment(data=data)
            message = "comment updated" if result else "something went wrong"
            return jsonify(message=message)
        except Exception as e:
            raise e