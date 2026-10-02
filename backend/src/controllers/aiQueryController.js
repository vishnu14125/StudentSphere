const axios = require('axios');
const Company = require('../models/Company');
const InterviewExperience = require('../models/InterviewExperience');

const aiUrl = () => process.env.AI_SERVICE_URL || 'http://localhost:8000';
const queryAI = async (req, res) => {
  const { query, companyId, company, role, round, year, topK = 5 } = req.body;
  if (!query || !query.trim()) return res.status(400).json({ message: 'A question is required.' });
  try {
    let resolvedCompanyId = companyId;
    if (!resolvedCompanyId && company) resolvedCompanyId = (await Company.findOne({ name: new RegExp(`^${company}$`, 'i') }))?._id;
    const filter = {};
    if (resolvedCompanyId) filter.company = resolvedCompanyId;
    if (role) filter.role = { $regex: role.trim(), $options: 'i' };
    if (round) filter.interviewRounds = { $regex: round.trim(), $options: 'i' };
    if (year) filter.year = Number(year);
    const interviews = await InterviewExperience.find(filter).populate('company', 'name').sort({ createdAt: -1 }).limit(100);
    if (!interviews.length) return res.json({ answer: 'Insufficient interview data matches this question. Try removing a filter or add a relevant interview experience.', insights: [], sources: [], grounded: true });
    const documents = interviews.map((item) => ({
      id: String(item._id), text: item.experienceText, metadata: { interviewId: String(item._id), companyId: String(item.company._id), companyName: item.company.name, role: item.role || '', rounds: (item.interviewRounds || []).join(', '), year: String(item.year || ''), source: item.source || 'StudentSphere submission', title: item.experienceTitle || 'Interview experience' },
    }));
    await axios.post(`${aiUrl()}/api/ai/index`, { documents }, { timeout: 30000 });
    const response = await axios.post(`${aiUrl()}/api/ai/query`, { query, n_results: Math.min(Math.max(Number(topK) || 5, 1), 8), filters: resolvedCompanyId ? { companyId: String(resolvedCompanyId) } : null }, { timeout: 60000 });
    res.json(response.data);
  } catch (error) {
    res.status(503).json({ message: 'The AI service is unavailable. Start the AI service and try again.', error: error.message });
  }
};
const health = async (_req, res) => { try { const { data } = await axios.get(`${aiUrl()}/api/ai/health`, { timeout: 4000 }); res.json(data); } catch { res.status(503).json({ status: 'unavailable' }); } };
module.exports = { queryAI, health };
