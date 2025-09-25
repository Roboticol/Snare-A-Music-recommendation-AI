# Snare 🎵  
An AI-powered music recommendation system with a dedicated **frontend** and **backend**, each dockerized for easy deployment.  

## Features
- Intelligent music recommendation engine (AI-powered backend).  
- Streamlit frontend interface for exploring recommendations.  
- Backend uses FastAPI for sending recommendations to the user.
- Both backend and frontend are containerized with Docker for consistency.  
- Integrated with Docker Compose for testing.  

## Running with Docker
NOTE: You must have a spotify developer's account to run this project.

NOTE: These are only instructions for testing the project, not deploying.

### 1. Configure Environment Files
1. Go to the backend directory and make a new folder there named "run", inside it make another folder "secrets". Finally, inside the secrets folder make the file "API_KEY.env", it must look like this:
```env
API_KEY = CUSTOM API KEY OF YOUR BACKEND
```
2. Make a file in the frontend directory ".env" with this info:
```env
client_id = SPOTIFY DEV CLIENT ID

client_secret = SPOTIFY DEV CLIENT SECRET

API_KEY = CUSTOM API KEY OF YOUR BACKEND

API_URL (only required if you're using this outside of testing) = URL TO BACKEND i.e https://backend.com/predict
```
### 2. Run the Project (Must have Docker installed)
```bash
# NOTE: From project root
docker build -t snare-frontend ./frontend
docker build -t snare-backend ./backend
docker-compose up
```