import sentiment_service.app
from models import db
from routes import create_app
from sqlalchemy.exc import OperationalError
from sqlalchemy import text

app = create_app()

with app.app_context():
    try:
        db.session.execute(text('SELECT 1'))
        print("DB connection was successful")
    except OperationalError as e:
        print(f"DB connection error: {str(e)}")
        exit(1)

with app.app_context():
    try:
        #db.drop_all()
        db.create_all()
        print("Tables created successfully")
    except Exception as e:
        print(f"Error creating tables: {str(e)}")
with app.app_context():
    try:
        sentiment_service.app.initialize_model()
    except Exception as e:
        print(f"Error at loading the sentiments service")
if __name__ == '__main__':
    app.run(debug=True)
