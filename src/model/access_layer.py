from model.base_models import CommentModel
from model.db import session_scope


class SQLayer:

    @classmethod
    def get_all_comments(cls, sort: callable):
        with session_scope() as session:
            return session.query(CommentModel).order_by(sort(CommentModel.timestamp))

    @classmethod
    def get_comment_with_children(cls, comment_id, sort):
        with session_scope() as session:
            return session.query(CommentModel)\
                .filter({CommentModel.id:comment_id})\
                    .order_by(sort(CommentModel.timestamp))

    @classmethod
    def create_comment(cls, comment: CommentModel):
        with session_scope() as session:
            session.add(comment)
            session.flush()
            return comment.id

    @classmethod
    def get_comment_with_no_childer(cls, comment_id: int, user_id: int):
        with session_scope() as session:
            return session.query(CommentModel).filter(
                CommentModel.id==comment_id,
                CommentModel.user==user_id,
                CommentModel.replies==None
            )

    @classmethod
    def update_comment(cls, comment_id: int, user_id: int, text: str):
        with session_scope() as session:
            result = session.query(CommentModel)\
                .filter(
                    CommentModel.id==comment_id, 
                    CommentModel.user==user_id
                ).update({
                CommentModel.text: text
                })
        return result

