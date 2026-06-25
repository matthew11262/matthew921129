from django.db import models

# 1. 遊戲狀態模型 (GameState)
class GameState(models.Model):
    direction = models.CharField(max_length=50, blank=True)
    key_height = models.CharField(max_length=50, blank=True)
    error_count = models.CharField(max_length=50, blank=True)
    freq = models.CharField(max_length=50, blank=True)
    rgb_color = models.CharField(max_length=50, blank=True)
    morse_code = models.CharField(max_length=50, blank=True)
    vault_knob = models.CharField(max_length=50, blank=True)
    keypad = models.CharField(max_length=50, blank=True)
    switch_state = models.CharField(max_length=50, blank=True)
    
    timestamp = models.DateTimeField(auto_now_add=True)
    is_latest = models.BooleanField(default=True)

    class Meta:
        ordering = ['-timestamp']

# 2. 按鈕模型 (ButtonData)
class ButtonData(models.Model):
    # 將 STATUS_CHOICES 定義在類別外面，或是放在該類別內部
    STATUS_CHOICES = [
        ('ON', 'On'),
        ('OFF', 'Off'),
    ]
    
    button_id = models.CharField(max_length=50, default='button_1')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES)
    timestamp = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_latest = models.BooleanField(default=False)

    class Meta:
        indexes = [
            models.Index(fields=['button_id', 'is_latest']),
            models.Index(fields=['timestamp']),
        ]
        ordering = ['-timestamp']

    def __str__(self):
        return f"{self.button_id} {self.status} @ {self.timestamp}"