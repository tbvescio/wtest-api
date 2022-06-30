from sqlalchemy import true
from src import create_app

application = create_app()
application.run(debug=True)