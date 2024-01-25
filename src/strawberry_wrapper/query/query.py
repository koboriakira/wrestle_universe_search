import strawberry
from typing import Optional
from util.custom_logging import get_logger
from strawberry_wrapper.type.cast import Cast
from strawberry_wrapper.query.query_casts import QueryCasts
from infrastructure.json_repository.json_local_repository import JsonLocalRepository


logger = get_logger(__name__)

json_repository = JsonLocalRepository()
query_casts = QueryCasts(json_repository=json_repository)

@strawberry.type
class Query:
    @strawberry.field
    def casts(self, sub_display_name: Optional[str] = None) -> list[Cast]:
        """
        sample query:
        {
            casts(subDisplayName: "RAKU") {
                id
            }
        }
        """
        return query_casts.query(sub_display_name)
