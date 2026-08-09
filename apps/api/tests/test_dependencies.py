from types import SimpleNamespace

import pytest

from app.core.exceptions import ForbiddenException
from app.dependencies import get_current_admin
from app.models.user import UserRole


def test_user_is_forbidden_from_admin_access():
    user = SimpleNamespace(
        role=UserRole.USER,
    )

    with pytest.raises(ForbiddenException) as exc_info:
        get_current_admin(user)

    assert exc_info.value.status_code == 403
    assert exc_info.value.error_code == "ADMIN_ACCESS_REQUIRED"


def test_admin_can_access_admin_resources():
    admin = SimpleNamespace(
        role=UserRole.ADMIN,
    )

    result = get_current_admin(admin)

    assert result is admin
