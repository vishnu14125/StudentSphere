# StudentSphere Setup and Testing Guide

## Prerequisites

Before starting, ensure you have the following installed:

- **Node.js** (v16 or higher) - [Download](https://nodejs.org/)
- **MongoDB** (v4.4 or higher) - [Download](https://www.mongodb.com/try/download/community)
- **Python** (v3.8 or higher) - [Download](https://www.python.org/downloads/)
- **Git** - [Download](https://git-scm.com/downloads)
- **npm** (comes with Node.js)
- **pip** (comes with Python)

## Installation Steps

### 1. Verify Prerequisites

Open a terminal and run:

```bash
node --version  # Should be v16 or higher
npm --version   # Should be 8 or higher
python --version  # Should be 3.8 or higher
mongod --version  # Should be 4.4 or higher
```

### 2. Start MongoDB

**Windows:**
```bash
# If MongoDB is installed as a service
net start MongoDB

# Or run manually
mongod
```

**Mac/Linux:**
```bash
# Start MongoDB service
sudo systemctl start mongodb

# Or run manually
mongod
```

Verify MongoDB is running:
```bash
# In a new terminal
mongo
# You should see MongoDB shell
exit
```

### 3. Backend Setup

```bash
cd backend
npm install
```

Create `.env` file:
```bash
cp .env.example .env
```

Edit `backend/.env`:
```env
PORT=5000
NODE_ENV=development
MONGODB_URI=mongodb://localhost:27017/studentsphere
JWT_SECRET=your_secret_key_change_this_in_production
JWT_EXPIRE=7d
AI_SERVICE_URL=http://localhost:8000
FRONTEND_URL=http://localhost:3000
```

Start backend:
```bash
npm run dev
```

Backend should start on `http://localhost:5000`

Keep this terminal open.

### 4. Frontend Setup

Open a new terminal:

```bash
cd frontend
npm install
```

Start frontend:
```bash
npm start
```

Frontend should open in your browser at `http://localhost:3000`

Keep this terminal open.

### 5. AI Service Setup

Open a new terminal:

```bash
cd ai-service
pip install -r requirements.txt
```

Create `.env` file:
```bash
cp .env.example .env
```

Edit `ai-service/.env`:
```env
HOST=0.0.0.0
PORT=8000
BACKEND_URL=http://localhost:5000
OPENAI_API_KEY=your_openai_api_key_here  # Optional, fallback available
EMBEDDING_MODEL=sentence-transformers/all-MiniLM-L6-v2
CHROMA_PERSIST_DIRECTORY=./chroma_db
```

Start AI service:
```bash
python main.py
```

AI service should start on `http://localhost:8000`

Keep this terminal open.

---

## Testing the System

### Test 1: Backend Health Check

Open a new terminal and run:

```bash
curl http://localhost:5000/api/health
```

Expected response:
```json
{
  "status": "OK",
  "message": "StudentSphere API is running"
}
```

### Test 2: AI Service Health Check

```bash
curl http://localhost:8000/health
```

Expected response:
```json
{
  "status": "healthy"
}
```

### Test 3: User Registration

1. Open browser: `http://localhost:3000/register`
2. Fill in the form:
   - Name: Test User
   - Email: test@example.com
   - Password: password123
   - College: MIT
   - Branch: Computer Science
   - Graduation Year: 2025
3. Click "Create account"
4. You should be redirected to the dashboard

### Test 4: User Login

1. Logout if logged in
2. Go to: `http://localhost:3000/login`
3. Enter credentials:
   - Email: test@example.com
   - Password: password123
4. Click "Sign in"
5. You should be redirected to the dashboard

### Test 5: Seed Companies

Using Postman or curl:

```bash
# First, get your JWT token from the login response
# Then use it to seed companies

curl -X POST http://localhost:5000/api/companies/seed \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"
```

Expected response:
```json
{
  "message": "Companies seeded successfully",
  "count": 10,
  "companies": [...]
}
```

### Test 6: Browse Companies

1. Click "Companies" in the navigation
2. You should see a list of companies
3. Try searching for "Amazon"
4. Click on a company to view details

### Test 7: Submit Interview Experience

1. Click "Submit Experience" in the navigation
2. Fill in the form:
   - Company: Amazon
   - Role: SDE
   - Experience Title: Amazon SDE Interview 2024
   - Experience Text: "I had my Amazon SDE interview recently. It consisted of 3 technical rounds. The first round was an online assessment with DSA questions. The second round was a technical interview focused on data structures and algorithms. The third round was a system design round. They asked questions about LRU Cache, Binary Tree Traversal, and SQL joins. The difficulty was medium to hard."
   - Interview Rounds (one per line):
     ```
     Online Assessment
     Technical Round 1
     Technical Round 2
     HR Round
     ```
   - Difficulty: Medium
   - Year: 2024
   - Topics: Arrays, Trees, Dynamic Programming, DBMS
   - Questions (one per line):
     ```
     LRU Cache implementation
     Binary Tree Traversal
     SQL Joins
     ```
   - Source: LeetCode
3. Click "Submit Experience"
4. You should be redirected to the interviews list

### Test 8: View Interview Experience

1. Click on the interview you just submitted
2. You should see:
   - Interview details
   - Company information
   - Experience text
   - Topics and questions
   - AI-generated summary (may take a few seconds to appear)

### Test 9: Search and Filter

1. Go to "Interviews" page
2. Try different filters:
   - Company: Amazon
   - Role: SDE
   - Difficulty: Medium
   - Year: 2024
3. Try text search: "DSA"
4. Clear filters and try again

### Test 10: Dashboard Statistics

1. Go to "Dashboard"
2. You should see:
   - Total interview experiences
   - Number of companies
   - Popular topics
   - Most common roles
   - Difficulty distribution
   - Top companies

### Test 11: AI Processing Check

Wait 1-2 minutes after submitting an interview, then:

1. Go to the interview details page
2. You should see an "AI Analysis" section with:
   - AI-generated summary
   - Extracted topics
   - Key questions

If AI processing is not working, check:
- AI service is running on port 8000
- Backend AI_SERVICE_URL is correct
- Check AI service logs for errors

### Test 12: Profile Update

1. Click your name in the navigation
2. Update your profile:
   - Add skills: JavaScript, Python, React
   - Add target roles: SDE, Data Engineer
3. Click "Update Profile"
4. Changes should be saved

### Test 13: Edit Interview

1. Go to an interview you submitted
2. Click "Edit" (only visible for your own interviews)
3. Make changes and save
4. Verify changes are reflected

### Test 14: Delete Interview

1. Go to an interview you submitted
2. Click "Delete"
3. Confirm deletion
4. Interview should be removed

---

## API Testing with curl

### Register
```bash
curl -X POST http://localhost:5000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Test User",
    "email": "test@example.com",
    "password": "password123"
  }'
```

### Login
```bash
curl -X POST http://localhost:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "password123"
  }'
```

### Get Companies
```bash
curl http://localhost:5000/api/companies
```

### Create Interview
```bash
curl -X POST http://localhost:5000/api/interviews \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -d '{
    "company": "Amazon",
    "role": "SDE",
    "experienceTitle": "Test Interview",
    "experienceText": "Test experience text",
    "year": 2024
  }'
```

### Get Interviews
```bash
curl http://localhost:5000/api/interviews
```

### Get Statistics
```bash
curl http://localhost:5000/api/interviews/stats
```

---

## Troubleshooting

### MongoDB Connection Issues

**Problem:** Backend fails to connect to MongoDB

**Solutions:**
1. Verify MongoDB is running: `mongod`
2. Check MongoDB URI in `.env` file
3. Ensure MongoDB is accessible on port 27017
4. Check MongoDB logs for errors

### Port Already in Use

**Problem:** Port 5000, 3000, or 8000 already in use

**Solutions:**
1. Find the process using the port:
   ```bash
   # Windows
   netstat -ano | findstr :5000
   
   # Mac/Linux
   lsof -i :5000
   ```
2. Kill the process or change the port in `.env`

### npm Install Fails

**Problem:** `npm install` fails with errors

**Solutions:**
1. Clear npm cache: `npm cache clean --force`
2. Delete `node_modules` and `package-lock.json`
3. Run `npm install` again
4. Try with different Node.js version

### pip Install Fails

**Problem:** `pip install` fails with errors

**Solutions:**
1. Upgrade pip: `pip install --upgrade pip`
2. Use virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # Mac/Linux
   venv\Scripts\activate     # Windows
   pip install -r requirements.txt
   ```

### AI Service Not Responding

**Problem:** AI processing doesn't work

**Solutions:**
1. Verify AI service is running on port 8000
2. Check AI service logs for errors
3. Verify backend `AI_SERVICE_URL` in `.env`
4. Check if embeddings are downloading (first run takes time)
5. If using OpenAI, verify API key

### Frontend Build Errors

**Problem:** Frontend fails to start or build

**Solutions:**
1. Delete `node_modules` and `package-lock.json`
2. Run `npm install` again
3. Check Node.js version (should be 16+)
4. Clear browser cache

### CORS Errors

**Problem:** CORS errors in browser console

**Solutions:**
1. Verify backend CORS configuration
2. Check `FRONTEND_URL` in backend `.env`
3. Ensure both services are running

---

## Performance Tips

### Development

1. Use `npm run dev` for backend (auto-restart)
2. Use `npm start` for frontend (hot reload)
3. Use `python main.py` for AI service (auto-reload)

### Production Considerations

1. Enable compression
2. Implement caching
3. Use environment variables properly
4. Enable HTTPS
5. Implement rate limiting
6. Use production database

---

## Common Commands

### Backend
```bash
cd backend
npm install              # Install dependencies
npm run dev              # Start development server
npm start                # Start production server
```

### Frontend
```bash
cd frontend
npm install              # Install dependencies
npm start                # Start development server
npm run build            # Build for production
```

### AI Service
```bash
cd ai-service
pip install -r requirements.txt  # Install dependencies
python main.py                    # Start development server
```

### MongoDB
```bash
# Start MongoDB
mongod

# Access MongoDB shell
mongo

# Backup database
mongodump --db studentsphere --out ./backup

# Restore database
mongorestore --db studentsphere ./backup/studentsphere
```

---

## Testing Checklist

- [ ] MongoDB is running
- [ ] Backend starts successfully
- [ ] Frontend starts successfully
- [ ] AI service starts successfully
- [ ] User can register
- [ ] User can login
- [ ] User can view dashboard
- [ ] Companies are seeded
- [ ] User can browse companies
- [ ] User can submit interview
- [ ] AI processing works
- [ ] User can search interviews
- [ ] User can filter interviews
- [ ] User can update profile
- [ ] User can edit own interview
- [ ] User can delete own interview
- [ ] Statistics are displayed correctly

---

## Next Steps

After successful testing:

1. **Review the code:** Understand the architecture
2. **Add more features:** Implement future enhancements
3. **Customize the UI:** Modify Tailwind CSS
4. **Add more seed data:** Populate with real interview experiences
5. **Configure OpenAI:** Add API key for better AI results
6. **Deploy:** Prepare for production deployment

---

## Support

If you encounter issues:

1. Check the terminal logs for error messages
2. Review the troubleshooting section above
3. Check the documentation in the `docs/` folder
4. Verify all prerequisites are installed correctly
5. Ensure all services are running

---

## Additional Resources

- [React Documentation](https://react.dev/)
- [Express Documentation](https://expressjs.com/)
- [MongoDB Documentation](https://docs.mongodb.com/)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Tailwind CSS Documentation](https://tailwindcss.com/docs)
