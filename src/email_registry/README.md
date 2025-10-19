# Django App for Email Preview

This app is lightly modified from the original [django-email-testview](https://pypi.org/project/django-email-testview/) app.

* The layout of templates for bodies and subjects has been relaxed.
  * Instead the subject can be directly specified.
  * Or the subject template is assumed to have a suffix of "***_subject***"
