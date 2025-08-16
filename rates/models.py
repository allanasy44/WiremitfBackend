from django.db import models
class Rate(models.Model):
    pair = models.CharField(max_length=20, db_index=True)
    rate = models.FloatField()
    sources = models.JSONField(default=dict)
    timestamp = models.DateTimeField(auto_now_add=True)
    class Meta: ordering=['-timestamp']
    def __str__(self): return f"{self.pair} - {self.rate} @ {self.timestamp.isoformat()}"
