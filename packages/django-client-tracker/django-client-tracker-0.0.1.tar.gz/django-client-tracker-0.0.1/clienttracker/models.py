from django.db import models
from datetime import datetime, timedelta
import pytz


# Create your models here.
class ClientTrace(models.Model):
    sessionID = models.CharField(primary_key=True, auto_created=False, max_length=70)
    ip_address = models.CharField(max_length=50)
    city = models.CharField(max_length=70)
    region = models.CharField(max_length=50)
    country = models.CharField(max_length=50)
    latitude = models.FloatField()
    longitude = models.FloatField()


class LoginTimes(models.Model):
    client = models.ForeignKey(ClientTrace, on_delete=models.CASCADE)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()

    def save(self, *args, **kwargs):
        now = datetime.now(pytz.utc)
        obs = LoginTimes.objects.filter(client=self.client).order_by('-end_time')
        if len(obs) > 0:
            ob = obs[0]
            if ob.end_time > now - timedelta(minutes=30):
                ob.end_time = now
                self.pk = ob.pk
                self.client= ob.client
                self.start_time = ob.start_time
                self.end_time = ob.end_time
                super(LoginTimes, ob).save()
                return
        self.start_time = now
        self.end_time = now
        super(LoginTimes, self).save(*args, **kwargs)

    def __str__(self):
        return '"' + self.client.sessionID + '": ' + str(self.start_time) + ' -> ' + str(self.end_time) + ''
