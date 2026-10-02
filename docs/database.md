# StudentSphere Database Documentation

## Overview

StudentSphere uses two database systems:
1. **MongoDB** - Structured data storage (users, companies, interviews)
2. **ChromaDB** - Vector database for RAG (embeddings)

## MongoDB Schema

### Database Name
`studentsphere`

### Collections

#### 1. Users Collection

**Model:** `User`

**Schema:**
```javascript
{
  _id: ObjectId,
  name: {
    type: String,
    required: true,
    trim: true
  },
  email: {
    type: String,
    required: true,
    unique: true,
    lowercase: true,
    trim: true,
    match: /^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$/
  },
  password: {
    type: String,
    required: true,
    minlength: 6,
    select: false  // Not returned by default queries
  },
  college: {
    type: String,
    trim: true
  },
  branch: {
    type: String,
    trim: true
  },
  graduationYear: {
    type: Number
  },
  skills: [{
    type: String,
    trim: true
  }],
  targetRoles: [{
    type: String,
    trim: true
  }],
  targetCompanies: [{
    type: ObjectId,
    ref: 'Company'
  }],
  createdAt: {
    type: Date,
    default: Date.now
  },
  updatedAt: {
    type: Date,
    default: Date.now
  }
}
```

**Indexes:**
- `email` (unique)

**Relationships:**
- References `Company` in `targetCompanies`

**Security:**
- Password is hashed using bcryptjs before storage
- Password field is excluded from queries by default

---

#### 2. Companies Collection

**Model:** `Company`

**Schema:**
```javascript
{
  _id: ObjectId,
  name: {
    type: String,
    required: true,
    unique: true,
    trim: true
  },
  logo: {
    type: String,
    default: ''
  },
  industry: {
    type: String,
    trim: true
  },
  description: {
    type: String,
    trim: true
  },
  roles: [{
    type: String,
    trim: true
  }],
  interviewCount: {
    type: Number,
    default: 0
  },
  popularTopics: [{
    type: String,
    trim: true
  }],
  createdAt: {
    type: Date,
    default: Date.now
  },
  updatedAt: {
    type: Date,
    default: Date.now
  }
}
```

**Indexes:**
- `name` (unique)

**Relationships:**
- Referenced by `InterviewExperience`
- Referenced by `User` in `targetCompanies`

**Computed Fields:**
- `interviewCount` - Updated when interviews are added/removed

---

#### 3. InterviewExperiences Collection

**Model:** `InterviewExperience`

**Schema:**
```javascript
{
  _id: ObjectId,
  user: {
    type: ObjectId,
    ref: 'User',
    required: true
  },
  company: {
    type: ObjectId,
    ref: 'Company',
    required: true
  },
  role: {
    type: String,
    required: true,
    trim: true
  },
  experienceTitle: {
    type: String,
    required: true,
    trim: true
  },
  experienceText: {
    type: String,
    required: true
  },
  interviewRounds: [{
    type: String,
    trim: true
  }],
  difficulty: {
    type: String,
    enum: ['Easy', 'Medium', 'Hard'],
    default: 'Medium'
  },
  year: {
    type: Number,
    required: true
  },
  topics: [{
    type: String,
    trim: true
  }],
  questions: [{
    type: String,
    trim: true
  }],
  source: {
    type: String,
    trim: true
  },
  aiSummary: {
    type: String
  },
  aiExtractedTopics: [{
    type: String,
    trim: true
  }],
  aiExtractedQuestions: [{
    type: String,
    trim: true
  }],
  aiProcessed: {
    type: Boolean,
    default: false
  },
  createdAt: {
    type: Date,
    default: Date.now
  },
  updatedAt: {
    type: Date,
    default: Date.now
  }
}
```

**Indexes:**
- `company` (for company-specific queries)
- `role` (for role-based filtering)
- `difficulty` (for difficulty filtering)
- `year` (for year-based filtering)
- `topics` (for topic-based queries)
- Text index on `experienceText` and `experienceTitle` (for full-text search)

**Relationships:**
- References `User` (author)
- References `Company` (company)
- Referenced by RAG system (via document ID)

**AI Fields:**
- `aiSummary` - AI-generated summary
- `aiExtractedTopics` - Topics extracted by AI
- `aiExtractedQuestions` - Questions extracted by AI
- `aiProcessed` - Flag indicating AI processing status

---

## ChromaDB Schema

### Collection Name
`interview_experiences`

### Document Structure

Each document in ChromaDB represents a chunk of an interview experience:

```python
{
  "id": "string",  # Unique identifier (e.g., "interview_id_chunk_0")
  "embedding": [float],  # Vector embedding
  "document": "string",  # Text chunk
  "metadata": {
    "type": "interview_experience",
    "chunk_index": 0,
    "parent_doc_id": "interview_id",
    "company": "string",  # Optional
    "role": "string",  # Optional
    "year": 2024  # Optional
  }
}
```

### Metadata Fields

- `type` - Document type (for filtering)
- `chunk_index` - Index of the chunk in the original document
- `parent_doc_id` - Reference to the original interview experience
- `company` - Company name (optional, for filtering)
- `role` - Role (optional, for filtering)
- `year` - Interview year (optional, for filtering)

### Embedding Model

- **Model:** `sentence-transformers/all-MiniLM-L6-v2`
- **Dimension:** 384
- **Purpose:** Semantic similarity search

---

## Database Relationships

### Entity Relationship Diagram

```
User (1) ----< (N) InterviewExperience (N) >---- (1) Company
  |                                                       |
  |                                                       |
  +--------< (N) targetCompanies ------------------------+
```

