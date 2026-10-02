# StudentSphere - AI-Powered Career Development Platform

## Overview

StudentSphere is a centralized platform that collects and organizes interview experiences from multiple sources (LeetCode, Reddit, Glassdoor, GeeksforGeeks) and uses AI to summarize them, identify frequently asked questions and technical topics, analyze company/role interview patterns, and generate personalized placement preparation roadmaps.

## Problem Statement

Students currently search multiple platforms to understand real interview experiences. The information is scattered, lengthy, and difficult to analyze. StudentSphere solves this by providing a unified platform with AI-powered insights.

## Features

### Phase 1 (Current - 40% Milestone)
- **User Authentication**: Register, login, profile management
- **Company Management**: Browse companies, view company details
- **Interview Experiences**: Submit, view, edit, delete interview experiences
- **Search & Filtering**: Search by company, role, difficulty, year, and text search
- **AI Summarization**: Automatic AI-generated summaries, topic extraction, question extraction
- **Dashboard**: Statistics on interviews, companies, popular topics, and roles
- **RAG Foundation**: Initial RAG architecture with embeddings and vector storage

### Future Phases
- Advanced RAG chatbot with source citations
- Company-wise interview pattern analysis
- Question frequency analysis
- Interview trend analysis
- Personalized preparation roadmap
- Resume-based recommendations
- Skill-gap analysis
- Company comparison
- Mock interview generation
- Student preparation progress tracking

## Technology Stack

### Frontend
- React.js
- JavaScript
- HTML5
- CSS3
- Tailwind CSS
- React Router
- Axios

### Backend
- Node.js
- Express.js
- REST APIs
- MongoDB
- Mongoose
- JWT Authentication
- bcryptjs

### AI Service
- Python
- FastAPI
- OpenAI GPT (for summarization)
- Sentence Transformers (for embeddings)
- Persistent local Numpy vector index
- RAG Architecture

## System Architecture

```
Frontend (React)
       |
       | REST API
       ↓
Node.js + Express Backend
       |
       ├── Authentication
       ├── User Management
       ├── Interview Experiences
       ├── Companies
       ├── Questions
       ├── Topics
       └── AI Service Communication
                    |
                    ↓
              Python AI Service
                    |
                    ├── Text Processing
                    ├── Embeddings
                    ├── Vector Search
                    ├── RAG
                    └── LLM
                    |
                    ↓
              AI Generated Insights

MongoDB stores structured application data.
Persistent local Numpy vector store stores vector embeddings for RAG.
```

## Installation

### Prerequisites
- Node.js (v16 or higher)
- MongoDB (v4.4 or higher)
- Python (v3.8 or higher)
- npm or yarn
- pip

### 1. Clone the Repository
```bash
git clone <repository-url>
cd StudentSphere
```

### 2. Backend Setup

```bash
cd backend
npm install
cp .env.example .env
```

Configure `backend/.env`:
```env
PORT=5000
NODE_ENV=development
MONGODB_URI=mongodb://localhost:27017/studentsphere
JWT_SECRET=your_jwt_secret_key_here
JWT_EXPIRE=7d
AI_SERVICE_URL=http://localhost:8000
FRONTEND_URL=http://localhost:3000
```

Start MongoDB:
```bash
# On Windows
net start MongoDB

# On Mac/Linux
sudo systemctl start mongodb
# or
mongod
```

Run backend:
```bash
npm run dev
```

Backend will run on `http://localhost:5000`

### 3. Frontend Setup

```bash
cd frontend
npm install
```

Run frontend:
```bash
npm start
```

Frontend will run on `http://localhost:3000`

### 4. AI Service Setup

```bash
cd ai-service
pip install -r requirements.txt
cp .env.example .env
```

Configure `ai-service/.env`:
```env
HOST=0.0.0.0
PORT=8000
BACKEND_URL=http://localhost:5000
OPENAI_API_KEY=your_openai_api_key_here  # Optional, fallback available
EMBEDDING_MODEL=sentence-transformers/all-MiniLM-L6-v2
VECTOR_PERSIST_DIRECTORY=./vector_db
```

