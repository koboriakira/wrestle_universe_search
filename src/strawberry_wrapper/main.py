from mangum import Mangum
import strawberry
from strawberry.asgi import GraphQL
from strawberry_wrapper.query.query import Query
from util.custom_logging import get_logger

logger = get_logger(__name__)

def generate_graphql_app() -> GraphQL:
    schema = strawberry.Schema(query=Query)
    graphql_app = GraphQL(schema)
    return graphql_app
