const express = require('express');
const { queryAI, health } = require('../controllers/aiQueryController');
const { protect } = require('../middleware/auth');
const router = express.Router();
router.get('/health', health); router.post('/query', protect, queryAI);
module.exports = router;
