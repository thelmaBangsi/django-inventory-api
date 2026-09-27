"""
ASGI config for config project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
<<<<<<< HEAD
<<<<<<< HEAD
https://docs.djangoproject.com/en/4.2/howto/deployment/asgi/
=======
https://docs.djangoproject.com/en/6.0/howto/deployment/asgi/
>>>>>>> fc9e15cac64e90c9743f8920246eede0efd88882
=======
https://docs.djangoproject.com/en/6.0/howto/deployment/asgi/
>>>>>>> fc9e15cac64e90c9743f8920246eede0efd88882
"""

import os

from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

application = get_asgi_application()
