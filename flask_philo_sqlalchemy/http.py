from flask import current_app, _app_ctx_stack
from flask_philo_core import ConfigurationError
from flask_philo_core.views import BaseResourceView


class SQLAlchemyView(BaseResourceView):
    def __init__(self):
        self.app = current_app._get_current_object()
        if 'FLASK_PHILO_SQLALCHEMY' not in self.app.config:
            raise ConfigurationError(
                'Not configuration found for Flask-Philo-SQLAlchemy')
        ctx = _app_ctx_stack.top
        self.sqlalchemy_pool = ctx.sqlalchemy_pool
