# Flask imports
from flask import Flask, request
from flask.ext.sqlalchemy import SQLAlchemy

# Controller imports
from mendeleycache.controllers.fields import FieldsController
from mendeleycache.controllers.profiles import ProfilesController
from mendeleycache.controllers.publications import PublicationsController
from mendeleycache.controllers.statistics import StatisticsController
from mendeleycache.controllers.system import SystemController


# Initialize the main application
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
db = SQLAlchemy(app)

# Create the controllers
fields_controller = FieldsController(app, db)
profiles_controller = ProfilesController(app, db)
publications_controller = PublicationsController(app, db)
statistics_controller = StatisticsController(app, db)
system_controller = SystemController(app, db)

# Register the url handlers
fields_controller.register()
profiles_controller.register()
publications_controller.register()
statistics_controller.register()
system_controller.register()


# If entry point run the application
if __name__ == '__main__':
    app.run(debug=True)
