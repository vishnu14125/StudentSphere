const express = require('express');
const { getOverview, getTopics, getQuestions, getCompanies, getTrends } = require('../controllers/analyticsController');
const router = express.Router();
router.get('/overview', getOverview); router.get('/topics', getTopics); router.get('/questions', getQuestions); router.get('/companies', getCompanies); router.get('/trends', getTrends);
module.exports = router;
