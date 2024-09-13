from sqlalchemy import ForeignKey
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
