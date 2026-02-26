from django.urls import path
from .views import chatbot_view, chat_history_view, login_view, signup_view, upload_file_view, chat_sessions_view

urlpatterns = [
    path('', chatbot_view, name='chatbot'),
    path('history/', chat_history_view, name='chat_history'),
    path('sessions/', chat_sessions_view, name='chat_sessions'),
    path('login/', login_view, name='login'),
    path('signup/', signup_view, name='signup'),
    path('upload/', upload_file_view, name='upload_file'),
]