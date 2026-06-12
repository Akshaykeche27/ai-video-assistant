from app import create_app,socketio

app=create_app()
 
# with app.app_context():  #temparoryly active flask app flask related thing can work
#     db.create_all()


if __name__=="__main__":
    socketio.run(app,debug=False) 