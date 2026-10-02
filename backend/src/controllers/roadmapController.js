const UserProgress = require('../models/UserProgress');
const { generateRoadmap } = require('../services/roadmapService');
const generate = async (req, res) => {
  try {
    const { company, role, durationDays, skills = [], weakAreas = [] } = req.body;
    if (!role) return res.status(400).json({ message: 'Target role is required.' });
    const result = await generateRoadmap({ company, role, durationDays, skills, weakAreas });
    const progress = await UserProgress.findOneAndUpdate({ user: req.user._id }, { user: req.user._id, targetCompany: result.targetCompany, targetRole: result.targetRole, durationDays: result.durationDays, roadmap: result.roadmap.map((week) => ({ ...week, completedTopics: [] })), weakAreas: result.weakAreas, lastActivity: new Date() }, { upsert: true, new: true, setDefaultsOnInsert: true });
    res.json({ ...result, progress });
  } catch (error) { res.status(500).json({ message: 'Unable to generate roadmap', error: error.message }); }
};
const getProgress = async (req, res) => { const progress = await UserProgress.findOne({ user: req.user._id }); res.json(progress || { roadmap: [], topicsProgress: [], preparationStreak: 0 }); };
const updateProgress = async (req, res) => {
  try {
    const { topic, completed, score } = req.body;
    if (!topic) return res.status(400).json({ message: 'Topic is required.' });
    const progress = await UserProgress.findOneAndUpdate({ user: req.user._id }, { $setOnInsert: { user: req.user._id }, $pull: { topicsProgress: { topic } } }, { upsert: true, new: true });
    progress.topicsProgress.push({ topic, completed: Boolean(completed), score });
    progress.lastActivity = new Date();
    progress.preparationStreak = completed ? Math.max(1, progress.preparationStreak + 1) : progress.preparationStreak;
    await progress.save();
    res.json(progress);
  } catch (error) { res.status(500).json({ message: 'Unable to update progress', error: error.message }); }
};
module.exports = { generate, getProgress, updateProgress };
