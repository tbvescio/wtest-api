import os

from src import create_app

application = create_app()
application.run(port=os.environ['PORT'])

