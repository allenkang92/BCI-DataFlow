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
    

class Preprocessor(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class PreprocessingStep(models.Model):
    preprocessor = models.ForeignKey(Preprocessor, on_delete=models.CASCADE, related_name='steps')
    order = models.IntegerField()
    step_type = models.CharField(max_length=50)  # e.g., 'noise_removal', 'artifact_removal', etc.
    parameters = models.JSONField()

    def __str__(self):
        return f"{self.preprocessor.name} - Step {self.order}: {self.step_type}"

    class Meta:
        ordering = ['order']