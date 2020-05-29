import os
from app import create_app, db

# Import Schema in to current context for Migrate
from app.models.User import User
from app.models.Post import Post


app = create_app(os.getenv('FLASK_CONFIG') or 'default')



