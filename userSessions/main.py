from fastapi import FastAPI, Response, Request, status,HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse, FileResponse,JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from dotenv import load_dotenv
import uvicorn
import json
import requests
import db_utils as db
import mysql.connector as mysql
from auth import logged_in, logout, login, get_who
import plotly.graph_objects as go
from models import User, Visitor

@app.post('/login', status_code=status.HTTP_200_OK)
def post_login(visitor: Visitor, request: Request, response: Response, next_route="/") -> JSONResponse:
        username = visitor.username
        password = visitor.password
        user_data = {
        "firstName": "john",
        "lastName": "Doe",
        "userId": "123456"
        }
        #print(user_data)
        # Authenticate the user
        if login(username, password, request, response):
                # Set cookie here as needed
                response.set_cookie(key="session", value="example_session_value")
                return JSONResponse(
                       status_code=200,
                        content={
                        "success": True,
                        "next": next_route, #this doesn't do anything?
                        "firstName": user_data["firstName"],
                        "lastName": user_data["lastName"],
                        "userId": user_data["userId"]
                    },
                       headers={"set-cookie": response.headers.get("set-cookie")}
                    )
        else:
                return JSONResponse(
                       status_code=401,
                       content={"success": False, "message": "Unauthorized"},
                        )    

# Route to retrieve all users
@app.get('/users')
def get_users() -> dict:
    users = db.select_users()
    keys = ['id', 'first_name', 'last_name', 'username', 'email']
    users = [dict(zip(keys, user)) for user in users]
    return {"users": users}

# Route to retrieve a specific user by ID
@app.get('/users/{user_id}')
def get_user(user_id: int) -> dict:
    user = db.select_users(user_id)
    if user:
        return {'id': user[0], 'username': user[1], 'email': user[2], 'first_name': user[3], 'last_name': user[4]}
    return {}

# Route to create a new user
@app.post("/users", status_code=status.HTTP_201_CREATED)
async def create_user(user: User, response: Response):
    new_id = db.create_user(user.username, user.password, user.email, user.first_name, user.last_name)
    print(new_id)
    if new_id == 0:
        response.status_code = status.HTTP_418_IM_A_TEAPOT
        return
    return get_user(new_id)

# Route to handle user logout
@app.get("/logout", response_class=HTMLResponse)
async def get_logout(request: Request, response: Response):
    logout(request, response)
    return RedirectResponse("/", status_code=311)

# Route to access protected content
@app.get('/protected')
@logged_in
def get_protected(request: Request) -> dict:
    return {'message': 'Access granted'}