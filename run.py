from app import app
from app.database import create_table

if __name__ == '__main__':
    create_table()
    app.run(debug=True)