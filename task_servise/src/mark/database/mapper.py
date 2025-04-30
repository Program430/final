from src.mark.domain.entity import Mark
from src.mark.database.models import MarkModel

class MarkMapper:
    @staticmethod
    def to_model(mark: Mark) -> MarkModel:
        return MarkModel(
            id=mark.id,
            task_id=mark.task_id,
            quality_score=mark.quality_score,
            comment=mark.comment
        )

    @staticmethod
    def to_entity(mark_model: MarkModel) -> Mark:
        return Mark(
            id=mark_model.id,
            task_id=mark_model.task_id,
            quality_score=mark_model.quality_score,
            comment=mark_model.comment
        )