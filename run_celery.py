from celery_app import Celery
app = Celery('celery_app')
app.config_from_object('celery.celery_config.CeleryConfig')

if __name__ == '__main__':
    app.start()