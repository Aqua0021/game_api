from flask import Flask, request, jsonify
from game_api.db_config import get_connection
import psycopg2.extras  # for RealDictCursor

app = Flask(__name__)

@app.route('/')
def home():
    return "✅ Flask Game API is running!"

# ---------------- REGISTER ROUTE ----------------
@app.route('/register', methods=['POST'])
def register():
    data = request.json
    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        return jsonify({"status": "fail", "message": "Username and password required"})

    db = get_connection()
    cursor = db.cursor()

    cursor.execute("SELECT * FROM main_game WHERE user_name = %s", (username,))
    if cursor.fetchone():
        cursor.close()
        db.close()
        return jsonify({"status": "fail", "message": "Username already exists"})

    cursor.execute("INSERT INTO main_game (user_name, password) VALUES (%s, %s)", (username, password))
    db.commit()
    cursor.close()
    db.close()

    return jsonify({"status": "ok", "message": "Account created successfully"})


# ---------------- LOGIN ROUTE ----------------
@app.route('/login', methods=['POST'])
def login():
    data = request.json
    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        return jsonify({"status": "fail", "message": "Username and password required"})

    db = get_connection()
    cursor = db.cursor(cursor_factory=psycopg2.extras.RealDictCursor)  # ✅ PostgreSQL dict cursor

    cursor.execute("SELECT * FROM main_game WHERE user_name = %s AND password = %s", (username, password))
    user = cursor.fetchone()

    cursor.close()
    db.close()

    if user:
        return jsonify({"status": "ok", "message": "Login successful"})
    else:
        return jsonify({"status": "fail", "message": "Invalid username or password"})


# ---------------- UPDATE SCORE ROUTE ----------------
@app.route('/update_score', methods=['POST'])
def update_score():
    data = request.json
    username = data.get("username")
    game = data.get("game")  
    score = data.get("score")

    if not username or not game or score is None:
        return jsonify({"status": "fail", "message": "Username, game, and score required"})

    game_columns = {
        "hard_car": "hard_car_high_score",
        "easy_car": "easy_car_high_score",
        "snake": "snake_high_score"
    }

    if game not in game_columns:
        return jsonify({"status": "fail", "message": "Invalid game type"})

    column_name = game_columns[game]

    db = get_connection()
    cursor = db.cursor()

    cursor.execute(f"SELECT {column_name} FROM main_game WHERE user_name = %s", (username,))
    result = cursor.fetchone()

    if result:
        current_score = result[0] or 0
        if score > current_score:
            cursor.execute(f"UPDATE main_game SET {column_name} = %s WHERE user_name = %s", (score, username))
            db.commit()
            message = "Score updated"
        else:
            message = "Score not updated (lower than current)"
    else:
        message = "User not found"

    cursor.close()
    db.close()
    return jsonify({"status": "ok", "message": message})


# ---------------- GET SCORES ROUTE ----------------
@app.route('/get_scores', methods=['GET'])
def get_scores():
    game = request.args.get("game")

    if not game:
        return jsonify({"status": "fail", "message": "Game type required"})

    game_columns = {
        "hard_car": "hard_car_high_score",
        "easy_car": "easy_car_high_score",
        "snake": "snake_high_score"
    }

    if game not in game_columns:
        return jsonify({"status": "fail", "message": "Invalid game type"})

    column_name = game_columns[game]

    db = get_connection()
    cursor = db.cursor(cursor_factory=psycopg2.extras.RealDictCursor)  # ✅ PostgreSQL dict cursor

    cursor.execute(f"SELECT user_name, {column_name} as score FROM main_game ORDER BY {column_name} DESC LIMIT 10")
    scores = cursor.fetchall()

    cursor.close()
    db.close()
    return jsonify({"status": "ok", "scores": scores})


if __name__ == '__main__':
    app.run(debug=True)
