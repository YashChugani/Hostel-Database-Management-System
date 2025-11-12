import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text
from dotenv import load_dotenv

load_dotenv()
db = SQLAlchemy()

def create_app():
    app = Flask(__name__, static_folder="static", template_folder="templates")

    db_user = os.getenv('DATABASE_USER')
    db_pass = os.getenv('DATABASE_PASS')
    db_host = os.getenv('DATABASE_HOST', 'localhost')
    db_name = os.getenv('DATABASE_NAME')

    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'devkey')
    app.config['SQLALCHEMY_DATABASE_URI'] = f"mysql+pymysql://{db_user}:{db_pass}@{db_host}/{db_name}"
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    # Register blueprints
    from app.routes import main_bp
    app.register_blueprint(main_bp)


    @app.route('/')
    def home():
        return "<h2>Hostel Management Flask App is running — go to /students or /rooms</h2>"

    return app





# import os
# from flask import Flask
# from flask_sqlalchemy import SQLAlchemy
# from dotenv import load_dotenv

# load_dotenv()  # reads .env

# db = SQLAlchemy()

# def create_app():
#     app = Flask(__name__, static_folder="static", template_folder="templates")

#     # Config from environment variables
#     db_user = os.getenv('DATABASE_USER')
#     db_pass = os.getenv('DATABASE_PASS')
#     db_host = os.getenv('DATABASE_HOST', 'localhost')
#     db_name = os.getenv('DATABASE_NAME')

#     app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'devkey')
#     # Use pymysql driver
#     app.config['SQLALCHEMY_DATABASE_URI'] = f"mysql+pymysql://{db_user}:{db_pass}@{db_host}/{db_name}"
#     app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

#     db.init_app(app)

#     # Register a simple route to test DB connectivity
#     @app.route('/')
#     def home():
#         return "Flask app is running. Go to /testdb to verify DB."

#     @app.route('/testdb')
#     def testdb():
#         # run a simple raw SQL query against your Students table
#         try:
#             result = db.session.execute("SELECT COUNT(*) FROM Students;")
#             count = result.scalar()  # number of rows in Students
#             return {"students_count": int(count)}
#         except Exception as e:
#             # return error so we can debug if connection/SQL fails
#             return {"error": str(e)}

#     return app