### Relationship Details

**User ↔ InterviewExperience**
- One user can have many interview experiences
- One interview experience belongs to one user
- Relationship: One-to-Many

**Company ↔ InterviewExperience**
- One company can have many interview experiences
- One interview experience belongs to one company
- Relationship: One-to-Many

**User ↔ Company**
- One user can target many companies
- One company can be targeted by many users
- Relationship: Many-to-Many

---

## Indexes

### MongoDB Indexes

#### Users Collection
```javascript
db.users.createIndex({ email: 1 }, { unique: true })
```

#### Companies Collection
```javascript
db.companies.createIndex({ name: 1 }, { unique: true })
```

#### InterviewExperiences Collection
```javascript
db.interviewexperiences.createIndex({ company: 1 })
db.interviewexperiences.createIndex({ role: 1 })
db.interviewexperiences.createIndex({ difficulty: 1 })
db.interviewexperiences.createIndex({ year: 1 })
db.interviewexperiences.createIndex({ topics: 1 })
db.interviewexperiences.createIndex({ 
  experienceText: "text", 
  experienceTitle: "text" 
})
```

### ChromaDB Indexes

ChromaDB automatically creates HNSW (Hierarchical Navigable Small World) indexes for efficient similarity search.

---

## Data Migration

### Seed Data

#### Companies Seed Data
```javascript
[
  {
    name: 'Amazon',
    industry: 'E-commerce & Cloud',
    description: 'Global technology company focused on e-commerce, cloud computing, and AI',
    roles: ['SDE', 'SDE-1', 'SDE-2', 'Data Engineer', 'DevOps Engineer']
  },
  {
    name: 'Microsoft',
    industry: 'Software & Cloud',
    description: 'Technology company known for Windows, Azure, and productivity software',
    roles: ['Software Engineer', 'Data Scientist', 'Product Manager', 'Cloud Architect']
  },
  // ... more companies
]
```

---

## Database Operations

### Common Queries

#### Get User by Email
```javascript
const user = await User.findOne({ email }).select('+password');
```

#### Get Company Interviews with Pagination
```javascript
const interviews = await InterviewExperience.find({ company: companyId })
  .populate('user', 'name college')
  .sort({ createdAt: -1 })
  .skip(skip)
  .limit(limit);
```

#### Search Interviews
```javascript
const interviews = await InterviewExperience.find({
  $text: { $search: searchTerm }
}).populate('company', 'name');
```

#### Get Statistics
```javascript
const stats = await InterviewExperience.aggregate([
  {
    $group: {
      _id: '$difficulty',
      count: { $sum: 1 }
    }
  }
]);
```

---

## Backup and Recovery

### MongoDB Backup

```bash
# Backup
mongodump --db studentsphere --out /backup/path

# Restore
mongorestore --db studentsphere /backup/path/studentsphere
```

### ChromaDB Backup

ChromaDB data is stored in the `chroma_db` directory. Backup the entire directory:

```bash
# Backup
cp -r chroma_db /backup/path/

# Restore
cp -r /backup/path/chroma_db ./
```

---

## Performance Optimization

### Query Optimization

1. **Use Indexes:** Ensure all query fields are indexed
2. **Pagination:** Use `skip()` and `limit()` for large result sets
3. **Projection:** Select only required fields
4. **Population:** Use `populate()` judiciously

### Aggregation Optimization

1. **Filter Early:** Apply `$match` as early as possible
2. **Limit Results:** Use `$limit` after filtering
3. **Index Usage:** Ensure aggregation stages use indexes

---

## Security Considerations

### Data Protection

1. **Password Hashing:** Always hash passwords before storage
2. **Sensitive Fields:** Exclude sensitive fields from queries
3. **Input Validation:** Validate all inputs before database operations
4. **SQL Injection:** Use parameterized queries (Mongoose handles this)

### Access Control

1. **Authentication:** Verify user identity before operations
2. **Authorization:** Check user permissions
3. **Ownership:** Ensure users can only modify their own data

---

## Monitoring

### MongoDB Metrics

- Connection count
- Query performance
- Index usage
- Database size
- Operation statistics

### ChromaDB Metrics

- Collection size
- Query performance
- Index efficiency
- Memory usage

---

## Maintenance

### Regular Tasks

1. **Index Rebuilding:** Rebuild indexes if performance degrades
2. **Data Cleanup:** Remove old or irrelevant data
3. **Statistics Update:** Update collection statistics
4. **Backup Verification:** Verify backup integrity

### MongoDB Maintenance

```javascript
// Analyze collection
db.interviewexperiences.stats()

// Rebuild index
db.interviewexperiences.reIndex()

// Compact collection
db.interviewexperiences.compact()
```

---

## Troubleshooting

### Common Issues

#### Slow Queries
- Check if indexes exist
- Use `explain()` to analyze query plan
- Optimize aggregation pipeline

#### Connection Issues
- Verify MongoDB is running
- Check connection string
- Ensure network connectivity

#### Duplicate Key Errors
- Check unique constraints
- Handle race conditions
- Use upsert operations

---

## Future Enhancements

### Planned Improvements

1. **Caching Layer:** Add Redis for frequently accessed data
2. **Read Replicas:** Improve read performance
3. **Sharding:** Scale horizontally for large datasets
4. **Change Streams:** Real-time data synchronization
5. **Advanced Indexing:** Add more specialized indexes
6. **Data Archival:** Archive old data to reduce collection size
