const InterviewExperience = require('../models/InterviewExperience');
const Company = require('../models/Company');
const axios = require('axios');

const getInterviews = async (req, res) => {
  try {
    const { company, role, difficulty, year, search, page = 1, limit = 10 } = req.query;
    const query = {};
    if (company) {
      const byId = /^[a-f\d]{24}$/i.test(company) ? await Company.findById(company) : null;
      const companyDoc = byId || await Company.findOne({ name: new RegExp(company, 'i') });
      if (companyDoc) query.company = companyDoc._id;
    }
    if (role) query.role = new RegExp(role, 'i');
    if (difficulty) query.difficulty = difficulty;
    if (year) query.year = Number(year);
    if (search) query.$text = { $search: search };
    const pageNum = Math.max(Number(page) || 1, 1); const limitNum = Math.min(Math.max(Number(limit) || 10, 1), 100);
    const [interviews, total] = await Promise.all([
      InterviewExperience.find(query).populate('user', 'name college').populate('company', 'name logo').sort({ createdAt: -1 }).skip((pageNum - 1) * limitNum).limit(limitNum),
      InterviewExperience.countDocuments(query),
    ]);
    res.json({ interviews, page: pageNum, pages: Math.ceil(total / limitNum), total });
  } catch (error) { res.status(500).json({ message: 'Server error', error: error.message }); }
};

const getInterviewById = async (req, res) => {
  try {
    const interview = await InterviewExperience.findById(req.params.id).populate('user', 'name college branch graduationYear').populate('company', 'name logo industry description');
    if (!interview) return res.status(404).json({ message: 'Interview experience not found' });
    res.json(interview);
  } catch (error) { res.status(500).json({ message: 'Server error', error: error.message }); }
};

const processWithAI = async (interviewId, text, metadata = {}) => {
  try { await axios.post(`${process.env.AI_SERVICE_URL || 'http://localhost:8000'}/api/ai/summarize`, { interviewId: String(interviewId), text, metadata }, { timeout: 30000 }); }
  catch (error) { console.error('AI Processing Error:', error.message); }
};

const createInterview = async (req, res) => {
  try {
    const { company, role, experienceTitle, experienceText, interviewRounds, difficulty, year, topics, questions, source } = req.body;
    let companyDoc = await Company.findOne({ name: new RegExp(`^${company}$`, 'i') });
    if (!companyDoc) companyDoc = await Company.create({ name: company, roles: [role] });
    const interview = await InterviewExperience.create({ user: req.user._id, company: companyDoc._id, role, experienceTitle, experienceText, interviewRounds: interviewRounds || [], difficulty: difficulty || 'Medium', year, topics: topics || [], questions: questions || [], source: source || 'StudentSphere user submission' });
    companyDoc.interviewCount += 1; await companyDoc.save();
    processWithAI(interview._id, experienceText, { interviewId: String(interview._id), companyId: String(companyDoc._id), companyName: companyDoc.name, role, rounds: (interviewRounds || []).join(', '), year: String(year || ''), source: source || 'StudentSphere user submission', title: experienceTitle });
    res.status(201).json(await InterviewExperience.findById(interview._id).populate('user', 'name college').populate('company', 'name logo'));
  } catch (error) { res.status(500).json({ message: 'Server error', error: error.message }); }
};

