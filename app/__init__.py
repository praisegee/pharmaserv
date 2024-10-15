from flask import Flask

from .celery_config import celery_init_app
from .routes import main


def create_app():
    app = Flask(__name__)
    app.config.from_mapping(
        CELERY=dict(
            broker_url="redis://redis:6379",
            result_backend="redis://redis:6379",
            task_ignore_result=True,
        ),
    )
    app.register_blueprint(main)
    celery_app = celery_init_app(app)
    celery_app.set_default()

    return app, celery_app
