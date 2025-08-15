# app.py (Render)
from flask import Flask, request, jsonify
from flask_cors import CORS
import os, time, hmac, hashlib, base64
import psycopg  # server side only
from datetime import datetime, timedelta

app = Flask(__name__)
CORS(app)

SECRET = os.getenv("API_SECRET", "change-me")  # set in Render
DATABASE_URL = os.getenv("DATABASE_URL")

def db():
    return psycopg.connect(DATABASE_URL)

# --- tiny HMAC token (expires in 1 hour) ---
def make_token(username):
    exp = int(time.time()) + 3600
    msg = f"{username}.{exp}".encode()
    sig = hmac.new(SECRET.encode(), msg, hashlib.sha256).digest()
    return base64.urlsafe_b64encode(msg + b"." + sig).decode()

def verify_token(token):
    try:
        raw = base64.urlsafe_b64decode(token.encode())
        parts = raw.split(b".")
        if len(parts) != 3: return None
        username = parts[0].decode()
        exp = int(parts[1].decode())
        sig = parts[2]
        if time.time() > exp: return None
        msg = parts[0] + b"." + parts[1]
        expect = hmac.new(SECRET.encode(), msg, hashlib.sha256).digest()
        if not hmac.compare_digest(sig, expect): return None
        return username
    except Exception:
        return None

def require_auth():
    auth = request.headers.get("Authorization", "")
    if not auth.startswith("Bearer "): return None
    return verify_token(auth.split(" ",1)[1])

@app.post("/api/register")
def register():
    data = request.get_json(force=True)
    u, p = data.get("username","").strip(), data.get("password","")
    if not u or not p: return jsonify(msg="missing fields"), 400
    with db() as conn, conn.cursor() as c:
        c.execute("select 1 from main_game where user_name=%s", (u,))
        if c.fetchone(): return jsonify(msg="username taken"), 409
        c.execute("insert into main_game(user_name,password) values(%s,%s)", (u,p))
        conn.commit()
    return jsonify(msg="ok"), 200

@app.post("/api/login")
def login():
    data = request.get_json(force=True)
    u, p = data.get("username","").strip(), data.get("password","")
    with db() as conn, conn.cursor() as c:
        c.execute("select password from main_game where user_name=%s", (u,))
        row = c.fetchone()
        if not row or row[0] != p:
            return jsonify(msg="invalid credentials"), 401
    return jsonify(token=make_token(u))

@app.get("/api/scores")
def get_scores():
    u = require_auth()
    if not u: return jsonify(msg="unauthorized"), 401
    with db() as conn, conn.cursor() as c:
        c.execute("""select easy_car_high_score, hard_car_high_score, snake_high_score
                     from main_game where user_name=%s""", (u,))
        row = c.fetchone() or (0,0,0)
    return jsonify(
        easy_car_high_score = row[0] or 0,
        hard_car_high_score = row[1] or 0,
        snake_high_score    = row[2] or 0
    )

@app.post("/api/scores")
def post_scores():
    u = require_auth()
    if not u: return jsonify(msg="unauthorized"), 401
    data = request.get_json(force=True)
    fields, vals = [], []
    for col in ("easy_car_high_score","hard_car_high_score","snake_high_score"):
        if col in data:
            fields.append(f"{col} = GREATEST(COALESCE({col},0), %s)")
            vals.append(int(data[col]))
    if not fields: return jsonify(msg="nothing to update"), 400
    with db() as conn, conn.cursor() as c:
        c.execute(f"update main_game set {', '.join(fields)} where user_name=%s", (*vals, u))
        conn.commit()
    return jsonify(msg="ok")

@app.get("/api/leaderboard")
def leaderboard():
    kind = request.args.get("kind")  # car_easy | car_hard | snake
    col = {"car_easy":"easy_car_high_score", "car_hard":"hard_car_high_score", "snake":"snake_high_score"}.get(kind)
    if not col: return jsonify(msg="bad kind"), 400
    with db() as conn, conn.cursor() as c:
        c.execute(f"select user_name, COALESCE({col},0) as s from main_game order by s desc limit 50")
        rows = c.fetchall()
    return jsonify([{"user_name": r[0], "score": int(r[1] or 0)} for r in rows])
