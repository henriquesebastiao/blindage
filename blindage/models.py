from datetime import datetime

from sqlalchemy import ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column, registry

table_registry = registry()


@table_registry.mapped_as_dataclass
class Account:
    __tablename__ = 'accounts'

    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    password: Mapped[bytes]
    name: Mapped[bytes] = mapped_column(unique=True)
    username: Mapped[bytes | None] = mapped_column(default=None)
    otp_secret: Mapped[bytes | None] = mapped_column(default=None)
    url: Mapped[bytes | None] = mapped_column(default=None)
    recovery_codes: Mapped[bytes | None] = mapped_column(default=None)

    created_at: Mapped[datetime] = mapped_column(
        init=False, server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        init=False, onupdate=func.now(), server_default=func.now()
    )
    password_updated_at: Mapped[datetime | None] = mapped_column(default=None)


@table_registry.mapped_as_dataclass
class OtherAttribute:
    __tablename__ = 'other_attributes'

    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    name: Mapped[bytes]
    content: Mapped[bytes]
    account_id: Mapped[int] = mapped_column(ForeignKey('accounts.id'))


@table_registry.mapped_as_dataclass
class BlindageSettings:
    __tablename__ = 'blindage_settings'

    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    main_password: Mapped[str]


@table_registry.mapped_as_dataclass
class PasswordHistory:
    __tablename__ = 'password_history'

    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    password: Mapped[bytes]
    account_id: Mapped[int] = mapped_column(ForeignKey('accounts.id'))
    created_at: Mapped[datetime] = mapped_column(
        init=False, server_default=func.now()
    )
