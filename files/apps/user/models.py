from typing import TYPE_CHECKING

from sqlalchemy import String, text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from config import Base


if TYPE_CHECKING:
    from files import Subdivision


class User(Base):
    """
    User's model definitions
    """

    __tablename__ = "users"

    username: Mapped[str] = mapped_column(primary_key=True, index=True)

    email: Mapped[str | None] = mapped_column(String(255), unique=True, index=True)
    password: Mapped[bytes] = mapped_column()

    name: Mapped[str | None] = mapped_column(String(255))
    phone_number: Mapped[str | None]
    avatar: Mapped[str | None] = mapped_column(unique=True)
    about: Mapped[str | None]

    is_staff: Mapped[bool] = mapped_column(default=False, server_default=text("FALSE"))
    is_active: Mapped[bool] = mapped_column(default=True, server_default=text("TRUE"))
    is_superuser: Mapped[bool] = mapped_column(
        default=False, server_default=text("FALSE")
    )

    departments: Mapped[list["Subdivision"]] = relationship(
        back_populates="employees",
        secondary="employees",
        viewonly=True,
    )
