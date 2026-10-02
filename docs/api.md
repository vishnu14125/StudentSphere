# StudentSphere API Documentation

## Base URL

**Development:** `http://localhost:5000/api`

**Production:** `https://api.studentsphere.com/api`

## Authentication

Most endpoints require JWT authentication. Include the token in the Authorization header:

```
Authorization: Bearer <your_jwt_token>
```

## Response Format

All API responses follow this format:

### Success Response
```json
{
  "success": true,
  "data": { ... }
}
```

### Error Response
```json
{
  "success": false,
  "message": "Error message",
  "errors": [ ... ]  // Optional, for validation errors
}
```

---

## Authentication Endpoints

### Register User

Create a new user account.

**Endpoint:** `POST /auth/register`

**Authentication:** None required

**Request Body:**
```json
{
  "name": "John Doe",
  "email": "john@example.com",
  "password": "password123",
  "college": "MIT",
  "branch": "Computer Science",
  "graduationYear": 2025,
  "skills": ["JavaScript", "Python"],
  "targetRoles": ["SDE", "Data Engineer"]
}
```

**Validation Rules:**
- `name`: Required, string, trimmed
- `email`: Required, valid email format, unique
- `password`: Required, minimum 6 characters
- `college`: Optional, string
- `branch`: Optional, string
- `graduationYear`: Optional, integer (2000-2030)
- `skills`: Optional, array of strings
- `targetRoles`: Optional, array of strings

**Success Response (201):**
```json
{
  "_id": "user_id",
  "name": "John Doe",
  "email": "john@example.com",
  "college": "MIT",
  "branch": "Computer Science",
  "graduationYear": 2025,
  "skills": ["JavaScript", "Python"],
  "targetRoles": ["SDE", "Data Engineer"],
  "token": "jwt_token_here"
}
```

**Error Response (400):**
```json
{
  "message": "User already exists"
}
```

---

### Login User

Authenticate a user and receive a JWT token.

**Endpoint:** `POST /auth/login`

**Authentication:** None required

**Request Body:**
```json
{
  "email": "john@example.com",
  "password": "password123"
}
```

**Validation Rules:**
- `email`: Required, valid email format
- `password`: Required

**Success Response (200):**
```json
{
  "_id": "user_id",
  "name": "John Doe",
  "email": "john@example.com",
  "college": "MIT",
  "branch": "Computer Science",
  "graduationYear": 2025,
  "skills": ["JavaScript", "Python"],
  "targetRoles": ["SDE", "Data Engineer"],
  "token": "jwt_token_here"
}
```

**Error Response (401):**
```json
{
  "message": "Invalid credentials"
}
```

---

### Get User Profile

Get the current user's profile.

**Endpoint:** `GET /auth/profile`

**Authentication:** Required

**Success Response (200):**
```json
{
  "_id": "user_id",
  "name": "John Doe",
  "email": "john@example.com",
  "college": "MIT",
  "branch": "Computer Science",
  "graduationYear": 2025,
  "skills": ["JavaScript", "Python"],
  "targetRoles": ["SDE", "Data Engineer"],
  "targetCompanies": ["company_id"]
}
```

**Error Response (404):**
```json
{
  "message": "User not found"
}
```

---

### Update User Profile

Update the current user's profile.

**Endpoint:** `PUT /auth/profile`

**Authentication:** Required

**Request Body:**
```json
{
  "name": "John Doe",
  "college": "MIT",
  "branch": "Computer Science",
  "graduationYear": 2025,
  "skills": ["JavaScript", "Python", "React"],
  "targetRoles": ["SDE", "Data Engineer"],
  "targetCompanies": ["company_id_1", "company_id_2"]
}
```

**Success Response (200):**
```json
{
  "_id": "user_id",
  "name": "John Doe",
  "email": "john@example.com",
  "college": "MIT",
  "branch": "Computer Science",
  "graduationYear": 2025,
  "skills": ["JavaScript", "Python", "React"],
  "targetRoles": ["SDE", "Data Engineer"],
  "targetCompanies": ["company_id_1", "company_id_2"]
}
```

---

## Company Endpoints

### Get All Companies

Get a list of all companies with optional search.

**Endpoint:** `GET /companies`

