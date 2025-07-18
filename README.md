# 📚 GenAI Medical Assistant Documentation

Welcome to the **GenAI Medical Assistant**! This project is an end-to-end application that combines a **FastAPI backend** and a **Gradio frontend** to provide a seamless AI-powered medical assistant experience. The backend handles authentication and AI processing, while the frontend provides an interactive user interface for users to interact with the system.

---

## 🌟 Features
✅ **User Authentication** - Users can register and log in to access the AI Doctor functionality.

✅ **AI Doctor** - Users can record their medical concerns as audio, upload relevant medical images, and receive a diagnosis and suggested remedies from the AI Doctor.

✅ **Text-to-Speech** - Converts the AI Doctor's response into audio using ElevenLabs.

✅ **Dynamic Tab Navigation** - The AI Doctor tab is only accessible after a successful login.

✅ **Dockerized Deployment** - Both the backend and frontend are containerized for easy deployment.

---

## Project Structure
```plaintext
📂 GenAI_Medical_Assistant/
├── 📂 backend/                # FastAPI backend
│   ├── main.py                # FastAPI entry point
│   ├── requirements.txt       # Backend dependencies
│   ├── Dockerfile             # Dockerfile for backend
│   ├── 📂 auth/               # Authentication logic
│   │   ├── jwt.py             # JWT token generation and verification
│   │   ├── model.py           # SQLAlchemy models for user authentication
│   │   ├── utility.py         # Password hashing and verification
│   ├── 📂 routers/            # API routes
│   │   ├── users.py           # User authentication routes
│   │   ├── ai_doctor.py       # AI Doctor routes
│   └── 📂 database/           # Database-related files
│       ├── connection.py      # Database connection logic
│       └── migrations/        # Database migrations (if applicable)
│
├── 📂 frontend/               # Gradio frontend
│   ├── gradio_app.py          # Gradio app entry point
│   ├── requirements.txt       # Frontend dependencies
│   ├── Dockerfile             # Dockerfile for frontend
│   └── 📂 static/             # Static assets (if any)
│       ├── css/               # CSS files
│       └── js/                # JavaScript files
│
├── docker-compose.yml         # Docker Compose file for multi-container deployment
├── README.md                  # Project documentation
└── .env                       # Environment variables (optional)
```

---

## Technologies Used
### Backend:
- **FastAPI** - Backend framework for building APIs.
- **SQLAlchemy** - ORM for database interactions.
- **JWT** - Authentication using JSON Web Tokens.
- **Uvicorn** - ASGI server for running FastAPI.

### Frontend:
- **Gradio** - Interactive UI for user interaction.
- **Requests** - For communicating with the backend.

### Deployment:
- **Docker** - Containerization for backend and frontend.
- **Docker Compose** - Simplified multi-container deployment.

---

## ⚙️ Setup Guide

### Prerequisites
- **Python 3.9 or higher**
- **Docker** and **Docker Compose**
- **PostgreSQL** (if not using Docker for the database)

---

## ⚙️ Environment Variables and Database Configuration

### The .env file is used to store sensitive information like database credentials and API keys. Create a .env file in the root directory of the project with the following variables:

```plaintext
# GROQ API Key
GROQ_API_KEY=your_groq_api_key_here
# ElevenLabs API Key (for text-to-speech)
ELEVENLABS_API_KEY=your_elevenlabs_api_key_here

# Database Configuration
DB_USER=your_user_name
DB_PASSWORD=your_password
DB_HOST=db
DB_PORT=5432
DB_NAME=your_db_name

DATABASE_URL = "postgresql://your_user_name:your_password@localhost/your_db_name"
```
---

### Database Details
The application uses **PostgreSQL** as the database. Below are the details for setting up the database:

1. **Database Name**: `your_db_name`
2. **Database User**: `your_user_name`
3. **Database Password**: `your_password`
4. **Host**: `localhost` (or `postgres` if using Docker)
5. **Port**: `5432`

---

### Setting Up the Database
1. **Ensure PostgreSQL is Installed**:
   - Install PostgreSQL on your system or use Docker to run a PostgreSQL container.

2. **Create the Database**:
   - Log in to PostgreSQL:
     ```bash
     psql -U postgres
     ```
   - Run the following SQL commands:
     ```sql
     CREATE DATABASE your_db_name;
     CREATE USER your_user_name WITH PASSWORD 'your_password';
     GRANT ALL PRIVILEGES ON DATABASE your_db_name TO your_user_name;
     ```

3. **Verify the Database**:
   - Log in to the database:
     ```bash
     psql -U your_user_name -d your_db_name
     ```
   - Check the tables:
     ```sql
     \dt
     ```

