from CeleryApp import celery, createApp

app = createApp()
app.app_context().push()