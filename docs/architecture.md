# StudentSphere Architecture Documentation

## System Overview

StudentSphere follows a microservices-inspired architecture with three main components:
1. **Frontend** - React.js SPA
2. **Backend** - Node.js/Express REST API
3. **AI Service** - Python FastAPI service for AI processing

## Architecture Diagram

```
┌─────────────────┐
│   Frontend      │
│   (React)       │
│                 │
│  - User Auth    │
│  - Companies    │
│  - Interviews   │
│  - Dashboard    │
└────────┬────────┘
         │ HTTP/REST
         ↓
┌─────────────────┐
│   Backend       │
│   (Node.js)     │
│                 │
│  - Auth API     │
│  - Company API  │
│  - Interview   │
│    API          │
└────────┬────────┘
         │ HTTP/REST
         ↓
┌─────────────────┐
│  AI Service     │
│  (Python)       │
│                 │
│  - Summarization│
│  - Embeddings   │
│  - RAG Pipeline │
│  - Vector DB    │
└─────────────────┘
```

## Component Details

### Frontend (React.js)

**Technology Stack:**
- React 18
- React Router 6
- Axios for API calls
- Tailwind CSS for styling
- Context API for state management

**Key Components:**
- `AuthProvider` - Authentication state management
- `Layout` - Main layout with navigation
- Pages: Login, Register, Dashboard, Companies, Interviews, Profile, etc.

**State Management:**
- Context API for authentication
- Local component state for UI
- API calls for data fetching

### Backend (Node.js/Express)

**Technology Stack:**
- Express.js framework
- MongoDB with Mongoose ODM
- JWT for authentication
- bcryptjs for password hashing
- express-validator for input validation

**Architecture Pattern:**
- MVC (Model-View-Controller)
- Separation of concerns
- Middleware for cross-cutting concerns

**Key Modules:**
- `controllers/` - Business logic
- `models/` - Database schemas
- `routes/` - API endpoints
- `middleware/` - Auth, error handling
- `validators/` - Input validation
- `utils/` - Helper functions

**API Design:**
- RESTful endpoints
- Consistent response format
- Proper HTTP status codes
- Pagination support

### AI Service (Python/FastAPI)

**Technology Stack:**
- FastAPI framework
- OpenAI GPT for summarization
- Sentence Transformers for embeddings
- ChromaDB for vector storage
- Custom RAG pipeline

**Architecture:**
- Service-oriented design
- Asynchronous processing
- Vector database integration
- Fallback mechanisms

**Key Modules:**
- `embeddings/` - Text embedding generation
- `rag/` - RAG pipeline and vector store
- `services/` - AI processing services
- `routes/` - API endpoints

## Data Flow

### User Registration Flow
```
1. User submits registration form
2. Frontend sends POST /api/auth/register
3. Backend validates input
4. Backend hashes password
5. Backend creates user in MongoDB
6. Backend generates JWT token
7. Frontend stores token
8. User redirected to dashboard
```

### Interview Submission Flow
```
1. User submits interview experience
2. Frontend sends POST /api/interviews
3. Backend validates and stores in MongoDB
4. Backend triggers AI processing (async)
5. AI service generates summary
6. AI service extracts topics/questions
7. AI service updates MongoDB via internal endpoint
8. AI service ingests into RAG system
9. Frontend displays AI results
```

### Search Flow
```
1. User enters search query
2. Frontend sends GET /api/interviews with params
3. Backend applies filters
4. Backend queries MongoDB
5. Backend returns paginated results
6. Frontend displays results
```

### RAG Search Flow (Future)
```
1. User asks a question
2. Frontend sends query to AI service
3. AI service generates query embedding
4. AI service searches vector database
5. AI service retrieves relevant contexts
6. AI service sends context to LLM
7. LLM generates answer with citations
8. AI service returns answer to frontend
```

## Database Design

### MongoDB (Structured Data)
- Stores user accounts, companies, interview experiences
- Relational data with proper indexing
- Optimized for CRUD operations

### ChromaDB (Vector Data)
- Stores text embeddings
- Optimized for similarity search
- Supports metadata filtering
- Persistent storage

## Security Architecture

### Authentication
- JWT-based stateless authentication
- Token stored in localStorage
- Protected routes require valid token
- Token expiration: 7 days

### Authorization
- User can only edit/delete their own interviews
- Role-based access control (future: admin roles)
- API endpoint protection

### Data Security
- Password hashing with bcryptjs
- Input validation and sanitization
- CORS configuration
- Environment variables for secrets

## Scalability Considerations

### Current Architecture
- Single instance for each service
- Suitable for development and demo
- Can handle moderate traffic

### Future Scalability
- Load balancing for frontend
- Horizontal scaling for backend
- Distributed caching (Redis)
- CDN for static assets
- Database sharding
- Microservices decomposition

## Error Handling

### Frontend
- User-friendly error messages
- Loading states
- Error boundaries
- API error handling

### Backend
- Centralized error handler
- Proper HTTP status codes
- Error logging
- Graceful degradation

### AI Service
- Fallback for AI failures
- Async processing to avoid blocking
- Error logging
- Retry mechanisms

## Performance Optimization

### Frontend
- Code splitting (future)
- Lazy loading (future)
- Image optimization (future)
- API response caching

### Backend
- Database indexing
- Pagination
- Response compression
- Connection pooling

### AI Service
- Async processing
- Batch embedding generation
- Vector database optimization
- Model caching

## Monitoring & Logging

### Current
- Console logging
- Error tracking
- Basic health checks

### Future
- Application performance monitoring
- Error tracking (Sentry)
- Log aggregation (ELK stack)
- Metrics collection (Prometheus)

## Deployment Architecture

### Development
- Local development setup
- MongoDB local instance
- All services on localhost

### Production (Future)
- Cloud hosting (AWS/GCP/Azure)
- Managed MongoDB (MongoDB Atlas)
- Container orchestration (Docker/Kubernetes)
- CI/CD pipeline
- SSL/TLS encryption
- CDN for static assets

## API Gateway (Future)

- Single entry point for all services
- Request routing
- Rate limiting
- Authentication/authorization
- Response caching
- Load balancing

## Event-Driven Architecture (Future)

- Message queue (RabbitMQ/Kafka)
- Event sourcing
- Async processing
- Service decoupling
- Better scalability

## Caching Strategy (Future)

- Redis for session storage
- API response caching
- Database query caching
- CDN caching
- Browser caching

## Testing Strategy

### Unit Tests (Future)
- Component testing
- Service testing
- Model testing

### Integration Tests (Future)
- API endpoint testing
- Database integration
- AI service integration

### E2E Tests (Future)
- User flow testing
- Cross-browser testing
- Performance testing

## Documentation

- API documentation (Swagger/OpenAPI)
- Code documentation (JSDoc/Docstrings)
- Architecture documentation
- Deployment guides
- Troubleshooting guides
