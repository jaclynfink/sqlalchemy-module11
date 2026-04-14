from enum import Enum

from sqlalchemy import CheckConstraint, Float, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class CalculationType(str, Enum):
    """Supported arithmetic operation types."""

    add = "add"
    subtract = "subtract"
    multiply = "multiply"
    divide = "divide"


class Calculation(Base):
    """Persisted arithmetic calculation.

    `result` is optional: when absent, the value is computed on demand via
    `computed_result`.
    """

    __tablename__ = "calculations"
    __table_args__ = (
        CheckConstraint(
            "type IN ('add', 'subtract', 'multiply', 'divide')",
            name="ck_calculations_type_allowed",
        ),
        CheckConstraint(
            "type != 'divide' OR b != 0",
            name="ck_calculations_divide_nonzero",
        ),
    )

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    a: Mapped[float] = mapped_column(Float, nullable=False)
    b: Mapped[float] = mapped_column(Float, nullable=False)
    type: Mapped[str] = mapped_column(String(20), nullable=False, index=True)
    result: Mapped[float | None] = mapped_column(Float, nullable=True)
    user_id: Mapped[int | None] = mapped_column(
        ForeignKey("users.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )

    user = relationship("User", back_populates="calculations")

    @property
    def computed_result(self) -> float:
        """Compute result from `a`, `b`, and `type` when needed."""
        if self.type == CalculationType.add.value:
            return self.a + self.b
        if self.type == CalculationType.subtract.value:
            return self.a - self.b
        if self.type == CalculationType.multiply.value:
            return self.a * self.b
        if self.type == CalculationType.divide.value:
            if self.b == 0:
                raise ValueError("Cannot divide by zero.")
            return self.a / self.b
        raise ValueError(f"Unsupported calculation type: {self.type}")

    @property
    def resolved_result(self) -> float:
        """Return stored result when present, otherwise compute on demand."""
        if self.result is not None:
            return self.result
        return self.computed_result
