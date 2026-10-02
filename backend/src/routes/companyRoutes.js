const express = require('express');
const router = express.Router();
const {
  getCompanies,
  getCompanyById,
  createCompany,
  updateCompany,
  deleteCompany,
  seedCompanies,
} = require('../controllers/companyController');
const { protect } = require('../middleware/auth');

router.get('/', getCompanies);
router.get('/:id', getCompanyById);
router.post('/', protect, createCompany);
router.put('/:id', protect, updateCompany);
router.delete('/:id', protect, deleteCompany);
router.post('/seed', protect, seedCompanies);

module.exports = router;
