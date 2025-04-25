from abc import ABC, abstractmethod
from src.authorization.domain.entity import UserOrganizationInfo


class AuthorizationAbstractApi(ABC):
    @abstractmethod
    async def get_user_organization_info(user_id: int) -> UserOrganizationInfo:
        raise NotImplemented
