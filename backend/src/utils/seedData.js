require('dotenv').config();
const mongoose = require('mongoose');
const InterviewExperience = require('../models/InterviewExperience');
const Company = require('../models/Company');

const interviewSeedData = [
  {
    company: 'Amazon',
    role: 'SDE',
    experienceTitle: 'Amazon SDE Interview Experience 2024',
    experienceText: 'I had my Amazon SDE interview recently. The process consisted of 4 rounds. The first round was an online assessment with 2 coding questions - one on arrays and one on trees. The second round was a technical interview focused on data structures and algorithms. They asked about LRU Cache implementation, binary tree traversal, and dynamic programming problems. The third round was system design where I had to design a URL shortener. The final round was HR and behavioral questions. The difficulty was medium to hard overall.',
    interviewRounds: ['Online Assessment', 'Technical Round 1', 'Technical Round 2', 'System Design', 'HR Round'],
    difficulty: 'Medium',
    year: 2024,
    topics: ['Arrays', 'Trees', 'Dynamic Programming', 'System Design', 'LRU Cache'],
    questions: ['LRU Cache implementation', 'Binary Tree Traversal', 'Design URL Shortener', 'Dynamic Programming - Knapsack'],
    source: 'LeetCode Discuss',
  },
  {
    company: 'Amazon',
    role: 'SDE-1',
    experienceTitle: 'Amazon SDE-1 Interview 2024',
    experienceText: 'Amazon SDE-1 interview had 3 technical rounds. First round was online coding test with questions on strings and arrays. Second round was DSA focused - they asked about two sum, tree traversal, and graph algorithms. Third round was problem-solving with medium difficulty questions. Interviewers were very helpful and provided hints when stuck. Overall good experience.',
    interviewRounds: ['Online Assessment', 'Technical Round 1', 'Technical Round 2'],
    difficulty: 'Medium',
    year: 2024,
    topics: ['Strings', 'Arrays', 'Trees', 'Graphs', 'Two Sum'],
    questions: ['Two Sum', 'Tree Traversal', 'Graph BFS/DFS', 'String Manipulation'],
    source: 'Glassdoor',
  },
  {
    company: 'Microsoft',
    role: 'Software Engineer',
    experienceTitle: 'Microsoft Software Engineer Interview',
    experienceText: 'Microsoft interview process was well-structured. Had 4 rounds including coding, system design, and behavioral. Coding questions were focused on arrays, linked lists, and trees. System design round asked to design a file system. Behavioral questions were about team collaboration and problem-solving approach. Interviewers were professional and the process was smooth.',
    interviewRounds: ['Online Assessment', 'Technical Round 1', 'System Design', 'Behavioral'],
    difficulty: 'Hard',
    year: 2024,
    topics: ['Arrays', 'Linked Lists', 'Trees', 'System Design', 'File Systems'],
    questions: ['Linked List Cycle Detection', 'Tree Serialization', 'Design File System', 'Merge Sorted Arrays'],
    source: 'GeeksforGeeks',
  },
  {
    company: 'Google',
    role: 'Software Engineer',
    experienceTitle: 'Google Software Engineer Interview 2024',
    experienceText: 'Google interview was challenging but fair. Had 5 rounds including coding, system design, and behavioral. Coding questions were mostly on graphs, dynamic programming, and trees. System design involved designing a distributed cache. They also asked about previous projects in depth. Need strong DSA fundamentals and problem-solving skills.',
    interviewRounds: ['Phone Screen', 'Technical Round 1', 'Technical Round 2', 'System Design', 'Behavioral'],
    difficulty: 'Hard',
    year: 2024,
    topics: ['Graphs', 'Dynamic Programming', 'Trees', 'Distributed Systems', 'Caching'],
    questions: ['Graph Shortest Path', 'DP - Longest Increasing Subsequence', 'Tree Diameter', 'Design Distributed Cache'],
    source: 'LeetCode',
  },
  {
    company: 'Zoho',
    role: 'Software Developer',
    experienceTitle: 'Zoho Software Developer Interview',
    experienceText: 'Zoho interview had 3 rounds - aptitude, technical, and HR. Technical round focused on basic programming, C/C++ concepts, and simple problem solving. Questions were easier compared to FAANG companies. They asked about arrays, strings, and basic algorithms. Good for freshers.',
    interviewRounds: ['Aptitude Test', 'Technical Round', 'HR Round'],
    difficulty: 'Easy',
    year: 2024,
    topics: ['Arrays', 'Strings', 'C Programming', 'Basic Algorithms'],
    questions: ['Array Rotation', 'String Palindrome', 'Fibonacci Series', 'Prime Numbers'],
    source: 'Company Website',
  },
  {
    company: 'TCS',
    role: 'System Engineer',
    experienceTitle: 'TCS System Engineer Interview',
    experienceText: 'TCS interview process included written test, technical interview, and HR. Written test had aptitude, reasoning, and technical questions. Technical round asked about C, Java, DBMS, and basic data structures. Questions were moderate difficulty. HR round was about company culture and career goals.',
    interviewRounds: ['Written Test', 'Technical Interview', 'HR Interview'],
    difficulty: 'Easy',
    year: 2024,
    topics: ['C Programming', 'Java', 'DBMS', 'Data Structures', 'SQL'],
    questions: ['C Pointers', 'Java OOPs', 'SQL Joins', 'Stack Operations'],
    source: 'Campus Placement',
  },
  {
    company: 'Infosys',
    role: 'Systems Engineer',
    experienceTitle: 'Infosys Systems Engineer Interview',
    experienceText: 'Infosys interview had 2 rounds - technical and HR. Technical round focused on programming basics, data structures, and logical reasoning. They asked questions on arrays, linked lists, and basic algorithms. HR round was about communication skills and problem-solving attitude. Overall a smooth process.',
    interviewRounds: ['Technical Round', 'HR Round'],
    difficulty: 'Easy',
    year: 2024,
    topics: ['Arrays', 'Linked Lists', 'Programming Basics', 'Logical Reasoning'],
    questions: ['Array Manipulation', 'Linked List Operations', 'Pattern Printing', 'Number Series'],
    source: 'Off-Campus Drive',
  },
  {
    company: 'Accenture',
    role: 'Software Engineer',
    experienceTitle: 'Accenture Software Engineer Interview',
    experienceText: 'Accenture interview included online assessment, technical interview, and HR. Online assessment had aptitude and coding questions. Technical round asked about Java, SQL, and data structures. They also asked about previous projects. HR round was about career aspirations and teamwork.',
    interviewRounds: ['Online Assessment', 'Technical Interview', 'HR Interview'],
    difficulty: 'Medium',
    year: 2024,
    topics: ['Java', 'SQL', 'Data Structures', 'Projects'],
    questions: ['Java Collections', 'SQL Queries', 'Array Problems', 'Project Discussion'],
    source: 'Company Drive',
  },
  {
    company: 'Amazon',
    role: 'Data Engineer',
    experienceTitle: 'Amazon Data Engineer Interview',
    experienceText: 'Amazon Data Engineer interview focused heavily on SQL, data modeling, and Python. Had 3 technical rounds covering SQL optimization, ETL pipelines, and data warehousing concepts. They asked about window functions, complex joins, and database design. Also asked Python coding questions for data manipulation.',
    interviewRounds: ['Technical Round 1', 'Technical Round 2', 'Technical Round 3'],
    difficulty: 'Hard',
    year: 2024,
    topics: ['SQL', 'Data Modeling', 'Python', 'ETL', 'Data Warehousing'],
    questions: ['SQL Window Functions', 'Database Normalization', 'Python Pandas', 'ETL Pipeline Design'],
    source: 'LinkedIn',
  },
  {
    company: 'Microsoft',
    role: 'Data Scientist',
    experienceTitle: 'Microsoft Data Scientist Interview',
    experienceText: 'Microsoft Data Scientist interview had 4 rounds including coding, statistics, machine learning, and behavioral. Coding questions were on data manipulation. Statistics round covered probability, hypothesis testing, and A/B testing. ML round asked about model evaluation and feature engineering. Challenging but fair process.',
    interviewRounds: ['Coding Round', 'Statistics Round', 'ML Round', 'Behavioral'],
    difficulty: 'Hard',
    year: 2024,
    topics: ['Statistics', 'Machine Learning', 'Python', 'A/B Testing', 'Feature Engineering'],
    questions: ['Probability Problems', 'Hypothesis Testing', 'Model Evaluation Metrics', 'Feature Selection'],
    source: 'Kaggle',
  },
];

