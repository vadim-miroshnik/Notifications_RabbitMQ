# import pika
import uvicorn
from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi
from fastapi.responses import ORJSONResponse

from api.v1 import notifications, users
from core.config import settings
from db import mongodb
from db.postgres import db
from db.queue import rabbitmq

# from pika import BlockingConnection


app = FastAPI(
    title=settings.project_name,
    docs_url="/api/openapi",
    openapi_url="/api/openapi.json",
    default_response_class=ORJSONResponse,
    swagger_ui_parameters={"syntaxHighlight": False},
)


def custom_openapi():
    if not app.openapi_schema:
        app.openapi_schema = get_openapi(
            title=settings.project_name,
            version="1.0.0",
            openapi_version="3.0.0",
            description="",
            routes=app.routes,
            tags="",
            servers="",
        )
        for _, method_item in app.openapi_schema.get("paths").items():
            for _, param in method_item.items():
                responses = param.get("responses")
                if "422" in responses:
                    del responses["422"]
                if "200" in responses:
                    del responses["200"]
    return app.openapi_schema


app.openapi = custom_openapi


@app.on_event("startup")
async def startup_event():
    # todo use env variables
    # credentials = pika.PlainCredentials("guest", "guest")
    # rabbitmq = pika.BlockingConnection(
    #    pika.ConnectionParameters(host=settings.rabbit.host, port=settings.rabbit.port, credentials=credentials)
    # )
    pass


@app.on_event("shutdown")
async def shutdown_event():
    rabbitmq.close()
    db.close()
    await mongodb.mongodb.close()


app.include_router(notifications.router, prefix="/api/v1/notifications", tags=["notifications"])
app.include_router(users.router, prefix="/api/v1/users", tags=["users"])


if __name__ == "__main__":
    uvicorn.run(
        app,  # type: ignore
        host="0.0.0.0",
        port=8000,
    )
