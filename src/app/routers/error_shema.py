from app.db.models import ORJSONModel


class ErrorMessage(ORJSONModel):
    error_code: int
    message: str
