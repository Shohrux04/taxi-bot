from . import start
from . import register
from . import client
from . import driver

routers = [
    start.router,
    register.router,
    client.router,
    driver.router
]