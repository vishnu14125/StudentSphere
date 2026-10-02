const express = require('express');
const { generate, getProgress, updateProgress } = require('../controllers/roadmapController');
const { protect } = require('../middleware/auth');
const router = express.Router();
router.use(protect); router.post('/generate', generate); router.get('/progress', getProgress); router.put('/progress', updateProgress);
module.exports = router;