Run AI service:
```bash
python main.py
```

AI service will run on `http://localhost:8000`

### 5. Seed Initial Data

After starting the backend, seed companies:
```bash
# Using Postman or curl
POST http://localhost:5000/api/companies/seed
Headers: Authorization: Bearer <your_jwt_token>
```

## Usage

### 1. Register a User
- Navigate to `http://localhost:3000/register`
- Fill in the registration form
- Submit to create an account

### 2. Login
- Navigate to `http://localhost:3000/login`
- Enter your credentials
- You'll be redirected to the dashboard

### 3. Browse Companies
- Click "Companies" in the navigation
- Search for specific companies
- Click on a company to view details and interview experiences

### 4. Submit Interview Experience
- Click "Submit Experience" in the navigation
- Fill in the interview details
- Submit - AI processing will start automatically
- View the AI-generated summary on the interview details page

### 5. Search Interview Experiences
- Click "Interviews" in the navigation
- Use filters to narrow down results
- Click on an experience to view full details

## API Documentation

### Authentication Endpoints

#### Register
```http
POST /api/auth/register
Content-Type: application/json

{
  "name": "John Doe",
  "email": "john@example.com",
  "password": "password123",
  "college": "MIT",
  "branch": "Computer Science",
  "graduationYear": 2025
}
```

#### Login
```http
POST /api/auth/login
Content-Type: application/json

{
  "email": "john@example.com",
  "password": "password123"
}
```

#### Get Profile
```http
GET /api/auth/profile
Authorization: Bearer <token>
```

#### Update Profile
```http
PUT /api/auth/profile
Authorization: Bearer <token>
Content-Type: application/json

{
  "name": "John Doe",
  "college": "MIT",
  "skills": ["JavaScript", "Python"],
  "targetRoles": ["SDE", "Data Engineer"]
}
```

### Company Endpoints

#### Get All Companies
```http
GET /api/companies
GET /api/companies?search=Amazon
```

#### Get Company Details
```http
GET /api/companies/:id
```

#### Create Company
```http
POST /api/companies
Authorization: Bearer <token>
Content-Type: application/json

{
  "name": "Amazon",
  "industry": "E-commerce",
  "description": "Global technology company",
  "roles": ["SDE", "Data Engineer"]
}
```

#### Seed Companies
```http
POST /api/companies/seed
Authorization: Bearer <token>
```

### Interview Endpoints

#### Get All Interviews
```http
GET /api/interviews
GET /api/interviews?company=Amazon
GET /api/interviews?role=SDE
GET /api/interviews?difficulty=Medium
GET /api/interviews?year=2024
GET /api/interviews?search=DSA
GET /api/interviews?page=1&limit=10
```

#### Get Interview Statistics
```http
GET /api/interviews/stats
```

#### Get Interview Details
```http
GET /api/interviews/:id
```

#### Create Interview
```http
POST /api/interviews
Authorization: Bearer <token>
Content-Type: application/json

{
  "company": "Amazon",
  "role": "SDE",
  "experienceTitle": "Amazon SDE Interview 2024",
  "experienceText": "Full interview experience...",
  "interviewRounds": ["Online Assessment", "Technical Round 1", "Technical Round 2", "HR"],
  "difficulty": "Medium",
  "year": 2024,
  "topics": ["Arrays", "Trees", "Dynamic Programming"],
  "questions": ["LRU Cache", "Binary Tree Traversal"],
  "source": "LeetCode"
}
```

#### Update Interview
```http
PUT /api/interviews/:id
Authorization: Bearer <token>
Content-Type: application/json

{
  "experienceTitle": "Updated Title",
  "difficulty": "Hard"
}
```

#### Delete Interview
```http
DELETE /api/interviews/:id
Authorization: Bearer <token>
```

### AI Service Endpoints

