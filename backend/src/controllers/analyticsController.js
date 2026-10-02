const { getAnalytics } = require('../services/analyticsService');

const getOverview = async (req, res) => {
  try { res.json(await getAnalytics(req.query)); }
  catch (error) { res.status(500).json({ message: 'Unable to calculate analytics', error: error.message }); }
};
const getTopics = async (req, res) => { try { res.json((await getAnalytics(req.query)).topicStats); } catch (error) { res.status(500).json({ message: error.message }); } };
const getQuestions = async (req, res) => { try { res.json((await getAnalytics(req.query)).questionStats); } catch (error) { res.status(500).json({ message: error.message }); } };
const getCompanies = async (req, res) => { try { res.json((await getAnalytics(req.query)).companyStats); } catch (error) { res.status(500).json({ message: error.message }); } };
const getTrends = async (req, res) => { try { res.json((await getAnalytics(req.query)).yearStats); } catch (error) { res.status(500).json({ message: error.message }); } };
module.exports = { getOverview, getTopics, getQuestions, getCompanies, getTrends };
