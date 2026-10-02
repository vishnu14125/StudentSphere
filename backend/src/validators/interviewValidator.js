const { body, validationResult } = require('express-validator');

const interviewValidation = [
  body('company')
    .notEmpty()
    .withMessage('Company is required'),
  body('role')
    .trim()
    .notEmpty()
    .withMessage('Role is required'),
  body('experienceTitle')
    .trim()
    .notEmpty()
    .withMessage('Experience title is required'),
  body('experienceText')
    .trim()
    .notEmpty()
    .withMessage('Experience text is required'),
  body('difficulty')
    .optional()
    .isIn(['Easy', 'Medium', 'Hard'])
    .withMessage('Difficulty must be Easy, Medium, or Hard'),
  body('year')
    .isInt({ min: 2015, max: 2026 })
    .withMessage('Please provide a valid year'),
  body('source')
    .optional()
    .trim(),
];

const validate = (req, res, next) => {
  const errors = validationResult(req);
  if (!errors.isEmpty()) {
    return res.status(400).json({ errors: errors.array() });
  }
  next();
};

module.exports = {
  interviewValidation,
  validate,
};
