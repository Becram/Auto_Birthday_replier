from routes import app
from models import db
db.create_all()
app.run(debug=True,port=8088,host='0.0.0.0')