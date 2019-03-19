import os
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

from app import application, db
from .config import Config

application.config.from_object(Config)

application.config.from_object(Config)

migrate = Migrate(application, db)
manager = Manager(application)

manager.add_command('db', MigrateCommand)


if __name__ == '__main__':
    manager.run()