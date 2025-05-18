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

## Step 3: Set Up the Database

### Create a PostgreSQL Database

**On Windows:**

```shellscript
# Open PostgreSQL command prompt (SQL Shell)
# Enter your PostgreSQL credentials when prompted

# Create a database
CREATE DATABASE agritech;

# Create a user (optional)
CREATE USER agritech_user WITH PASSWORD 'your_password';
GRANT ALL PRIVILEGES ON DATABASE agritech TO agritech_user;
```

**On macOS/Linux:**

```shellscript
# Access PostgreSQL command line
sudo -u postgres psql

# Create a database
CREATE DATABASE agritech;

# Create a user (optional)
CREATE USER agritech_user WITH PASSWORD 'your_password';
GRANT ALL PRIVILEGES ON DATABASE agritech TO agritech_user;

# Exit PostgreSQL
\q
```

### Initialize the Database Schema

```shellscript
# Run the schema SQL script
psql -U agritech_user -d agritech -f database/schema.sql

# If using the postgres user (on macOS/Linux)
sudo -u postgres psql -d agritech -f database/schema.sql
```

### 4. ## Run the Flask Backend

Navigate to the backend directory and run the Flask application:

```shellscript
# Navigate to the backend directory
cd backend

# Run the Flask application
python app.py
```

If you have a run.py file in the root directory, you can also use:

```shellscript
# From the project root
python run.py
```

You should see output indicating that the Flask server is running, typically on [http://localhost:5000](http://localhost:5000).


5. **Styling**:

1. Original: Tailwind CSS with shadcn/ui components
2. New: Custom CSS with similar styling





This conversion maintains the same functionality and database schema while using a more traditional tech stack with HTML, CSS, JavaScript, and Python.
