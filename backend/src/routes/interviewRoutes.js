const express = require('express');
const router = express.Router();
const {
  getInterviews,
  getInterviewById,
  createInterview,
  updateInterview,
  deleteInterview,
  getInterviewStats,
  internalAIUpdate,
} = require('../controllers/interviewController');
const { protect } = require('../middleware/auth');
const { interviewValidation, validate } = require('../validators/interviewValidator');

router.get('/', getInterviews);
router.get('/stats', getInterviewStats);
router.get('/:id', getInterviewById);
router.post('/', protect, interviewValidation, validate, createInterview);
router.put('/:id', protect, updateInterview);
router.delete('/:id', protect, deleteInterview);

// Internal AI update endpoint (no auth for AI service communication)
router.put('/:id/ai-update', internalAIUpdate);

module.exports = router;
