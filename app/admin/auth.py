from typing import Optional

from sqladmin import Admin
from sqladmin.authentication import AuthenticationBackend
from starlette.requests import Request
from starlette.responses import RedirectResponse

from app.auth import authenticate_user, create_access_token
from app.Holders.dependencies import get_current_admin, get_current_user


class AdminAuth(AuthenticationBackend):
    async def login(self, request: Request) -> bool:
        form = await request.form()
        email, password = form["username"], form["password"]

        user = await authenticate_user(email, password)
        if user:
            access_token = create_access_token({"uid": user.id})
            request.session.update({"token": access_token})

        return True

    async def logout(self, request: Request) -> bool:
        # Usually you'd want to just clear the session
        request.session.clear()
        return True

    async def authenticate(self, request: Request) -> Optional[RedirectResponse]:
        token = request.session.get("token")

        if not token:
            return RedirectResponse(request.url_for("admin:login"), status_code=302)

        user = await get_current_admin(token)

        if not user:
            return RedirectResponse(request.url_for("admin:login"), status_code=302)

        # Check the token in depth


au_be = AdminAuth(secret_key="...")