#### Summarize Interview
```http
POST /api/ai/summarize
Content-Type: application/json

{
  "interviewId": "interview_id",
  "text": "Interview experience text..."
}
```

#### Search Context (RAG)
```http
POST /api/ai/search
Content-Type: application/json

{
  "query": "Amazon SDE interview questions",
  "n_results": 5
}
```

## Database Schema

### User Model
```javascript
{
  name: String,
  email: String (unique),
  password: String (hashed),
  college: String,
  branch: String,
  graduationYear: Number,
  skills: [String],
  targetRoles: [String],
  targetCompanies: [ObjectId],
  createdAt: Date,
  updatedAt: Date
}
```

### Company Model
```javascript
{
  name: String (unique),
  logo: String,
  industry: String,
  description: String,
  roles: [String],
  interviewCount: Number,
  popularTopics: [String],
  createdAt: Date,
  updatedAt: Date
}
```

### InterviewExperience Model
```javascript
{
  user: ObjectId (ref: User),
  company: ObjectId (ref: Company),
  role: String,
  experienceTitle: String,
  experienceText: String,
  interviewRounds: [String],
  difficulty: String (Enum: Easy, Medium, Hard),
  year: Number,
  topics: [String],
  questions: [String],
  source: String,
  aiSummary: String,
  aiExtractedTopics: [String],
  aiExtractedQuestions: [String],
  aiProcessed: Boolean,
  createdAt: Date,
  updatedAt: Date
}
```

## Project Structure

```
StudentSphere/
├── backend/
│   ├── src/
│   │   ├── config/
│   │   │   └── database.js
│   │   ├── controllers/
│   │   │   ├── authController.js
│   │   │   ├── companyController.js
│   │   │   └── interviewController.js
│   │   ├── middleware/
│   │   │   ├── auth.js
│   │   │   └── errorHandler.js
│   │   ├── models/
│   │   │   ├── User.js
│   │   │   ├── Company.js
│   │   │   └── InterviewExperience.js
│   │   ├── routes/
│   │   │   ├── authRoutes.js
│   │   │   ├── companyRoutes.js
│   │   │   └── interviewRoutes.js
│   │   ├── utils/
│   │   │   └── generateToken.js
│   │   ├── validators/
│   │   │   ├── authValidator.js
│   │   │   └── interviewValidator.js
│   │   └── server.js
│   ├── package.json
│   └── .env.example
├── frontend/
│   ├── public/
│   │   └── index.html
│   ├── src/
│   │   ├── components/
│   │   ├── context/
│   │   │   └── AuthContext.js
│   │   ├── hooks/
│   │   ├── layouts/
│   │   │   └── Layout.js
│   │   ├── pages/
│   │   │   ├── Login.js
│   │   │   ├── Register.js
│   │   │   ├── Dashboard.js
│   │   │   ├── Companies.js
│   │   │   ├── CompanyDetails.js
│   │   │   ├── Interviews.js
│   │   │   ├── InterviewDetails.js
│   │   │   ├── SubmitInterview.js
│   │   │   └── Profile.js
│   │   ├── services/
│   │   ├── utils/
│   │   ├── App.js
│   │   ├── index.css
│   │   └── index.js
│   ├── package.json
│   ├── tailwind.config.js
│   └── postcss.config.js
├── ai-service/
│   ├── app/
│   │   ├── config.py
│   │   ├── embeddings/
│   │   │   └── embeddings.py
│   │   ├── models/
│   │   ├── rag/
│   │   │   ├── rag_pipeline.py
│   │   │   └── vector_store.py
│   │   ├── routes/
│   │   │   └── ai_routes.py
│   │   ├── services/
│   │   │   └── summarization_service.py
│   │   └── utils/
│   ├── main.py
│   ├── requirements.txt
│   └── .env.example
├── docs/
│   ├── architecture.md
│   ├── database.md
│   ├── api.md
│   └── rag.md
└── README.md
```