**Authentication:** None required

**Query Parameters:**
- `search` (optional): Search term for company name

**Example:** `GET /companies?search=Amazon`

**Success Response (200):**
```json
[
  {
    "_id": "company_id",
    "name": "Amazon",
    "logo": "https://example.com/logo.png",
    "industry": "E-commerce & Cloud",
    "description": "Global technology company",
    "roles": ["SDE", "Data Engineer"],
    "interviewCount": 15,
    "popularTopics": ["Arrays", "Trees", "DP"],
    "createdAt": "2024-01-01T00:00:00.000Z",
    "updatedAt": "2024-01-01T00:00:00.000Z"
  }
]
```

---

### Get Company by ID

Get details of a specific company.

**Endpoint:** `GET /companies/:id`

**Authentication:** None required

**URL Parameters:**
- `id`: Company ID

**Success Response (200):**
```json
{
  "_id": "company_id",
  "name": "Amazon",
  "logo": "https://example.com/logo.png",
  "industry": "E-commerce & Cloud",
  "description": "Global technology company",
  "roles": ["SDE", "Data Engineer"],
  "interviewCount": 15,
  "popularTopics": ["Arrays", "Trees", "DP"],
  "createdAt": "2024-01-01T00:00:00.000Z",
  "updatedAt": "2024-01-01T00:00:00.000Z"
}
```

**Error Response (404):**
```json
{
  "message": "Company not found"
}
```

---

### Create Company

Create a new company.

**Endpoint:** `POST /companies`

**Authentication:** Required

**Request Body:**
```json
{
  "name": "New Company",
  "logo": "https://example.com/logo.png",
  "industry": "Technology",
  "description": "Company description",
  "roles": ["SDE", "Product Manager"]
}
```

**Success Response (201):**
```json
{
  "_id": "company_id",
  "name": "New Company",
  "logo": "https://example.com/logo.png",
  "industry": "Technology",
  "description": "Company description",
  "roles": ["SDE", "Product Manager"],
  "interviewCount": 0,
  "popularTopics": [],
  "createdAt": "2024-01-01T00:00:00.000Z",
  "updatedAt": "2024-01-01T00:00:00.000Z"
}
```

**Error Response (400):**
```json
{
  "message": "Company already exists"
}
```

---

### Update Company

Update a company's details.

**Endpoint:** `PUT /companies/:id`

**Authentication:** Required

**URL Parameters:**
- `id`: Company ID

**Request Body:**
```json
{
  "name": "Updated Company Name",
  "description": "Updated description"
}
```

**Success Response (200):**
```json
{
  "_id": "company_id",
  "name": "Updated Company Name",
  "logo": "https://example.com/logo.png",
  "industry": "Technology",
  "description": "Updated description",
  "roles": ["SDE", "Product Manager"],
  "interviewCount": 0,
  "popularTopics": [],
  "createdAt": "2024-01-01T00:00:00.000Z",
  "updatedAt": "2024-01-01T00:00:00.000Z"
}
```

---

### Delete Company

Delete a company.

**Endpoint:** `DELETE /companies/:id`

**Authentication:** Required

**URL Parameters:**
- `id`: Company ID

**Success Response (200):**
```json
{
  "message": "Company removed"
}
```

---

### Seed Companies

Seed the database with initial company data.

**Endpoint:** `POST /companies/seed`

**Authentication:** Required

**Success Response (201):**
```json
{
  "message": "Companies seeded successfully",
  "count": 10,
  "companies": [...]
}
```

---

## Interview Endpoints

### Get All Interviews

Get a list of interview experiences with filtering and pagination.

**Endpoint:** `GET /interviews`

**Authentication:** None required

**Query Parameters:**
- `company` (optional): Filter by company name
- `role` (optional): Filter by role (case-insensitive)
- `difficulty` (optional): Filter by difficulty (Easy, Medium, Hard)
- `year` (optional): Filter by year
- `search` (optional): Full-text search
- `page` (optional): Page number (default: 1)
- `limit` (optional): Items per page (default: 10)

**Examples:**
```
GET /interviews
GET /interviews?company=Amazon
GET /interviews?role=SDE
GET /interviews?difficulty=Medium
GET /interviews?year=2024
GET /interviews?search=DSA
GET /interviews?page=2&limit=20
```

