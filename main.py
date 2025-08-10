import api.app as api
import db.session as db

if __name__ == "__main__":
    db.initConnection() 
    api.runApp()