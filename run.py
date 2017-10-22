from routes import app, db, system
db.create_all()
print("Importing changes from csv files. This may take a while...")
system.csv_import()
print("Import complete")
system.create_user(1, "admin", "password", 3)
app.run(debug=True, port=80)
