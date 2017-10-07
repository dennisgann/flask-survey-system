from routes import app, db
app.run(debug=True, port=80)
db.create_all()