const updateInterview = async (req, res) => {
  try {
    const interview = await InterviewExperience.findById(req.params.id);
    if (!interview) return res.status(404).json({ message: 'Interview experience not found' });
    if (interview.user.toString() !== req.user._id.toString()) return res.status(403).json({ message: 'Not authorized to update this interview' });
    const { company, role, experienceTitle, experienceText, interviewRounds, difficulty, year, topics, questions, source } = req.body;
    const textChanged = Boolean(experienceText && experienceText !== interview.experienceText);
    let companyDoc = await Company.findById(interview.company);
    if (company && company.toLowerCase() !== companyDoc?.name?.toLowerCase()) {
      companyDoc = await Company.findOne({ name: new RegExp(`^${company}$`, 'i') }) || await Company.create({ name: company, roles: role ? [role] : [] });
      interview.company = companyDoc._id;
    }
    Object.assign(interview, { role: role || interview.role, experienceTitle: experienceTitle || interview.experienceTitle, experienceText: experienceText || interview.experienceText, interviewRounds: interviewRounds || interview.interviewRounds, difficulty: difficulty || interview.difficulty, year: year || interview.year, topics: topics || interview.topics, questions: questions || interview.questions, source: source || interview.source });
    if (textChanged) interview.aiProcessed = false;
    const updated = await interview.save();
    if (textChanged) processWithAI(updated._id, updated.experienceText, { interviewId: String(updated._id), companyId: String(updated.company), companyName: companyDoc?.name || '', role: updated.role, rounds: (updated.interviewRounds || []).join(', '), year: String(updated.year || ''), source: updated.source || 'StudentSphere user submission', title: updated.experienceTitle });
    res.json(await InterviewExperience.findById(updated._id).populate('user', 'name college').populate('company', 'name logo'));
  } catch (error) { res.status(500).json({ message: 'Server error', error: error.message }); }
};

const deleteInterview = async (req, res) => {
  try {
    const interview = await InterviewExperience.findById(req.params.id);
    if (!interview) return res.status(404).json({ message: 'Interview experience not found' });
    if (interview.user.toString() !== req.user._id.toString()) return res.status(403).json({ message: 'Not authorized to delete this interview' });
    const company = await Company.findById(interview.company); if (company?.interviewCount > 0) { company.interviewCount -= 1; await company.save(); }
    await interview.deleteOne(); res.json({ message: 'Interview experience removed' });
  } catch (error) { res.status(500).json({ message: 'Server error', error: error.message }); }
};

const getInterviewStats = async (req, res) => {
  try {
    const [totalInterviews, totalCompanies, difficultyStats, yearStats, topicStats, roleStats, companyStats] = await Promise.all([
      InterviewExperience.countDocuments(), Company.countDocuments(),
      InterviewExperience.aggregate([{ $group: { _id: '$difficulty', count: { $sum: 1 } } }]),
      InterviewExperience.aggregate([{ $group: { _id: '$year', count: { $sum: 1 } } }, { $sort: { _id: -1 } }]),
      InterviewExperience.aggregate([{ $unwind: '$topics' }, { $group: { _id: '$topics', count: { $sum: 1 } } }, { $sort: { count: -1 } }, { $limit: 10 }]),
      InterviewExperience.aggregate([{ $group: { _id: '$role', count: { $sum: 1 } } }, { $sort: { count: -1 } }, { $limit: 10 }]),
      InterviewExperience.aggregate([{ $lookup: { from: 'companies', localField: 'company', foreignField: '_id', as: 'companyInfo' } }, { $unwind: '$companyInfo' }, { $group: { _id: '$company', companyName: { $first: '$companyInfo.name' }, count: { $sum: 1 } } }, { $sort: { count: -1 } }, { $limit: 10 }]),
    ]);
    res.json({ totalInterviews, totalCompanies, difficultyStats, yearStats, topicStats, roleStats, companyStats });
  } catch (error) { res.status(500).json({ message: 'Server error', error: error.message }); }
};

const internalAIUpdate = async (req, res) => {
  try {
    const interview = await InterviewExperience.findById(req.params.id); if (!interview) return res.status(404).json({ message: 'Interview experience not found' });
    ['aiSummary', 'aiExtractedTopics', 'aiExtractedQuestions', 'aiProcessed'].forEach((field) => { if (req.body[field] !== undefined) interview[field] = req.body[field]; });
    const updated = await interview.save(); res.json({ status: 'success', interviewId: updated._id, aiProcessed: updated.aiProcessed });
  } catch (error) { res.status(500).json({ message: 'Server error', error: error.message }); }
};
module.exports = { getInterviews, getInterviewById, createInterview, updateInterview, deleteInterview, getInterviewStats, internalAIUpdate };
