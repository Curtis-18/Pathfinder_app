from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from django.http import JsonResponse
import google.generativeai as genai
import json
import os
from django.conf import settings
from .models import ChatHistory
from django.views.decorators.http import require_GET
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.shortcuts import redirect
from django.db.models import Max

# Configure Gemini for Pathfinder Job Finder AI
SYSTEM_PROMPT = (
    "You are Pathfinder, an expert AI assistant for job seekers. "
    "You provide career guidance, help users edit and design modern CVs and resumes, "
    "and recommend available jobs in their area. "
    "If a user asks for a job search, ask for their location and skills if not provided. "
    "For CV/resume help, offer actionable suggestions and modern formatting tips. "
    "For career advice, be supportive and insightful. "
    "If you have access to external data (RAG), use it to provide up-to-date job listings."
)

genai.configure(api_key=settings.GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-1.5-flash")

@csrf_exempt
def chatbot_view(request):
    username = request.user.username if request.user.is_authenticated else None
    if request.method == "POST":
        data = json.loads(request.body)
        user_message = data.get("message", "")
        message_lower = user_message.lower()
        session_id = request.session.session_key
        if not session_id:
            request.session.create()
            session_id = request.session.session_key
        unrelated_keywords = [
            "hungry", "food", "eat", "lonely", "relationship", "love", "bored", "weather", "music", "movie", "game", "sports",
            "travel", "holiday", "vacation", "pet", "dog", "cat", "party", "birthday", "dream", "story", "joke", "funny", "hobby"
        ]
        if any(word in message_lower for word in unrelated_keywords):
            user_message = (
                f"The user said: '{user_message}'. "
                "Please respond in a fun, engaging, or creative way that gently brings the conversation back to jobs, careers, or professional development. "
                "You can use humor, analogies, or interesting facts to make the transition smooth and enjoyable. "
                "For example, if the user tells a story about their pet, you might mention animal-related careers or how caring for pets can build responsibility for the workplace. "
                "If the user talks about travel, relate it to travel jobs or skills gained from exploring new places. "
                "Always keep the tone friendly and supportive!"
            )
        # --- Conversational flow: use chat history for context ---
        # Fetch last 5 exchanges for this session
        history_qs = ChatHistory.objects.filter(session_id=session_id).order_by('-timestamp')[:5][::-1]
        history = []
        for h in history_qs:
            history.append(f"User: {h.user_message}\nAI: {h.bot_reply}")
        # Add current user message
        history.append(f"User: {user_message}")
        # Compose prompt
        prompt = f"{SYSTEM_PROMPT}\n" + "\n".join(history)
        chat = model.start_chat(history=[])
        response = chat.send_message(prompt)
        bot_reply = response.text
        # Store chat history
        ChatHistory.objects.create(
            session_id=session_id,
            user_message=user_message,
            bot_reply=bot_reply
        )
        return JsonResponse({"reply": bot_reply, "username": username})
    return render(request, "chatbot/chat.html", {"username": username})

@require_GET
def chat_history_view(request):
    session_id = request.GET.get('session_id') or request.session.session_key
    if not session_id:
        return JsonResponse({"history": []})
    history = ChatHistory.objects.filter(session_id=session_id).order_by("timestamp")
    history_data = [
        {"user_message": h.user_message, "bot_reply": h.bot_reply, "timestamp": h.timestamp} for h in history
    ]
    return JsonResponse({"history": history_data})

@csrf_protect
def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('chatbot')
        else:
            return render(request, "chatbot/login.html", {"error": "Invalid username or password."})
    return render(request, "chatbot/login.html")

@csrf_protect
def signup_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password1 = request.POST.get("password1")
        password2 = request.POST.get("password2")
        if password1 != password2:
            return render(request, "chatbot/signup.html", {"error": "Passwords do not match."})
        if User.objects.filter(username=username).exists():
            return render(request, "chatbot/signup.html", {"error": "Username already exists."})
        user = User.objects.create_user(username=username, password=password1)
        login(request, user)
        return redirect('chatbot')
    return render(request, "chatbot/signup.html")


@require_GET
def chat_sessions_view(request):
    if not request.user.is_authenticated:
        return JsonResponse({"sessions": []})
    # Get all session_ids for this user (by username in chat history)
    sessions = (
        ChatHistory.objects
        .filter(bot_reply__icontains=request.user.username)
        .values('session_id')
        .annotate(last_time=Max('timestamp'))
        .order_by('-last_time')
    )
    session_list = [s['session_id'] for s in sessions]
    return JsonResponse({"sessions": session_list})
