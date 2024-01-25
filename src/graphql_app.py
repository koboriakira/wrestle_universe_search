from mangum import Mangum
from fastapi import FastAPI
from strawberry_wrapper.main import generate_graphql_app
from util.custom_logging import get_logger

logger = get_logger(__name__)
logger.info("start")
logger.debug("debug: ON")

app = FastAPI(
    title="Wrestle Universe Search GraphQL API",
    version="0.0.1",
)

graphql_app = generate_graphql_app()
app.add_route("/graphql", graphql_app)

@app.get("/healthcheck")
def healthcheck():
    logger.debug("healthcheck")
    logger.info("healthcheck")
    return {
        'status': 'ok',
    }

handler = Mangum(app, lifespan="off")
