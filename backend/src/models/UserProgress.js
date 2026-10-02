const mongoose = require('mongoose');
const userProgressSchema = new mongoose.Schema({
  user: { type: mongoose.Schema.Types.ObjectId, ref: 'User', required: true, unique: true },
  targetCompany: String, targetRole: String, durationDays: { type: Number, default: 28 },
  roadmap: [{ week: Number, title: String, focus: [String], practice: [String], completedTopics: [String] }],
  topicsProgress: [{ topic: String, completed: { type: Boolean, default: false }, score: Number }],
  weakAreas: [String], preparationStreak: { type: Number, default: 0 }, lastActivity: Date,
}, { timestamps: true });
module.exports = mongoose.model('UserProgress', userProgressSchema);
