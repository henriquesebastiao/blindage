from sqlalchemy.orm import Mapped, mapped_column, registry

table_registry = registry()


@table_registry.mapped_as_dataclass
class Account:
    __tablename__ = 'account'

    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    password: Mapped[str]
    name: Mapped[str] = mapped_column(unique=True)
    username: Mapped[str | None] = mapped_column(default=None)
    otp_secret: Mapped[str | None] = mapped_column(default=None)
    url: Mapped[str | None] = mapped_column(default=None)
    recovery_codes: Mapped[str | None] = mapped_column(default=None)
