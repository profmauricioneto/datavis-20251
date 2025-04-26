from pages.home import register_home_callbacks
from pages.trends import register_trends_callbacks
from pages.types import register_types_callbacks

def register_callbacks(app):
    register_home_callbacks(app)
    register_trends_callbacks(app)
    register_types_callbacks(app)