**Success Response (200):**
```json
{
  "interviews": [
    {
      "_id": "interview_id",
      "user": {
        "_id": "user_id",
        "name": "John Doe",
        "college": "MIT"
      },
      "company": {
        "_id": "company_id",
        "name": "Amazon",
        "logo": "https://example.com/logo.png"
      },
      "role": "SDE",
      "experienceTitle": "Amazon SDE Interview 2024",
      "experienceText": "Full interview experience...",
      "interviewRounds": ["OA", "Technical 1", "Technical 2", "HR"],
      "difficulty": "Medium",
      "year": 2024,
      "topics": ["Arrays", "Trees"],
      "questions": ["LRU Cache"],
      "source": "LeetCode",
      "aiSummary": "AI-generated summary...",
      "aiExtractedTopics": ["Arrays", "Trees"],
      "aiExtractedQuestions": ["LRU Cache"],
      "aiProcessed": true,
      "createdAt": "2024-01-01T00:00:00.000Z",
      "updatedAt": "2024-01-01T00:00:00.000Z"
    }
  ],
  "page": 1,
  "pages": 5,
  "total": 50
}
```

---

### Get Interview Statistics

Get statistics about interview experiences.

**Endpoint:** `GET /interviews/stats`

**Authentication:** None required

**Success Response (200):**
```json
{
  "totalInterviews": 128,
  "totalCompanies": 24,
  "difficultyStats": [
    { "_id": "Medium", "count": 65 },
    { "_id": "Hard", "count": 40 },
    { "_id": "Easy", "count": 23 }
  ],
  "yearStats": [
    { "_id": 2024, "count": 80 },
    { "_id": 2023, "count": 48 }
  ],
  "topicStats": [
    { "_id": "Arrays", "count": 45 },
    { "_id": "Trees", "count": 38 },
    { "_id": "Dynamic Programming", "count": 32 }
  ],
  "roleStats": [
    { "_id": "SDE", "count": 60 },
    { "_id": "Software Engineer", "count": 45 }
  ],
  "companyStats": [
    { "_id": "company_id", "companyName": "Amazon", "count": 25 },
    { "_id": "company_id", "companyName": "Google", "count": 20 }
  ]
}
```

---

### Get Interview by ID

Get details of a specific interview experience.

**Endpoint:** `GET /interviews/:id`

**Authentication:** None required

**URL Parameters:**
- `id`: Interview ID

**Success Response (200):**
```json
{
  "_id": "interview_id",
  "user": {
    "_id": "user_id",
    "name": "John Doe",
    "college": "MIT",
    "branch": "Computer Science",
    "graduationYear": 2025
  },
  "company": {
    "_id": "company_id",
    "name": "Amazon",
    "logo": "https://example.com/logo.png",
    "industry": "E-commerce & Cloud",
    "description": "Global technology company"
  },
  "role": "SDE",
  "experienceTitle": "Amazon SDE Interview 2024",
  "experienceText": "Full interview experience...",
  "interviewRounds": ["OA", "Technical 1", "Technical 2", "HR"],
  "difficulty": "Medium",
  "year": 2024,
  "topics": ["Arrays", "Trees"],
  "questions": ["LRU Cache"],
  "source": "LeetCode",
  "aiSummary": "AI-generated summary...",
  "aiExtractedTopics": ["Arrays", "Trees"],
  "aiExtractedQuestions": ["LRU Cache"],
  "aiProcessed": true,
  "createdAt": "2024-01-01T00:00:00.000Z",
  "updatedAt": "2024-01-01T00:00:00.000Z"
}
```

**Error Response (404):**
```json
{
  "message": "Interview experience not found"
}
```

---

### Create Interview

Create a new interview experience.

**Endpoint:** `POST /interviews`

**Authentication:** Required

**Request Body:**
```json
{
  "company": "Amazon",
  "role": "SDE",
  "experienceTitle": "Amazon SDE Interview 2024",
  "experienceText": "Full interview experience...",
  "interviewRounds": ["Online Assessment", "Technical Round 1", "Technical Round 2", "HR"],
  "difficulty": "Medium",
  "year": 2024,
  "topics": ["Arrays", "Trees", "Dynamic Programming"],
  "questions": ["LRU Cache", "Binary Tree Traversal", "SQL Joins"],
  "source": "LeetCode"
}
```

