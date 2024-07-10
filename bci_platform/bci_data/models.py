from django.db import models

class BCISession(models.Model):
    session_name = models.CharField(max_length=100)
    date_recorded = models.DateTimeField()
    subject_id = models.CharField(max_length=50)
    
    def __str__(self):
        return f"{self.session_name} - {self.subject_id}"

class BCIData(models.Model):
    session = models.ForeignKey(BCISession, on_delete=models.CASCADE, related_name='data_points')
    timestamp = models.DateTimeField()
    channel_1 = models.FloatField()
    channel_2 = models.FloatField()
    channel_3 = models.FloatField()
    channel_4 = models.FloatField()
    
    def __str__(self):
        return f"Data point for {self.session} at {self.timestamp}"