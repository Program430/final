from src.comment.domain.entity import Comment
from src.comment.database.models import CommentModel

class CommentMapper:
    @staticmethod
    def to_model(comment: Comment) -> CommentModel:
        return CommentModel(
            id=comment.id,
            task_id=comment.task_id,
            description=comment.description,
            created_time=comment.created_time,
        )

    @staticmethod
    def to_entity(comment_model: CommentModel) -> Comment:
        return Comment(
            id=comment_model.id,
            task_id=comment_model.task_id,
            description=comment_model.description,
            created_time=comment_model.created_time,
        )

    @staticmethod
    def to_model_list(comments: list[Comment]) -> list[CommentModel]:
        return [CommentMapper.to_model(c) for c in comments]

    @staticmethod
    def to_entity_list(comment_models: list[CommentModel]) -> list[Comment]:
        return [CommentMapper.to_entity(cm) for cm in comment_models]
