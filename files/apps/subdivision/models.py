from datetime import datetime, UTC
from enum import Enum
from typing import TYPE_CHECKING

from sqlalchemy import (
    text,
    TIMESTAMP,
    Integer,
    String,
    Boolean,
    Date,
    DateTime,
    Numeric,
    ForeignKey,
    UniqueConstraint,
    CheckConstraint,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from config import Base

from files.apps.subdivision.enums import DepartmentEnum
from files.apps.user import user_models_adapter


class Employee(Base):
    """
    Intermediate table to provide
    connection between Department and User models
    """

    __tablename__ = "employees"

    user: Mapped[str] = mapped_column(
        ForeignKey("users.username", ondelete="CASCADE"),
        primary_key=True,
    )
    subdivision: Mapped[int] = mapped_column(
        ForeignKey("subdivisions.subdivision_id", ondelete="CASCADE"),
        primary_key=True,
    )

    __table_args__ = (
        UniqueConstraint(
            "user",
            "subdivision",
            name="uq_user_subdivision",
        ),
    )


class Subdivision(Base):
    """
    Lead that contains company data, user and records.
    Always has at least one contact.
    """

    __tablename__ = "subdivisions"

    subdivision_id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(256))
    description: Mapped[str | None] = mapped_column(
        String(4086),
        default=None,
        server_default="NULL",
    )
    creation_time: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True),
        default=datetime.now(UTC),
        server_default=text("TIMEZONE('utc', now())"),
    )
    department: Mapped[DepartmentEnum] = mapped_column(
        default=DepartmentEnum.ADMINISTRATIVE
    )

    projects: Mapped[list["Project"]] = relationship(back_populates="subdivision")
    employees: Mapped[list[user_models_adapter.User]] = relationship(
        back_populates="departments",
        secondary="employees",
        viewonly=True,
    )


class Project(Base):
    __tablename__ = "projects"

    project_id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(256))
    completed: Mapped[bool] = mapped_column(default=False, server_default="FALSE")

    start_time: Mapped[datetime] = mapped_column(TIMESTAMP(timezone=True))
    complete_time: Mapped[datetime] = mapped_column(TIMESTAMP(timezone=True))

    description: Mapped[str | None] = mapped_column(
        String(2048),
        default=None,
        server_default="NULL",
    )
    subdivision_id: Mapped[int] = mapped_column(
        ForeignKey(
            "subdivisions.subdivision_id",
            ondelete="CASCADE",
        )
    )
    subdivision: Mapped["Subdivision"] = relationship(back_populates="projects")
