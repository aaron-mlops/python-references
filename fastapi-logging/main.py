import time
import uuid
import uvicorn
from pydantic import BaseModel
from fastapi import FastAPI, Request

from log_util import logger_info, request_id_context

app = FastAPI(docs_url="/swagger")


@app.middleware("http")
async def logging_middleware(request: Request, call_next):
    request_id_context.set(str(uuid.uuid4()))
    start = time.time()

    request_log = dict(method=request.method, path=request.url.path, headers=dict(request.headers))
    if request.method == "GET":
        request_log.update(dict(query_params=dict(request.query_params)))
    elif request.method == "POST":
        request_log.update(dict(body=await request.json()))

    logger_info(f"request: {request_log}")

    response = await call_next(request)
    process_time = time.time() - start

    logger_info(f"time: {process_time}")
    return response


@app.get("/health_check")
async def health_check():
    message = "server alive"
    logger_info(message)
    return {"message": message}


class TestBody(BaseModel):
    message: str


@app.post("/test_body")
async def test_body_api(parameter: TestBody):
    answer = parameter.message + ":test"
    logger_info(dict(answer=answer))
    return answer


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, workers=2, timeout_keep_alive=20,
                access_log=False, log_level="info", server_header=False)
