from mangum import Mangum
from sabermine_backend.api import app

handler = Mangum(app)
