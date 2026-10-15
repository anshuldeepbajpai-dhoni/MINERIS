from types import SimpleNamespace

import pytest
from fastapi import HTTPException

from app.main import app
from app.api.v1.mines import routes
from app.api.v1.auth import routes as auth_routes
from app.schemas.auth import RegisterRequest


class MineQuery:
    def __init__(self, mines):
        self.mines = mines

    def all(self):
        return self.mines


class FakeDatabase:
    def __init__(self, mines):
        self.mines = mines
        self.rollback_called = False

    def scalars(self, _statement):
        return MineQuery(self.mines)

    def rollback(self):
        self.rollback_called = True


def test_overview_returns_one_result_per_mine(monkeypatch):
    mines = [
        SimpleNamespace(id=7, name="North Zone"),
        SimpleNamespace(id=19, name="South Zone"),
    ]
    db = FakeDatabase(mines)

    def result_for(_db, mine):
        return SimpleNamespace(
            prospectivity_score=float(mine.id),
            classification="MEDIUM",
            confidence=80.0,
            model_version="random-forest-v1",
        )

    monkeypatch.setattr(routes, "get_or_create_prospectivity", result_for)

    response = routes.get_prospectivity_overview(db=db, current_user=object())

    assert [item.mine_id for item in response] == [7, 19]
    assert response[0].mine_name == "North Zone"
    assert response[1].score == 19.0


def test_overview_handles_empty_database(monkeypatch):
    db = FakeDatabase([])
    monkeypatch.setattr(
        routes,
        "get_or_create_prospectivity",
        lambda *_args: pytest.fail("No model prediction should be requested"),
    )

    assert routes.get_prospectivity_overview(db=db, current_user=object()) == []


def test_overview_reports_missing_model_without_internal_path(monkeypatch):
    db = FakeDatabase([SimpleNamespace(id=1, name="Zone")])

    def missing_model(*_args):
        raise FileNotFoundError("private artifact path")

    monkeypatch.setattr(routes, "get_or_create_prospectivity", missing_model)

    with pytest.raises(HTTPException) as error:
        routes.get_prospectivity_overview(db=db, current_user=object())

    assert error.value.status_code == 503
    assert "private artifact path" not in error.value.detail
    assert db.rollback_called


def test_static_overview_route_is_registered_before_mine_detail():
    paths = [route.path for route in routes.router.routes if hasattr(route, "path")]

    assert "/mines/prospectivity-overview" in paths
    assert paths.index("/mines/prospectivity-overview") < paths.index(
        "/mines/{mine_id}"
    )


def test_public_registration_cannot_assign_admin_role(monkeypatch):
    class RegistrationDatabase:
        user = None

        def scalar(self, _statement):
            return None

        def add(self, user):
            self.user = user

        def commit(self):
            pass

        def refresh(self, _user):
            pass

    monkeypatch.setattr(auth_routes, "hash_password", lambda _password: "hashed")
    db = RegistrationDatabase()
    request = RegisterRequest(
        email="new-user@example.com",
        full_name="New User",
        password="test-password",
        role="admin",
    )

    auth_routes.register(data=request, db=db)

    assert db.user.role == "viewer"