**Validation Rules:**
- `company`: Required, string
- `role`: Required, string
- `experienceTitle`: Required, string
- `experienceText`: Required, string
- `interviewRounds`: Optional, array of strings
- `difficulty`: Optional, enum (Easy, Medium, Hard), default: Medium
- `year`: Required, integer (2015-2026)
- `topics`: Optional, array of strings
- `questions`: Optional, array of strings
- `source`: Optional, string

**Success Response (201):**
```json
{
  "_id": "interview_id",
  "user": {
    "_id": "user_id",
    "name": "John Doe",
    "college": "MIT"
  },
  "company": {
    "_id": "company_id",
    "name": "Amazon",
    "logo": ""
  },
  "role": "SDE",
  "experienceTitle": "Amazon SDE Interview 2024",
  "experienceText": "Full interview experience...",
  "interviewRounds": ["Online Assessment", "Technical Round 1", "Technical Round 2", "HR"],
  "difficulty": "Medium",
  "year": 2024,
  "topics": ["Arrays", "Trees", "Dynamic Programming"],
  "questions": ["LRU Cache", "Binary Tree Traversal", "SQL Joins"],
  "source": "LeetCode",
  "aiProcessed": false,
  "createdAt": "2024-01-01T00:00:00.000Z",
  "updatedAt": "2024-01-01T00:00:00.000Z"
}
```

**Note:** AI processing is triggered asynchronously after creation.

---

### Update Interview

Update an interview experience (only by owner).

**Endpoint:** `PUT /interviews/:id`

**Authentication:** Required

**URL Parameters:**
- `id`: Interview ID

**Request Body:**
```json
{
  "experienceTitle": "Updated Title",
  "difficulty": "Hard",
  "topics": ["Arrays", "Trees", "Dynamic Programming", "System Design"]
}
```

**Success Response (200):**
```json
{
  "_id": "interview_id",
  "user": {
    "_id": "user_id",
    "name": "John Doe",
    "college": "MIT"
  },
  "company": {
    "_id": "company_id",
    "name": "Amazon",
    "logo": ""
  },
  "role": "SDE",
  "experienceTitle": "Updated Title",
  "experienceText": "Full interview experience...",
  "interviewRounds": ["Online Assessment", "Technical Round 1", "Technical Round 2", "HR"],
  "difficulty": "Hard",
  "year": 2024,
  "topics": ["Arrays", "Trees", "Dynamic Programming", "System Design"],
  "questions": ["LRU Cache", "Binary Tree Traversal", "SQL Joins"],
  "source": "LeetCode",
  "aiProcessed": false,
  "createdAt": "2024-01-01T00:00:00.000Z",
  "updatedAt": "2024-01-01T00:00:00.000Z"
}
```

**Error Response (403):**
```json
{
  "message": "Not authorized to update this interview"
}
```

---

### Delete Interview

Delete an interview experience (only by owner).

**Endpoint:** `DELETE /interviews/:id`

**Authentication:** Required

**URL Parameters:**
- `id`: Interview ID

**Success Response (200):**
```json
{
  "message": "Interview experience removed"
}
```

**Error Response (403):**
```json
{
  "message": "Not authorized to delete this interview"
}
```

---

### Internal AI Update

Internal endpoint for AI service to update interview with AI-generated data.

**Endpoint:** `PUT /interviews/:id/ai-update`

**Authentication:** Internal (no auth required for AI service)

**URL Parameters:**
- `id`: Interview ID

**Request Body:**
```json
{
  "aiSummary": "AI-generated summary...",
  "aiExtractedTopics": ["Arrays", "Trees"],
  "aiExtractedQuestions": ["LRU Cache"],
  "aiProcessed": true
}
```

**Success Response (200):**
```json
{
  "status": "success",
  "interviewId": "interview_id",
  "aiProcessed": true
}
```

---

## AI Service Endpoints

### Base URL

**Development:** `http://localhost:8000/api/ai`

### Summarize Interview

