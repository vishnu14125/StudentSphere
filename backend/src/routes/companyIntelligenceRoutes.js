const express = require('express');
const { getCompanyIntelligence, triggerCompanyAnalysis } = require('../controllers/companyIntelligenceController');
const { protect } = require('../middleware/auth');
const router = express.Router();
router.get('/:id/intelligence', getCompanyIntelligence); router.post('/:id/analyze', protect, triggerCompanyAnalysis);
module.exports = router;
