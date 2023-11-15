from app.routes import app, connection_to_db
from app.database import create_table

if __name__ == '__main__':
    create_table(connection_to_db())
    app.run(debug=True)