Generate AI summary and extract topics/questions from interview text.

**Endpoint:** `POST /summarize`

**Authentication:** None required

**Request Body:**
```json
{
  "interviewId": "interview_id",
  "text": "Full interview experience text..."
}
```

**Success Response (200):**
```json
{
  "status": "success",
  "summary": "Amazon SDE interview consisted of 3 technical rounds...",
  "topics": ["Arrays", "Trees", "Dynamic Programming", "DBMS"],
  "questions": ["LRU Cache", "Binary Tree Traversal", "SQL joins"]
}
```

---

### Search Context (RAG)

Search for relevant interview experiences using RAG.

**Endpoint:** `POST /search`

**Authentication:** None required

**Request Body:**
```json
{
  "query": "Amazon SDE interview questions about arrays",
  "n_results": 5
}
```

**Success Response (200):**
```json
{
  "status": "success",
  "contexts": [
    {
      "id": "doc_id",
      "text": "Relevant text chunk...",
      "metadata": {
        "type": "interview_experience",
        "chunk_index": 0,
        "parent_doc_id": "interview_id"
      },
      "distance": 0.123
    }
  ]
}
```

---

### Delete Document from RAG

Delete a document from the RAG system.

**Endpoint:** `DELETE /documents/:doc_id`

**Authentication:** None required

**URL Parameters:**
- `doc_id`: Document ID

**Success Response (200):**
```json
{
  "status": "success",
  "doc_id": "doc_id"
}
```

---

### Health Check

Check AI service health.

**Endpoint:** `GET /health`

**Authentication:** None required

**Success Response (200):**
```json
{
  "status": "healthy",
  "service": "AI Service"
}
```

---

## Error Codes

| Status Code | Description |
|-------------|-------------|
| 200 | Success |
| 201 | Created |
| 400 | Bad Request (validation error) |
| 401 | Unauthorized (invalid or missing token) |
| 403 | Forbidden (insufficient permissions) |
| 404 | Not Found |
| 500 | Internal Server Error |

---

## Rate Limiting

Currently, no rate limiting is implemented. This will be added in future versions.

---

## Versioning

Current API version: `v1`

Include version in URL for future compatibility:
```
http://localhost:5000/api/v1/...
```

---

## Testing

Use Postman or curl to test endpoints:

### Example with curl
```bash
# Register
curl -X POST http://localhost:5000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{"name":"John Doe","email":"john@example.com","password":"password123"}'

# Login
curl -X POST http://localhost:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"john@example.com","password":"password123"}'

# Get companies
curl http://localhost:5000/api/companies

# Create interview (with token)
curl -X POST http://localhost:5000/api/interviews \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <token>" \
  -d '{"company":"Amazon","role":"SDE","experienceTitle":"Test","experienceText":"Test experience","year":2024}'
```

---

## Changelog

### v1.0.0 (Current)
- Initial API release
- Authentication endpoints
- Company CRUD operations
- Interview CRUD operations
- Search and filtering
- AI integration
- Statistics endpoint

## Advanced feature endpoints

### Company intelligence

`GET /api/companies/:id/intelligence` returns live company-level analytics based on interview experiences. `POST /api/companies/:id/analyze` saves the calculated snapshot and requires JWT authentication.

### Analytics

`GET /api/analytics/overview` returns global or filtered analytics. Optional query parameters: `companyId`, `role`, and `year`.

### Grounded AI query

`POST /api/ai/query` requires a Bearer token.

```json
{
  "query": "What DSA topics are commonly reported for Amazon?",
  "company": "Amazon",
  "role": "SDE",
  "round": "Technical Round",
  "topK": 5
}
```

The response includes `answer`, `insights`, `sources`, and `grounded`. Each source has an interview ID and evidence excerpt so the frontend can link to the original record.

### Preparation roadmap

`POST /api/roadmap/generate` requires a Bearer token.

```json
{
  "company": "Amazon",
  "role": "SDE",
  "durationDays": 28,
  "skills": ["Arrays", "JavaScript"],
  "weakAreas": ["Dynamic Programming"]
}
```

`GET /api/roadmap/progress` retrieves the signed-in user's saved plan. `PUT /api/roadmap/progress` updates a topic completion record.
