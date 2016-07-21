from famous_people import app
from famous_people.views import db

if __name__ == '__main__':
    db.create_all()
    app.run()
