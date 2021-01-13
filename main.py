from app import app 
import views

if __name__ == '__main__':
    db.create_all()
    app.run()