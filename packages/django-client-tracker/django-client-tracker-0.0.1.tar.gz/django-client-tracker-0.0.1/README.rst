=====
Client Tracker
=====

Client Tracker is a Django app to keep track of clients visiting your website. 
Client IP, and location is fetched using a client-side script. Every 10 minutes
the script pings the server to inform that the client is still on the site.

Detailed documentation is in the "docs" directory.

Quick start
-----------

1. Add "clienttracker" to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = [
        ...
        'clienttracker',
    ]

2. Include the clienttracker URLconf in your project urls.py like this::

    path('ticker/', include('clienttracker.urls'))

3. Run ``python manage.py migrate`` to create the clienttracker models.

4. Include tracer.js in base.html at the bottom of the page. If you do not use base.html you will need
   to include the js in every html file separately.
   
   <script src="{% static 'js/tracer.js' %}"></script>

4. Start the development server and visit http://127.0.0.1:8000/. 