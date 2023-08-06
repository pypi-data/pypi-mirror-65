from django.test import TestCase
from .models import ClientTrace, LoginTimes
import time
from datetime import timedelta, datetime
import pytz


# Create your tests here.
class LoginTimeTestCase(TestCase):
    def setUp(self):
        ClientTrace.objects.create(sessionID='ABCD',
                                   ip_address='',
                                   city='',
                                   region='',
                                   country='',
                                   latitude=0,
                                   longitude=0)
        ClientTrace.objects.create(sessionID='XYZ',
                                   ip_address='',
                                   city='',
                                   region='',
                                   country='',
                                   latitude=0,
                                   longitude=0)
        ClientTrace.objects.create(sessionID='JKL',
                                   ip_address='',
                                   city='',
                                   region='',
                                   country='',
                                   latitude=0,
                                   longitude=0)

    def test_new_login(self):
        client_1 = ClientTrace.objects.get(sessionID='ABCD')
        a = LoginTimes.objects.create(client=client_1)
        self.assertEquals(LoginTimes.objects.filter(client=client_1).count(), 1)

    def test_relogin_in_few_sec(self):
        client_1 = ClientTrace.objects.get(sessionID='XYZ')
        a = LoginTimes.objects.create(client=client_1)
        self.assertEquals(LoginTimes.objects.filter(client=client_1).count(), 1)
        time.sleep(5)
        b = LoginTimes.objects.create(client=client_1)
        print(a, b)
        self.assertEquals(LoginTimes.objects.filter(client=client_1).count(), 1)
        self.assertEquals(a.start_time, b.start_time)

    def test_relogin_after_30_mins(self):
        client_1 = ClientTrace.objects.get(sessionID='JKL')
        a = LoginTimes.objects.create(client=client_1)
        now = datetime.now(pytz.utc)
        temp_save = a.save
        def save(self, *args, **kwargs):
            self.start_time = now-timedelta(hours=1)
            self.end_time = now-timedelta(minutes=45)
            return super(LoginTimes, self).save(*args, **kwargs)
        a.save = save
        a.save(a)
        a.save = temp_save

        self.assertEquals(LoginTimes.objects.filter(client=client_1).count(), 1)
        b = LoginTimes.objects.create(client=client_1)
        self.assertEquals(LoginTimes.objects.filter(client=client_1).count(), 2)
        self.assertNotEquals(a.start_time, b.start_time)