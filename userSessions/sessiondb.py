''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
from typing import Dict, Any

import mysql.connector as mysql
from fastapi import Request, Response
import secrets, json
from datetime import datetime, timezone, timedelta
import threading, time
import db_utils

''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
### PULLED FROM ECE140A Project
class Sessions:
    def __init__(self, db_config:dict, secret_key:str, expiry:int=900) -> None:
        self.expiry = expiry
        self.db = SessionStore(db_config, expiry)
        self.db_config = db_config
        self.secret_key = secret_key
        self.expiry_process = threading.Thread(target=self.auto_expire, args=(expiry,), daemon=True)
        self.expiry_process.start()

    def __del__(self):
        self.stop_thread = True
        self.expiry_process.join()

    def create_session(self, response:Response, session_data:dict) -> str:
        session_id = secrets.token_urlsafe(16)
        self.db.create(session_id, session_data)
        response.set_cookie(key="session_id", value=session_id)
        return session_id

    def get_session(self, request:Request) -> dict:
        session_id = request.cookies.get("session_id")
        return self.db.read(session_id)

    def end_session(self, request:Request, response:Response) -> None:
        session_id = request.cookies.get("session_id")
        self.db.delete(session_id)
        response.delete_cookie(key="session_id")

    def auto_expire(self, expiry) -> None:
        while True:
            time.sleep(expiry)
            self.db.delete_expired()
            print('[LOGGING] deleted expired sessions')

''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
class SessionStore:
    def __init__(self, db_config:dict, expiry:int) -> None:
        self.db_config = db_config
        self.expiry = expiry

    def create(self, session_id:str, session_data:dict) -> None:
        db = mysql.connect(**self.db_config)
        cursor = db.cursor()
        user_id = db_utils.get_user_id(session_data['username'])
        query = "insert into sessions (session_id, user_id) values (%s, %s);"
        cursor.execute(query, (session_id, user_id))
        db.commit()

        cursor.close()
        db.close()

    def read(self, session_id:str) -> dict:
        if session_id is None:
            return {}

        db = mysql.connect(**self.db_config)
        cursor = db.cursor()

        query = "select created_at from sessions where session_id = %s;"
        cursor.execute(query, (session_id,))
        result = cursor.fetchone()

        cursor.close()
        db.close()

        if result is None:
            return {}

        # Invalidate the session if it has expired; expiry is in units of seconds
        created_at = result[0]
        elapsed = (datetime.utcnow() - created_at).total_seconds()
        if elapsed > self.expiry:
            self.delete(session_id)
            return {}

        return {'session_id': session_id}

    def delete(self, session_id:str) -> None:
        if session_id is not None:
            db = mysql.connect(**self.db_config)
            cursor = db.cursor()

            query = "delete from sessions where session_id = %s;"
            cursor.execute(query, (session_id,))
            db.commit()

            cursor.close()
            db.close()

    def delete_expired(self) -> None:
        db = mysql.connect(**self.db_config)
        cursor = db.cursor()

        session_age = datetime.utcnow() - timedelta(seconds=self.expiry)
        query = "delete from sessions where created_at < %s;"
        cursor.execute(query, (session_age,))
        db.commit()

        cursor.close()
        db.close()