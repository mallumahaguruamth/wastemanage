from flask import Flask, render_template, request, jsonify, session
import sqlite3
import json
import requests
import os

app = Flask(__name__)

# Secret key for Flask session
app.secret_key = "waste-management-chatbot-secret-key"

# File paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "db.sqlite")
DATA_PATH = os.path.join(BASE_DIR, "data.json")


# --------------------------------------------------
# DATABASE
# --------------------------------------------------

def init_database():
    connection = sqlite3.connect(DB_PATH)
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            session_id TEXT NOT NULL,
            role TEXT NOT NULL,
            message TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    connection.commit()
    connection.close()


def save_message(session_id, role, message):
    connection = sqlite3.connect(DB_PATH)
    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO messages (session_id, role, message)
        VALUES (?, ?, ?)
    """, (session_id, role, message))

    connection.commit()
    connection.close()


def get_memory(session_id, limit=10):
    connection = sqlite3.connect(DB_PATH)
    cursor = connection.cursor()

    cursor.execute("""
        SELECT role, message
        FROM messages
        WHERE session_id = ?
        ORDER BY id DESC
        LIMIT ?
    """, (session_id, limit))

    rows = cursor.fetchall()
    connection.close()

    rows.reverse()
    return rows


# --------------------------------------------------
# LOAD WASTE MANAGEMENT DATA
# --------------------------------------------------

def load_waste_data():
    try:
        with open(DATA_PATH, "r", encoding="utf-8") as file:
            return json.load(file)
    except Exception:
        return {}


waste_data = load_waste_data()


# --------------------------------------------------
# CREATE KNOWLEDGE CONTEXT
# --------------------------------------------------

def create_knowledge_context():
    context = ""

    for category, details in waste_data.items():
        context += f"\nCATEGORY: {category}\n"

        if isinstance(details, dict):
            for key, value in details.items():
                context += f"{key}: {value}\n"
        else:
            context += str(details) + "\n"

    return context


# --------------------------------------------------
# OLLAMA CHATBOT
# --------------------------------------------------

def ask_ollama(user_message, memory):

    memory_text = ""

    for role, message in memory:
        memory_text += f"{role.upper()}: {message}\n"

    knowledge = create_knowledge_context()

    prompt = f"""
You are EcoBot, a helpful Waste Management Assistant.

Your main purpose is to help users understand:

1. Waste management
2. Types of waste
3. Recycling
4. Reusable materials
5. Waste disposal
6. Composting
7. E-waste
8. Plastic waste
9. Organic waste
10. Recommendations
11. Suggestions for reducing waste
12. Environment-friendly practices

Use the waste-management knowledge provided below.

WASTE MANAGEMENT KNOWLEDGE:
{knowledge}

CONVERSATION MEMORY:
{memory_text}

USER QUESTION:
{user_message}

Instructions:

- Give simple and accurate answers.
- Keep answers easy for students and general users.
- If the user asks about a waste item, explain:
  Type:
  Can it be recycled?:
  How to dispose:
  Recommendation:
- Give practical suggestions.
- Do not invent recycling rules for a specific city.
- If information is not available, clearly say that local waste-management rules may differ.
- Remember previous messages in the conversation when useful.
- Stay focused on waste management and environmental topics.

Answer the user now.
"""

    try:
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": "llama3.2:latest",
                "prompt": prompt,
                "stream": False
            },
            timeout=120
        )

        if response.status_code != 200:
            return "Sorry, I could not connect to Ollama. Please make sure Ollama is running."

        result = response.json()

        return result.get(
            "response",
            "Sorry, I could not generate a response."
        )

    except requests.exceptions.ConnectionError:
        return (
            "Ollama is not running. Please start Ollama and make sure "
            "the llama3.2:latest model is installed."
        )

    except Exception as error:
        return f"Error connecting to Ollama: {error}"


# --------------------------------------------------
# HOME PAGE
# --------------------------------------------------

@app.route("/")
def home():

    if "session_id" not in session:
        import uuid
        session["session_id"] = str(uuid.uuid4())

    return render_template("index.html")


# --------------------------------------------------
# CHAT API
# --------------------------------------------------

@app.route("/chat", methods=["POST"])
def chat():

    if "session_id" not in session:
        import uuid
        session["session_id"] = str(uuid.uuid4())

    session_id = session["session_id"]

    data = request.get_json()

    user_message = data.get("message", "").strip()

    if not user_message:
        return jsonify({
            "reply": "Please enter a question."
        })

    # Save user message
    save_message(
        session_id,
        "user",
        user_message
    )

    # Get previous conversation
    memory = get_memory(
        session_id,
        limit=10
    )

    # Generate chatbot response
    bot_response = ask_ollama(
        user_message,
        memory
    )

    # Save chatbot response
    save_message(
        session_id,
        "assistant",
        bot_response
    )

    return jsonify({
        "reply": bot_response
    })


# --------------------------------------------------
# CLEAR CHAT MEMORY
# --------------------------------------------------

@app.route("/clear", methods=["POST"])
def clear_chat():

    if "session_id" not in session:
        return jsonify({
            "message": "No chat memory found."
        })

    session_id = session["session_id"]

    connection = sqlite3.connect(DB_PATH)
    cursor = connection.cursor()

    cursor.execute("""
        DELETE FROM messages
        WHERE session_id = ?
    """, (session_id,))

    connection.commit()
    connection.close()

    return jsonify({
        "message": "Chat memory cleared."
    })


# --------------------------------------------------
# RUN APPLICATION
# --------------------------------------------------

if __name__ == "__main__":

    init_database()

    app.run(
        debug=True,
        host="127.0.0.1",
        port=5000
    )