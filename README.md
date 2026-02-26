# 🧭 Pathfinder AI — Career Assistant Chatbot

> **🏆 Hackathon Project — 3rd Place**

Pathfinder AI is an intelligent career assistant chatbot built with Django and powered by Google Gemini 1.5 Flash. It helps job seekers with career guidance, CV/resume writing tips, interview preparation, and personalized job recommendations — all through a sleek, animated conversational interface.

---

## ✨ Features

- 🤖 **AI-Powered Career Assistant** — Leverages Google Gemini 1.5 Flash to provide expert career guidance, CV advice, and job search help
- 💬 **Persistent Chat History** — Conversations are saved per session so context is maintained across messages
- 🕒 **Session History Browser** — A slide-out drawer lets users browse and reload previous chat sessions
- 🔐 **User Authentication** — Full signup and login system so users get personalized, consistent experiences
- 📎 **File Upload Support** — Users can upload files (e.g., CVs) via the `/upload/` endpoint
- 🎨 **Animated Chat UI** — Glassmorphism-inspired design with floating particles, typing indicators, and smooth message animations
- 📱 **Responsive Design** — Fully mobile-friendly layout

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| Backend Framework | Django 4.2 |
| AI Model | Google Gemini 1.5 Flash (`google-generativeai`) |
| Database | SQLite3 |
| Frontend | Vanilla HTML, CSS, JavaScript |
| Auth | Django's built-in authentication system |
| Env Management | `python-dotenv` |

---

## 📁 Project Structure

```
Pathfinder_app/
└── Pathfinder1/                    # Django project root
    ├── manage.py
    ├── db.sqlite3                  # SQLite database
    ├── media/                      # Uploaded files
    ├── Pathfinder1/                # Project configuration
    │   ├── settings.py
    │   ├── urls.py
    │   ├── wsgi.py
    │   ├── asgi.py
    │   └── .env                    # Environment variables (see setup)
    └── chatbot/                    # Main application
        ├── models.py               # ChatHistory model
        ├── views.py                # All view logic (chat, auth, history)
        ├── urls.py                 # URL routing
        ├── admin.py                # Django admin registration
        ├── migrations/             # Database migrations
        └── templates/chatbot/
            ├── chat.html           # Main chat interface
            ├── login.html          # Login page
            └── signup.html         # Sign-up page
```

---

## 🚀 Getting Started

### Prerequisites

- Python 3.10+
- A [Google Gemini API key](https://aistudio.google.com/app/apikey)

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/pathfinder-ai.git
cd pathfinder-ai
```

### 2. Create and Activate a Virtual Environment

```bash
python -m venv venv
source venv/bin/activate        # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install django google-generativeai python-dotenv
```

### 4. Configure Environment Variables

Create a `.env` file inside the `Pathfinder1/Pathfinder1/` directory:

```
GEMINI_API_KEY=your_gemini_api_key_here
```

> ⚠️ **Never commit your `.env` file.** Add it to `.gitignore`.

### 5. Apply Migrations

```bash
cd Pathfinder1
python manage.py migrate
```

### 6. (Optional) Create a Superuser for Admin Access

```bash
python manage.py createsuperuser
```

### 7. Run the Development Server

```bash
python manage.py runserver
```

The app will be available at **http://127.0.0.1:8000/**

---

## 🌐 URL Routes

| URL | Name | Description |
|---|---|---|
| `/` | `chatbot` | Main chat interface |
| `/login/` | `login` | User login page |
| `/signup/` | `signup` | User sign-up page |
| `/history/` | `chat_history` | JSON API: fetch session chat history |
| `/sessions/` | `chat_sessions` | JSON API: list previous sessions |
| `/upload/` | `upload_file` | File upload endpoint |
| `/admin/` | — | Django admin panel |

---

## 🤖 How the AI Works

Pathfinder uses a custom **system prompt** that instructs Gemini to act as an expert career assistant named "Pathfinder". Its specialties include:

- **Job search guidance** — asks for location and skills to tailor recommendations
- **CV/Resume help** — offers actionable, modern formatting tips
- **Career advice** — supportive and insightful responses
- **Topic steering** — if a user veers off-topic (e.g., food, travel, pets), Pathfinder creatively bridges the conversation back to careers

The last **5 exchanges** from the current session are included in every prompt to maintain conversation context (retrieval-augmented history).

---

## 🗄️ Database Model

### `ChatHistory`

| Field | Type | Description |
|---|---|---|
| `session_id` | `CharField` | Links messages to a browser session |
| `user_message` | `TextField` | The user's input |
| `bot_reply` | `TextField` | Gemini's response |
| `timestamp` | `DateTimeField` | Auto-set when message is created |

---

## 🖼️ UI Highlights

- **Animated gradient background** with floating particle effects
- **Glassmorphism** chat card with blur and shadow
- **Typing indicator** (animated bouncing dots) while waiting for AI response
- **Slide-out drawer** for browsing previous sessions
- **Message bubbles** styled differently for user vs. AI
- **Enter key** support for sending messages

---

## 🔒 Security Notes

> Before deploying to production, make the following changes in `settings.py`:

- Set `DEBUG = False`
- Set a secure `SECRET_KEY` (do not use the default)
- Configure `ALLOWED_HOSTS` with your domain
- Use a production-grade database (e.g., PostgreSQL)
- Set up HTTPS

---

## 👥 Team

Built during a hackathon. **3rd place finish!** 🥉

| Role | Contributor |
|---|---|
| Backend & AI Integration | Curtis |
| Collaboration & Features | Kokole Wahid |

---


