import csv
from main import app, db, Exercise

db.create_all(app=app)

with open('/workspace/2602project/exercises.csv', 'r' ,encoding="windows-1252") as csvfile:
    reader = csv.DictReader(csvfile, delimiter= ',')

    for row in reader:
        data = Exercise(name= row['name'], difficulty= row['difficulty'], description= row['description'], 
        equipment_needed= row['equipment_needed'], equipment= row['equipment'], primary_muscle= row['primary_muscle'], 
        secondary_muscle= row['secondary_muscle'])
        
        db.session.add(data)


    db.session.commit()


print('database initialized!')