const seedInterviews = async () => {
  try {
    console.log('Connecting to MongoDB...');
    await mongoose.connect(process.env.MONGODB_URI || 'mongodb://localhost:27017/studentsphere');
    console.log('✅ MongoDB connected');

    console.log('Starting interview seed data insertion...');

    // Get existing companies
    const companies = await Company.find({});
    const companyMap = {};
    companies.forEach(company => {
      companyMap[company.name.toLowerCase()] = company._id;
    });

    console.log(`Found ${companies.length} companies in database`);

    let insertedCount = 0;
    let skippedCount = 0;

    for (const interviewData of interviewSeedData) {
      const companyName = interviewData.company;
      const companyId = companyMap[companyName.toLowerCase()];

      if (!companyId) {
        console.log(`Skipping interview for ${companyName} - company not found`);
        skippedCount++;
        continue;
      }

      // Check if similar interview already exists
      const existing = await InterviewExperience.findOne({
        company: companyId,
        role: interviewData.role,
        experienceTitle: interviewData.experienceTitle,
      });

      if (existing) {
        console.log(`Skipping duplicate interview: ${interviewData.experienceTitle}`);
        skippedCount++;
        continue;
      }

      // Create interview experience
      await InterviewExperience.create({
        user: null, // System-generated, no user
        company: companyId,
        role: interviewData.role,
        experienceTitle: interviewData.experienceTitle,
        experienceText: interviewData.experienceText,
        interviewRounds: interviewData.interviewRounds,
        difficulty: interviewData.difficulty,
        year: interviewData.year,
        topics: interviewData.topics,
        questions: interviewData.questions,
        source: interviewData.source,
        aiProcessed: false, // Will be processed by AI service
      });

      insertedCount++;
      console.log(`✅ Inserted: ${interviewData.experienceTitle}`);

      // Update company interview count
      await Company.findByIdAndUpdate(companyId, {
        $inc: { interviewCount: 1 }
      });
    }

    console.log(`\n🎉 Seed data insertion complete!`);
    console.log(`📊 Inserted: ${insertedCount} interviews`);
    console.log(`⏭️  Skipped: ${skippedCount} interviews`);
    console.log(`📈 Total interviews in database: ${await InterviewExperience.countDocuments()}`);

  } catch (error) {
    console.error('❌ Error seeding interview data:', error);
  } finally {
    await mongoose.connection.close();
    console.log('MongoDB connection closed');
  }
};

// Run the seed
seedInterviews();
