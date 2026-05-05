import random
import uvicorn
from starlette.applications import Starlette
from starlette.responses import JSONResponse
from starlette.routing import Route

from service_vector import vectorize_transaction


async def ready(request):
    return JSONResponse({"status": "ready"}, status_code=200)


async def fraud_score(request):
    try:
        data = await request.json()
        transaction = vectorize_transaction(data=data)
        score = round(random.random(), 2)
        approved = score < 0.5

        return JSONResponse({
            "approved": approved,
            "fraud_score": score
        })
    except Exception:
        return JSONResponse({"error": "Invalid payload"}, status_code=400)

routes = [
    Route("/ready", endpoint=ready, methods=["GET"]),
    Route("/fraud-score", endpoint=fraud_score, methods=["POST"]),
]

app = Starlette(debug=True, routes=routes)


def run_server(port: int):
    uvicorn.run(app, host="0.0.0.0", port=port)
