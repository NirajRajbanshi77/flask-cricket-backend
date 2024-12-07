from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

# Create Flask app instance
app = Flask(__name__)

# Configure SQLite database URI
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Disable modification tracking (optional)
app.config['SECRET_KEY'] = 'your-secret-key'

# Initialize SQLAlchemy
db = SQLAlchemy(app)

# Enable CORS for the app (allow cross-origin requests)
CORS(app)

# Define User model (table) for SQLite
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)

    def __repr__(self):
        return f'<User {self.name}>'

# Create database tables (if they don't exist)
with app.app_context():
    db.create_all()

@app.route('/')
def home():
    return jsonify({"message": "Welcome to Cricket Analytics and Guide API!"})

# Registration Route
@app.route('/register', methods=['POST'])
def register():
    data = request.json
    # Check if all fields are provided
    if not data.get('name') or not data.get('email') or not data.get('password'):
        return jsonify({"message": "All fields (name, email, password) are required!"}), 400
    
    # Check if user already exists
    existing_user = User.query.filter_by(email=data['email']).first()
    if existing_user:
        return jsonify({"message": "User already exists!"}), 400

    # Create new user and add to the database
    new_user = User(name=data['name'], email=data['email'], password=data['password'])
    db.session.add(new_user)
    db.session.commit()

    return jsonify({"message": "User registered successfully!"}), 201

# Login Route
@app.route('/login', methods=['POST'])
def login():
    data = request.json
    # Check if email and password are provided
    if not data.get('email') or not data.get('password'):
        return jsonify({"message": "Both email and password are required!"}), 400
    
    # Find the user by email
    user = User.query.filter_by(email=data['email']).first()

    if user is None or user.password != data['password']:
        return jsonify({"message": "Invalid credentials!"}), 401
    
    return jsonify({"message": "Login successful!"}), 200

# Analyze Route (You can add your analysis logic here later)
@app.route('/analyze', methods=['POST'])
def analyze():
    # For now, just returning a placeholder message
    return jsonify({"message": "Analyze cricket shots (This is a placeholder)"})

# Run the app
if __name__ == '__main__':
    app.run(debug=True)
