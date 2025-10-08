from django.db import models
from django.contrib.auth.models import User

class GameMode(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    mode = models.CharField(max_length=50)  # 'easy', 'intermediate', 'hard'
    attempt = models.PositiveIntegerField()  # attempt number for the day
    created_at = models.DateTimeField(auto_now_add=True)
    date = models.DateField(auto_now_add=True)  # new field for daily grouping
    iq = models.FloatField(null=True, blank=True, help_text="Overall IQ for this attempt")

    class Meta:
        unique_together = ('user', 'date', 'attempt')  # enforces 1,2,3... per day

    def __str__(self):
        return f"{self.user.username} | {self.mode} | Attempt {self.attempt} | {self.date} | IQ: {self.iq}"


class GameQuestionRecord(models.Model):
    """
    Stores each question's details for a particular attempt.
    """
    game_mode = models.ForeignKey(GameMode, on_delete=models.CASCADE, related_name='questions')
    question_number = models.PositiveIntegerField(null=True, blank=True)  # optional for saving incomplete data
    time = models.PositiveIntegerField(null=True, blank=True, help_text="Time in seconds for this question")
    streak = models.PositiveIntegerField(default=0)  # usually 0 by default, no need for null
    user_answer = models.CharField(max_length=255, blank=True)  # blank allows empty string
    correct_answer = models.CharField(max_length=255, blank=True)
    status = models.CharField(
    max_length=20, 
    choices=[
        ('correct', 'Correct'),
        ('incorrect', 'Incorrect'),
        ('skipped', 'Skipped'),
    ],
    blank=True  # optional if status not yet set
) 

    class Meta:
        unique_together = ('game_mode', 'question_number')  
        ordering = ['question_number']

    def __str__(self):
        return f"{self.game_mode.user.username} | Q{self.question_number} | {self.status}"