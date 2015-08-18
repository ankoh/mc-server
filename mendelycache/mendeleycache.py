from flask import Flask

from mendelycache.blueprints.fields.blueprint import blueprint as fields
from mendelycache.blueprints.profiles.blueprint import blueprint as profiles
from mendelycache.blueprints.publications.blueprint import blueprint as publications
from mendelycache.blueprints.statistics.blueprint import blueprint as statistics
from mendelycache.blueprints.system.blueprint import blueprint as system

app = Flask(__name__)

# Blueprints
app.register_blueprint(fields, url_prefix='/fields')
app.register_blueprint(profiles, url_prefix='/profiles')
app.register_blueprint(publications, url_prefix='/publications')
app.register_blueprint(statistics, url_prefix='/statistics')
app.register_blueprint(system, url_prefix='/system')

# Main entry point
if __name__ == '__main__':
    app.run()
