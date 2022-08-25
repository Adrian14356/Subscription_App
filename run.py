import os
from app.constants import DB_PATH
from app import create_app, db
from app.models import Subscriptions
from app.schema import SubscriptionsPricesSchema, SubscriptionsSchema

def create_db(app):
    with app.app_context():
        if not os.path.exists(DB_PATH):
            db.create_all()

if __name__ == "__main__":
    app = create_app()
    app.secret_key = "secret_key"
    create_db(app)
    app.run(host = "127.0.0.1", port = 5005, debug = True)