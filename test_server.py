from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config.Config import Config

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URL'] = "postgresql://{0}:{1}@localhost/{2}".format(Config.user, Config.password,
                                                                                    Config.database)
db = SQLAlchemy(app)


class Recipes(db.Model):
    __tablename__ = 'recipes'
    recipe_id = db.Column('recipe_id', db.Integer, primary_key=True)
    recipe_name = db.Column('recipe_name', db.Unicode)
    
    
recepies = Recipes().query.all()

print(recepies)
