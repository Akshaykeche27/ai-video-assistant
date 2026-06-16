from app import create_app,os

app=create_app()
 
# with app.app_context():  #temparoryly active flask app flask related thing can work
#     db.create_all()


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)