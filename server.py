from fastapi import FastAPI, Response, Request
from starlette.websockets import WebSocket, WebSocketDisconnect

from fastapi_sessions.frontends.implementations import SessionCookie, CookieParameters
from fastapi import Depends

from connection_manager import ConnectionManager
from session_verifier import backend, SessionData, verifier

from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from uuid import uuid4, UUID


cookie_params = CookieParameters()

# Uses UUID
cookie = SessionCookie(
    cookie_name="cookie",
    identifier="general_verifier",
    auto_error=True,
    secret_key="DONOTUSE",
    cookie_params=cookie_params,
)


app = FastAPI()

# static files
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# ws connection manager and notification service
con_mgr = ConnectionManager() 


@app.get("/")
async def get(request: Request):
    """Returns the page where user sets their display name
    """
    return templates.TemplateResponse("signup.html", {"request": request})

# session shenanigans
@app.post("/create_session/{name}")
async def create_session(name: str, response: Response):
    """Set username for their session
    """
    session = uuid4()
    data = SessionData(username=name)

    await backend.create(session, data)
    cookie.attach_to_response(response, session)

    return f"created session for {name}"

@app.get("/whoami", dependencies=[Depends(cookie)])
async def whoami(session_data: SessionData = Depends(verifier)):
    """Returns the username
    """
    return session_data

@app.post("/delete_session")
async def del_session(response: Response, session_id: UUID = Depends(cookie)):
    """Deletes the current session
    """
    await backend.delete(session_id)
    cookie.delete_from_response(response)
    return "deleted session"

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """Prototype of a websocket connection to implement chat
    """
    await con_mgr.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            await websocket.send_text(f"Message text was: {data}")
    except WebSocketDisconnect:
        con_mgr.remove(websocket)


@app.get("/push/{message}")
async def push_to_connected_websockets(message: str):
    """WIP (push notification)
    """
    await con_mgr.push(f"! Push notification: {message} !")



@app.on_event("startup")
async def startup():
    # Prime the push notification generator
    await con_mgr.generator.asend(None)