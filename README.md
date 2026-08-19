# 🤖 Memory-Based Chatbot using Flask & Ollama

A simple **AI-powered memory-based chatbot** developed using **Python Flask** and **Ollama Llama 3.2**.
The chatbot can remember previous conversations and provide responses based on the stored conversation history.

## 📌 Features

* 🤖 AI chatbot using **Llama 3.2**
* 🧠 Memory-based conversation
* 💬 Chat interface built with **Bootstrap**
* 🗃️ Conversation data stored locally
* 🐍 Python Flask backend
* 📱 Responsive chatbot interface
* 🔘 Floating chatbot icon at the bottom-right corner
* 🔄 Maintains conversation context during the session
* 💾 SQLite database support
* 📄 JSON data storage

## 🛠️ Technologies Used

* **Python**
* **Flask**
* **Ollama**
* **Llama 3.2**
* **SQLite**
* **HTML5**
* **Bootstrap**
* **JSON**

## 📂 Project Structure

```text
session3/
│
├── app.py
├── data.json
├── db.sqlite
├── requirements.txt
│
└── templates/
    └── index.html
```

### 📄 File Description

| File                   | Description                             |
| ---------------------- | --------------------------------------- |
| `app.py`               | Main Flask application                  |
| `data.json`            | Stores chatbot-related data             |
| `db.sqlite`            | SQLite database for conversation memory |
| `requirements.txt`     | Required Python packages                |
| `templates/index.html` | Chatbot user interface                  |

## ⚙️ Prerequisites

Before running the project, install:

1. **Python 3.9 or above**
2. **Ollama**
3. **Llama 3.2 model**
4. **VS Code** or another Python IDE

## 🐍 Step 1: Create a Virtual Environment

Open the project folder in VS Code terminal:

```bash
python -m venv venv
```

Activate the virtual environment.

### Windows

```bash
venv\Scripts\activate
```

### macOS/Linux

```bash
source venv/bin/activate
```

## 📦 Step 2: Install Dependencies

Run:

```bash
pip install -r requirements.txt
```

## 🦙 Step 3: Install Ollama

Install Ollama on your computer and then download the Llama 3.2 model.

Run:

```bash
ollama pull llama3.2:latest
```

Check that the model is available:

```bash
ollama list
```

You should see:

```text
llama3.2:latest
```

## ▶️ Step 4: Run the Flask Application

Make sure Ollama is running.

Then execute:

```bash
python app.py
```

If everything is configured correctly, Flask will display something similar to:

```text
Running on http://127.0.0.1:5000/
```

Open your browser and visit:

```text
http://127.0.0.1:5000/
```

## 💬 How the Chatbot Works

The basic workflow is:

```text
User
  ↓
Chatbot Interface
  ↓
Flask Application
  ↓
Retrieve Previous Conversation
  ↓
Ollama Llama 3.2
  ↓
Generate Response
  ↓
Store Conversation
  ↓
Display Response
```

The chatbot retrieves previous conversation information and sends the relevant context to the Llama 3.2 model. This allows the chatbot to provide more context-aware responses.

## 🧠 Memory System

The chatbot uses local storage to maintain conversation information.

SQLite can be used to store:

* User messages
* Chatbot responses
* Conversation history
* Session information

Example:

```text
User: My name is Rahul.

Bot: Nice to meet you, Rahul!

User: What is my name?

Bot: Your name is Rahul.
```

## 🌐 User Interface

The application contains:

* Home page
* Floating chatbot button
* Chatbot window
* Message input field
* Send button
* Conversation display

The interface uses **Bootstrap** for styling and interactions.

## 🔧 Troubleshooting

### Ollama model not found

Run:

```bash
ollama list
```

If `llama3.2:latest` is not available:

```bash
ollama pull llama3.2:latest
```

### Flask command not found

Make sure the virtual environment is activated and install Flask:

```bash
pip install flask
```

### Port already in use

Run Flask on another port, for example:

```python
app.run(debug=True, port=5001)
```

Then open:

```text
http://127.0.0.1:5001/
```

### Python is not recognized

Check Python installation:

```bash
python --version
```

If that doesn't work on Windows, try:

```bash
py --version
```

## 🚀 Future Enhancements

The project can be extended with:

* 👤 User login and registration
* 🔐 Authentication
* 🗂️ Multiple chat sessions
* 🧹 Clear conversation option
* 📊 Chat history dashboard
* 🎤 Voice input
* 🔊 Text-to-speech
* 🌍 Multilingual chatbot
* ☁️ Cloud database
* 🌐 Online deployment

## 📜 License

This project is created for **educational and academic purposes**.

You are free to modify and extend the project for learning and college project demonstrations.

## 👨‍💻 Author

**BCA Department**

Developed as an educational project demonstrating:

**Flask + Ollama + Llama 3.2 + SQLite + Bootstrap**
