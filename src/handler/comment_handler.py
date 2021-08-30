from model.access_layer import SQLayer
from model.base_models import CommentModel
from sqlalchemy import asc, desc

class CommentHandler:

    @classmethod
    def construct_threads(cls, comment, indent:int=0):
        data = {}
        data["id"] = comment.id
        data["user"] = comment.user.name
        data["user_id"] = comment.user_id
        data["text"] = comment.text
        data["timestamp"] = comment.timestamp
        data["post"] = comment.post.title
        data["post_id"] = comment.post_id
        data["parent_id"] = comment.parent_id
        data["indent"] = indent
        data["replies"] = []

        for reply in comment.replies:
            data["replies"].append(cls.construct_threads(reply, indent+1))

        return data

    @classmethod
    def get_comments(cls, comment_id:int, sort_option:str):
        data = []
        sort = desc if sort_option == "desc" else asc
        if comment_id:
            comments = SQLayer.get_comment_with_children(int(comment_id), sort)
        else:
            comments = SQLayer.get_all_comments(sort)

        for comment in comments:
            data.append(cls.construct_threads(comment))

        return data

    @classmethod
    def create_comment(cls, data:dict):
        parent_id = data.get("parent_id")
        text = data.get("text")
        user_id = data.get("user_id")
        post_id = data.get("post_id")

        if (not text or not user_id or not post_id):
            raise Exception("Missing data")
        
        comment = CommentModel(text=text, user_id=user_id, post_id=post_id, parent_id=parent_id)
        comment_id = SQLayer.create_comment(comment)
        return comment_id

    @classmethod
    def update_comment(cls, data:dict):
        comment_id = data.get("comment_id")
        user_id = data.get("user")
        text = data.get("text")

        if (not comment_id or not user_id or not text):
            raise Exception("Missing data")

        comment = SQLayer.get_comment_with_no_childer(comment_id, user_id)

        if not comment:
            return None

        return SQLayer.update_comment(comment_id, user_id, text)