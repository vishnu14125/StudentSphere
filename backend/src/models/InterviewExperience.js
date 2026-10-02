const mongoose = require('mongoose');

const interviewExperienceSchema = new mongoose.Schema({
  user: {
    type: mongoose.Schema.Types.ObjectId,
    ref: 'User',
    required: false, // Made optional for demo data
  },
  company: {
    type: mongoose.Schema.Types.ObjectId,
    ref: 'Company',
    required: true,
  },
  role: {
    type: String,
    required: [true, 'Please provide a role'],
    trim: true,
  },
  experienceTitle: {
    type: String,
    required: [true, 'Please provide an experience title'],
    trim: true,
  },
  experienceText: {
    type: String,
    required: [true, 'Please provide the experience text'],
  },
  interviewRounds: [{
    type: String,
    trim: true,
  }],
  difficulty: {
    type: String,
    enum: ['Easy', 'Medium', 'Hard'],
    default: 'Medium',
  },
  year: {
    type: Number,
    required: [true, 'Please provide the interview year'],
  },
  topics: [{
    type: String,
    trim: true,
  }],
  questions: [{
    type: String,
    trim: true,
  }],
  source: {
    type: String,
    trim: true,
  },
  aiSummary: {
    type: String,
  },
  aiExtractedTopics: [{
    type: String,
    trim: true,
  }],
  aiExtractedQuestions: [{
    type: String,
    trim: true,
  }],
  aiProcessed: {
    type: Boolean,
    default: false,
  },
}, {
  timestamps: true,
});

// Create indexes for search
interviewExperienceSchema.index({ company: 1, role: 1 });
interviewExperienceSchema.index({ difficulty: 1 });
interviewExperienceSchema.index({ year: 1 });
interviewExperienceSchema.index({ topics: 1 });
interviewExperienceSchema.index({ experienceText: 'text', experienceTitle: 'text' });

module.exports = mongoose.model('InterviewExperience', interviewExperienceSchema);
