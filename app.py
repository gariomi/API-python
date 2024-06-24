from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Record(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.String(200), nullable=False)

@app.route('/', methods=['GET'])
def home():
    return "Hello, World!"

@app.route('/echo', methods=['POST'])
def echo():
    data = request.json
    new_record = Record(data=str(data))
    db.session.add(new_record)
    db.session.commit()
    return jsonify(data), 201

@app.route('/records', methods=['GET'])
def get_records():
    records = Record.query.all()
    return jsonify([{"id": record.id, "data": record.data} for record in records])

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)

