const { calculateCompanyIntelligence, persistCompanyIntelligence, recentCompanyExperiences } = require('../services/companyIntelligenceService');
const getCompanyIntelligence = async (req, res) => {
  try {
    const intelligence = await calculateCompanyIntelligence(req.params.id);
    if (!intelligence) return res.status(404).json({ message: 'Company not found' });
    const recentExperiences = await recentCompanyExperiences(req.params.id);
    res.json({ ...intelligence, recentExperiences });
  } catch (error) { res.status(500).json({ message: 'Unable to calculate company intelligence', error: error.message }); }
};
const triggerCompanyAnalysis = async (req, res) => {
  try {
    const intelligence = await persistCompanyIntelligence(req.params.id);
    if (!intelligence) return res.status(404).json({ message: 'Company not found' });
    res.json(intelligence);
  } catch (error) { res.status(500).json({ message: 'Unable to analyse company', error: error.message }); }
};
module.exports = { getCompanyIntelligence, triggerCompanyAnalysis };