---

### Backend Setup
1. **Navigate to the Backend Directory**:
   ```bash
   cd backend
   ```

2. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Set Up the Database**:
   - Ensure PostgreSQL is running.
   - Create a database and user:
     ```sql
     CREATE DATABASE voice_assistant_db;
     CREATE USER haseeb WITH PASSWORD 'securepass';
     GRANT ALL PRIVILEGES ON DATABASE voice_assistant_db TO haseeb;
     ```

4. **Run the Backend Locally**:
   ```bash
   uvicorn main:app --reload
   ```

5. **Access the API**:
   - Swagger UI: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

---

### Frontend Setup
1. **Navigate to the Frontend Directory**:
   ```bash
   cd frontend
   ```

2. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the Frontend Locally**:
   ```bash
   python gradio_app.py
   ```

4. **Access the Gradio App**:
   - Gradio UI: [http://127.0.0.1:7860](http://127.0.0.1:7860)

---

### Dockerized Deployment
1. **Build and Run with Docker Compose**:
   - Ensure you are in the root directory of the project.
   ```bash
   docker-compose up --build
   ```

2. **Access the Application**:
   - Backend: [http://localhost:8000/docs](http://localhost:8000/docs)
   - Frontend: [http://localhost:7860](http://localhost:7860)

---

## Application Workflow

### 1️⃣ **Login and Authentication**
- Users must log in to access the **AI Doctor** tab.
- If the user does not have an account, they can register using the **Register** tab.

### 2️⃣ **AI Doctor Functionality**
- After logging in, users can access the **AI Doctor** tab.
- The **AI Doctor** tab allows users to:
  1. **Record Audio**: Users can record their medical concerns as audio.
  2. **Upload Images**: Users can upload relevant medical images (e.g., X-rays, scans).
  3. **Submit Data**: The audio and image data are sent to the backend for processing.

### 3️⃣ **Backend Processing**
- The backend processes the audio and image data:
  1. **Audio Transcription**: The audio is transcribed into text using a speech-to-text model.
  2. **Image Analysis**: The uploaded image is analyzed using an AI model to detect medical issues.
  3. **Diagnosis and Suggestions**: The backend combines the transcribed text and image analysis to generate a diagnosis and suggest remedies or medications.

### 4️⃣ **AI Doctor Response**
- The backend sends the diagnosis and suggestions back to the frontend.
- The response is displayed as text in the **Doctor's Response** field.
- The response is also converted into audio using ElevenLabs and played back to the user.

---

## API Endpoints (Backend)
### Authentication
1. **POST /auth/register**  
   - **Description**: Register a new user.
   - **Request Body**:
     ```json
     {
       "username": "string",
       "password": "string"
     }
     ```
   - **Response**:
     ```json
     {
       "message": "User registered successfully"
     }
     ```

2. **POST /auth/login**  
   - **Description**: Log in and receive a JWT token.
   - **Request Body**:
     ```json
     {
       "username": "string",
       "password": "string"
     }
     ```
   - **Response**:
     ```json
     {
       "access_token": "string",
       "token_type": "bearer"
     }
     ```

### AI Doctor
1. **GET /auth/ai_doctor**  
   - **Description**: Access the AI Doctor functionality (requires authentication).
   - **Headers**:
     ```json
     {
       "Authorization": "Bearer <token>"
     }
     ```
   - **Response**:
     ```json
     {
       "message": "Welcome to AI Doctor, <username>!"
     }
     ```

---

## Frontend Features
### Tabs
1. **Login Tab**:
   - Allows users to log in with their credentials.
   - On successful login, the **AI Doctor** tab becomes visible.

2. **Register Tab**:
   - Allows new users to register.

3. **AI Doctor Tab**:
   - Accessible only after login.
   - Accepts audio and image inputs to provide medical insights.

### Logout
- Logs out the user and hides the **AI Doctor** tab.

---

## 🚀 Future Enhancements
- Add multi-language support for the AI Doctor.
- Implement role-based access control (e.g., admin vs. user).
- Integrate additional AI models for advanced medical analysis.

---

## 📜 License
This project is licensed under the MIT License.

---

## 📩 Contact
For issues or suggestions, feel free to open an [issue](https://github.com/HaseebAhmed49/MediNova_Bot/issues) or reach out:
- **Email**: haseebahmed02@gmail.com
- **GitHub**: [haseebahmed49](https://github.com/HaseebAhmed49)

💡 **Happy Coding!** 🚀
Let me know if you need further assistance! 🚀
