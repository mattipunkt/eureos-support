# simpletix
this is a simple ticket system written in python using the django web framework.

### email-support
create a ```.env```file in the root of your folder and paste the following text:
```env
# EMAIL-CONFIGURATION
SMTP_SERVER=
SMTP_USER=
SMTP_PASSWORD=

# WILL BE DISPLAYED IN THE EMAIL-URLS
HOST_URL=http://localhost:8000
```
enter the urls for your specific setup. also, when running in production, change the host-url. 