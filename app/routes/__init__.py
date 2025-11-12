from flask import Blueprint

main_bp = Blueprint('main', __name__)

from app.routes import students
from app.routes import rooms     
from app.routes import dashboard 

from app.routes import hostels
from app.routes import staff
from app.routes import allocations
from app.routes import fees
from app.routes import complaints
from app.routes import maintenance
from app.routes import visitors