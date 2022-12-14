import typing

from services.permission import authenticate, is_admin
from strawberry.permission import BasePermission
from strawberry.types import Info


class IsAuthenticated(BasePermission):
    message = "User is not authenticated"

    def has_permission(self, source: typing.Any, info: Info, **kwargs) -> bool:
        if session_token := info.context["session_token"]:
            is_authenticate, context_save = authenticate(
                info.context, session_token
            )
            if is_authenticate:
                info.context.update(context_save)
                return True
        return False


class IsAdmin(BasePermission):
    message = "User is not admin"

    def has_permission(self, source: typing.Any, info: Info, **kwargs) -> bool:
        if session_token := info.context["session_token"]:
            return is_admin(info.context["db"], session_token)
        return False
