const mongoose = require('mongoose');

const companySchema = new mongoose.Schema({
  name: { type: String, required: [true, 'Please provide a company name'], unique: true, trim: true },
  logo: { type: String, default: '' },
  industry: { type: String, trim: true },
  description: { type: String, trim: true },
  roles: [{ type: String, trim: true }],
  interviewCount: { type: Number, default: 0 },
  popularTopics: [{ type: String, trim: true }],
  intelligence: {
    difficultyDistribution: { Easy: { type: Number, default: 0 }, Medium: { type: Number, default: 0 }, Hard: { type: Number, default: 0 } },
    topicFrequency: [{ topic: String, count: Number, percentage: Number }],
    commonQuestions: [{ question: String, frequency: Number }],
    interviewPattern: [String],
    aiInsight: String,
  },
  lastAnalyzed: Date,
}, { timestamps: true });

module.exports = mongoose.model('Company', companySchema);
