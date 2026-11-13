from app.models import Base, Milestone, Project


def test_initial_tables_are_registered() -> None:
    expected = {"users", "projects", "repositories", "project_repositories", "milestones", "tasks"}
    assert expected.issubset(Base.metadata.tables.keys())


def test_project_constraints_are_declared() -> None:
    constraints = {constraint.name for constraint in Project.__table__.constraints}
    assert "uq_projects_user_slug" in constraints
    assert "ck_projects_status" in constraints


def test_milestone_weight_constraint_is_declared() -> None:
    constraints = {constraint.name for constraint in Milestone.__table__.constraints}
    assert "ck_milestones_positive_weight" in constraints
