from fastapi import WebSocket, HTTPException, status

async def require_query_params(ws: WebSocket, name: str) -> str:
    value = ws.query_params.get(name)
    if not value:
        # Accept + close so client gets an error reason
        await ws.accept()
        await ws.close(code=4000, reason=f"Missing query parameter: {name}")
        raise HTTPException(status = status.HTTP_400_BAD_REQUEST, detail=f"Missing {name}")
    return value