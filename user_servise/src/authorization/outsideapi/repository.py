from src.authorization.domain.repository import AuthorizationAbstractApi
from src.authorization.domain.entity import UserOrganizationInfo

class AuthorizationApi(AuthorizationAbstractApi):
    async def get_user_organization_info(user_id: int) -> UserOrganizationInfo:
        return UserOrganizationInfo(
            id = 5,
            command = 1,
            status=1,
            department=None
        )