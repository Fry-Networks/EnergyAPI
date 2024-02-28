from celery import Celery
from celery import Task
from celery.schedules import crontab
import os
from flask import Flask
from flask_jwt_extended import JWTManager
from Energy.api.EnergyAPI import energy_api_v1

def CreateApp():
    print("Name: ", __name__)
    app = Flask(__name__)

    app.config.from_mapping(
        CELERY=dict(
            broker_url="redis://redis",
            result_backend="redis://redis",
            task_ignore_result=True,  
        ),
    )
    app.config.from_prefixed_env()
    CeleryInitApp(app)

    app.extensions["celery"].conf.beat_schedule = {
                                        "task-every-10-seconds": 
                                            {
                                                "task": "Energy.Tasks.BackgroundTasks.GetDevicesData",
                                                "schedule": crontab(minute="*/30"),
                                            }
                                    }

    @app.route("/")
    def index():
        return "HELLO"


    
    app.config["JWT_SECRET_KEY"] = "super-secret"  # Change this!
    jwt = JWTManager(app)

    app.register_blueprint(energy_api_v1)


    return app




def CeleryInitApp(app):
    class FlaskTask(Task):
        def __call__(self, *args: object, **kwargs: object):
            with app.app_context():
                return self.run(*args, **kwargs)
    print("app.name:", app.name)
    celery_app = Celery(app.name, task_cls=FlaskTask)
    celery_app.config_from_object(app.config["CELERY"])

    celery_app.set_default()

    app.extensions["celery"] = celery_app
    return celery_app