# import os
# from django.core.wsgi import get_wsgi_application

# # Check for the PRODUCTION environment variable to see if we are running in Azure App Service
# # If so, then load the settings from production.py
# settings_module = 'price_tracker.production' if 'PRODUCTION' in os.environ else 'price_tracker.settings'
# os.environ.setdefault('DJANGO_SETTINGS_MODULE', settings_module)


# application = get_wsgi_application()

#!/usr/bin/env python


# application = get_wsgi_application()

#!/usr/bin/env python



"""Django's command-line utility for administrative tasks."""
import os
import sys



def main():
    """Run administrative tasks."""
    settings_module = 'price_tracker.production' if 'WEBSITE_HOSTNAME' in os.environ else 'price_tracker.settings'
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', settings_module)
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()

 