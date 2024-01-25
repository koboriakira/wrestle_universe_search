from mangum import Mangum
from fastapi import FastAPI
from util.custom_logging import get_logger

logger = get_logger(__name__)
logger.info("start")
logger.debug("debug: ON")

app = FastAPI(
    title="Wrestle Universe Search GraphQL API",
    version="0.0.1",
)

@app.get("/graphql")
def graphql():
    request_data: dict = json.loads(request.data.decode('utf-8'))
    logger.debug("graphql")
    logger.info("graphql")
    return {
        'status': 'ok',
    }

@app.get("/healthcheck")
def healthcheck():
    logger.debug("healthcheck")
    logger.info("healthcheck")
    return {
        'status': 'ok',
    }

handler = Mangum(app, lifespan="off")
