=====
Facebook Messenger Bot : fbbot
=====

fbbot is a simple Django app to showcasing the Messenger Platform, make your facebook bot with django

Quick start
-----------

0. If yo don't have a https server and domain. For development purposes I use NGROK, a good "Secure tunnels to localhost" service ( url:https://ngrok.com/ )::

   > Download ngrok binary https://ngrok.com/download
   > execute ./ngrok http 8000
   > Copy url like '12345678.ngrok.io'

1. Clone this repo and install the requeriments::

    git clone https://github.com/espacioAntonio/Django-messenger-platform-bot.git
    cd Django-messenger-platform-bot
    pip install -r requirements.txt

2. Add your valid settings in ./fbbot/settings.py::

    FB_PAGE_TOKEN = "FACEBOOK_PAGE_TOKEN"
    FB_VERIFY_TOKEN = "VERIFY_TOKEN_DEFINED_BY_DEVELOPER"
    REAL_URL = "URL_PROVIDED_BY_NGROK" #example: 12346578.ngrok.io or www.yourdomain.com

3. Run::
    python manage.py runserver 8000

4. Suscribe your new webhook in your Facebook App::

    WEBHOOK
    URL Callback: https://YOUR_REAL_URL/fbbot/webhook
    Verify Token: "VERIFY_TOKEN_DEFINED_BY_DEVELOPER"

5. Visit http://127.0.0.1:8000/fbbot/webhook and see "Hello World, webhook enable" message.

6. Send a message to your facebook page or send this messages::

    image
    gif
    audio
    file
    button
    generic
    receipt
    quick reply
    read receipt
    typing on
    typing off
    account linking

Integrate this app with your Django App
-----------

1. Install the django-fbbot package with python-pip::

    pip install django-fbbot

1.1. If you want to uninstall this package run::

    pip uninstall django-fbbot

2. Add your valid tokens in your settings file mysite/settings.py::

    FB_PAGE_TOKEN = "FACEBOOK_PAGE_TOKEN"
    FB_VERIFY_TOKEN = "VERIFY_TOKEN_DEFINED_BY_DEVELOPER"
    REAL_URL = "URL_PROVIDED_FOR_NGROK" #example: 12346578.ngrok.io or www.yourdomain.com
    BASE_URL = "https://"+REAL_URL

CONFIGURE YOUR DJANGO APP

3. Add "fbbot" to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = [
        ...
        'fbbot',
    ]

4. Include the fbbot URLconf in your project urls.py like this::

    url(r'^fbbot/', include('fbbot.urls')),

5. Run `python manage.py collectstatic` to collect files to test.

6. Start the development server and visit http://127.0.0.1:8000/fbbot/webhook

7. Visit http://127.0.0.1:8000/fbbot/webhook and see "Hello World, webhook enable"

8. Send a message to your facebook page or send this messages::

    image
    gif
    audio
    file
    button
    generic
    receipt
    quick reply
    read receipt
    typing on
    typing off
    account linking
