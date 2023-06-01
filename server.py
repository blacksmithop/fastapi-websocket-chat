from fastapi import FastAPI, Form, Response, Request
from starlette.websockets import WebSocket, WebSocketDisconnect

from fastapi_sessions.frontends.implementations import SessionCookie, CookieParameters
from fastapi import Depends

from connection_manager import ConnectionManager
from session_verifier import backend, SessionData, verifier

from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from starlette.responses import RedirectResponse

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
async def show_signup(request: Request):
    """Returns the page where user sets their display name
    """
    return templates.TemplateResponse("signup.html", {"request": request})

@app.get("/chat")
@app.post("/chat")
async def show_chatroom(request: Request):
    """Returns the page where user sets their display name
    """
    return templates.TemplateResponse("chat.html", {"request": request})

# session shenanigans
@app.post("/create_session")
async def create_new_session(response: Response, username:str = Form()):
    """Set username for their session
    """
    session = uuid4()
    data = SessionData(username=username)

    await backend.create(session, data)
    cookie.attach_to_response(response, session)

    print(f"created session for {username}")

    url = app.url_path_for("show_chatroom")
    response = RedirectResponse(url=url)
    return response

@app.get("/whoami", dependencies=[Depends(cookie)])
async def whoami(session_data: SessionData = Depends(verifier)):
    """Returns the username
    """
    return session_data

@app.post("/delete_session")
async def delete_current_session(response: Response, session_id: UUID = Depends(cookie)):
    """Deletes the current session
    """
    await backend.delete(session_id)
    cookie.delete_from_response(response)
    return "deleted session"

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """Prototype of a websocket connection to implement chat
    """
    print(websocket)
    await con_mgr.connect(websocket)
    try:
        while True:
            data = await websocket.receive_json()
            # await websocket.send_json(data)
            await con_mgr.push(data)
    except WebSocketDisconnect:
        con_mgr.remove(websocket)


# @app.post("/push/{username}/{message}/")
# async def push_to_connected_websockets(username: str, message: str):
#     """push notification/message send
#     """
#     await con_mgr.push({'message': message, 'username': username})
#     return 200


@app.on_event("startup")
async def startup():
    # Prime the push notification generator
    await con_mgr.generator.asend(None)