from enum import Enum
from math import isclose, isfinite

from pydantic import BaseModel, ConfigDict, Field, model_validator


class CalculationType(str, Enum):
    """Supported arithmetic operation types for API payloads."""

    add = "add"
    subtract = "subtract"
    multiply = "multiply"
    divide = "divide"


def _compute_result(a: float, b: float, calculation_type: CalculationType) -> float:
    if calculation_type == CalculationType.add:
        return a + b
    if calculation_type == CalculationType.subtract:
        return a - b
    if calculation_type == CalculationType.multiply:
        return a * b
    if calculation_type == CalculationType.divide:
        return a / b
    raise ValueError(f"Unsupported calculation type: {calculation_type}")


class CalculationBase(BaseModel):
    """Shared validation for calculation request/response payloads."""

    a: float = Field(description="Left operand")
    b: float = Field(description="Right operand")
    type: CalculationType

    @model_validator(mode="after")
    def validate_operands(self) -> "CalculationBase":
        if not isfinite(self.a) or not isfinite(self.b):
            raise ValueError("Operands must be finite numbers.")
        if self.type == CalculationType.divide and self.b == 0:
            raise ValueError("Division by zero is not allowed for type='divide'.")
        return self


class CalculationCreate(CalculationBase):
    """Schema for creating calculations."""

    result: float | None = Field(default=None, description="Optional persisted result")
    user_id: int | None = Field(default=None, ge=1, description="Optional user owner id")

    @model_validator(mode="after")
    def validate_optional_result(self) -> "CalculationCreate":
        if self.result is not None:
            if not isfinite(self.result):
                raise ValueError("Result must be a finite number.")
            expected = _compute_result(self.a, self.b, self.type)
            if not isclose(self.result, expected, rel_tol=1e-9, abs_tol=1e-9):
                raise ValueError("Provided result does not match operands and operation type.")
        return self


class CalculationRead(CalculationBase):
    """Schema for exposing persisted calculations."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    result: float | None = None
    user_id: int | None = None
