from django.db import models

# Create your models here.

class ChatHistory(models.Model):
    session_id = models.CharField(max_length=128, db_index=True)
    user_message = models.TextField()
    bot_reply = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Session {self.session_id} at {self.timestamp}"  # For admin display
