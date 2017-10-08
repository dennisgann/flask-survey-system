from routes import app, db, system
db.create_all()
print("Importing changes from csv files. This may take a while...")
system.csv_import()
print("Import complete")
app.run(debug=True, port=1234)
