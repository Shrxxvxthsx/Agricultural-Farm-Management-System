## How to Run the Project

### 1. Set Up the Environment

Create a `.env` file in the root directory with the following content:

```plaintext
FLASK_ENV=development
DATABASE_URL=postgresql://username:password@localhost:5432/agritech
```

### 2. Install Dependencies

```shellscript
# Create and activate a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install required packages
pip install flask flask-sqlalchemy flask-cors psycopg2-binary python-dotenv
```

### 3. Set Up the Database

```shellscript
# Create the database
createdb agritech

# Run the schema script
psql -d agritech -f database/schema.sql
```

### 4. Run the Application

```shellscript
# Start the Flask server
python backend/app.py
```

Visit `http://localhost:5000` in your browser to see the application.

## Key Differences from the Original Project

1. **Architecture**:

1. Original: Next.js with TypeScript, Server Components, and API Routes
2. New: Separate HTML/CSS/JS frontend with Python Flask backend



2. **Frontend**:

1. Original: React components with TypeScript
2. New: Plain HTML, CSS, and vanilla JavaScript



3. **Backend**:

1. Original: Next.js API Routes with TypeScript
2. New: Python Flask with SQLAlchemy



4. **Database Access**:

1. Original: Server Actions and API Routes
2. New: RESTful API endpoints in Flask



5. **Styling**:

1. Original: Tailwind CSS with shadcn/ui components
2. New: Custom CSS with similar styling





This conversion maintains the same functionality and database schema while using a more traditional tech stack with HTML, CSS, JavaScript, and Python.