## Development

### Running in Development Mode

1. Start MongoDB
2. Start Backend: `cd backend && npm run dev`
3. Start Frontend: `cd frontend && npm start`
4. Start AI Service: `cd ai-service && python main.py`

### Code Style

- Follow clean code principles
- Use meaningful variable names
- Add comments for complex logic
- Follow existing code patterns
- Modular architecture with separation of concerns

### Git Workflow

```bash
# Create a feature branch
git checkout -b feature/feature-name

# Make changes and commit
git add .
git commit -m "Add feature description"

# Push to remote
git push origin feature/feature-name
```

## Security

- JWT authentication for protected routes
- Password hashing with bcryptjs
- Input validation with express-validator
- CORS configuration
- Environment variables for sensitive data
- Never expose API keys in frontend code

## Troubleshooting

### MongoDB Connection Issues
- Ensure MongoDB is running
- Check MongoDB URI in .env file
- Verify MongoDB is accessible on the specified port

### AI Service Not Responding
- Ensure AI service is running on port 8000
- Check OPENAI_API_KEY in .env (optional, fallback available)
- Verify backend AI_SERVICE_URL configuration

### Frontend Build Errors
- Delete node_modules and package-lock.json
- Run `npm install` again
- Ensure all dependencies are compatible

## Future Enhancements

- [ ] Advanced RAG chatbot with source citations
- [ ] Company-wise interview pattern analysis
- [ ] Question frequency analysis over time
- [ ] Interview trend visualization
- [ ] Personalized preparation roadmap generation
- [ ] Resume-based recommendations
- [ ] Skill-gap analysis
- [ ] Company comparison tool
- [ ] Mock interview generation
- [ ] Student preparation progress tracking
- [ ] Integration with more data sources
- [ ] Mobile application

## Contributing

This is a final-year engineering project. Contributions are welcome from team members following the established coding standards and project structure.

## License

This project is developed for educational purposes as a final-year engineering project.

## Team

Final Year Engineering Project Team
- Domain: Full Stack Web Development with Artificial Intelligence
- Institution: [Your Institution Name]
- Year: 2024-2025

## Acknowledgments

- OpenAI for GPT API
- Sentence Transformers for embeddings
- Persistent local Numpy vector storage
- React and Node.js communities
- All open-source contributors

## Final Review Features

The project now includes the following live features in addition to the original CRUD foundation:

- **Company intelligence:** `GET /api/companies/:id/intelligence` calculates difficulty, topic, question, role, and interview-round patterns from MongoDB data. `POST /api/companies/:id/analyze` stores the latest calculated snapshot.
- **Grounded AI insights:** Authenticated `POST /api/ai/query` indexes eligible interview narratives, retrieves semantically relevant chunks through ChromaDB, and returns an answer with source excerpts and links to the underlying experiences. When evidence is insufficient, it explicitly says so rather than inventing an answer.
- **Analytics:** `GET /api/analytics/overview` returns topic/question frequency, difficulty distribution, company comparison, roles, round patterns, and year trends from MongoDB aggregation.
- **Personalized roadmap:** Authenticated `POST /api/roadmap/generate` creates a week-wise plan from company/role data, persists it for the signed-in user, and identifies supplied or inferred weak areas. `GET` and `PUT /api/roadmap/progress` support progress persistence.

### Final Review Demo

1. Start MongoDB, the backend, the AI service, and the frontend in separate terminals.
2. Register and sign in, then open **Companies** and select a company to show live company intelligence.
3. Open **Analytics** to show live MongoDB aggregates.
4. Submit a properly attributed interview experience and explain that background processing extracts a summary and indexes chunks for retrieval.
5. Open **AI Insights**, ask a company or role question, then open one of the displayed source records to demonstrate traceability.
6. Open **Roadmap**, supply a target role and duration, and generate a week-wise preparation plan.

For the review dataset, use only user-submitted or permitted/attributed material. The application does not scrape third-party platforms.
