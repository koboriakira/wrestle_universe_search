import strawberry
from util.custom_logging import get_logger
from strawberry_wrapper.type.cast import Cast
from strawberry_wrapper.query.query_casts import query_casts

logger = get_logger(__name__)


@strawberry.type
class Query:
    @strawberry.field
    def casts(self) -> list[Cast]:
        return query_casts(self)
