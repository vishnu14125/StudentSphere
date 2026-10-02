const Company = require('../models/Company');
const InterviewExperience = require('../models/InterviewExperience');

// @desc    Get all companies
// @route   GET /api/companies
// @access  Public
const getCompanies = async (req, res) => {
  try {
    const { search } = req.query;
    
    let query = {};
    
    if (search) {
      query.name = { $regex: search, $options: 'i' };
    }

    const companies = await Company.find(query).sort({ name: 1 });

    res.json(companies);
  } catch (error) {
    res.status(500).json({ message: 'Server error', error: error.message });
  }
};

// @desc    Get single company
// @route   GET /api/companies/:id
// @access  Public
const getCompanyById = async (req, res) => {
  try {
    const company = await Company.findById(req.params.id);

    if (company) {
      res.json(company);
    } else {
      res.status(404).json({ message: 'Company not found' });
    }
  } catch (error) {
    res.status(500).json({ message: 'Server error', error: error.message });
  }
};

// @desc    Create a company
// @route   POST /api/companies
// @access  Private (Admin)
const createCompany = async (req, res) => {
  try {
    const { name, logo, industry, description, roles } = req.body;

    const companyExists = await Company.findOne({ name });

    if (companyExists) {
      return res.status(400).json({ message: 'Company already exists' });
    }

    const company = await Company.create({
      name,
      logo,
      industry,
      description,
      roles: roles || [],
    });

    res.status(201).json(company);
  } catch (error) {
    res.status(500).json({ message: 'Server error', error: error.message });
  }
};

// @desc    Update a company
// @route   PUT /api/companies/:id
// @access  Private (Admin)
const updateCompany = async (req, res) => {
  try {
    const company = await Company.findById(req.params.id);

    if (company) {
      company.name = req.body.name || company.name;
      company.logo = req.body.logo || company.logo;
      company.industry = req.body.industry || company.industry;
      company.description = req.body.description || company.description;
      company.roles = req.body.roles || company.roles;

      const updatedCompany = await company.save();
      res.json(updatedCompany);
    } else {
      res.status(404).json({ message: 'Company not found' });
    }
  } catch (error) {
    res.status(500).json({ message: 'Server error', error: error.message });
  }
};

// @desc    Delete a company
// @route   DELETE /api/companies/:id
// @access  Private (Admin)
const deleteCompany = async (req, res) => {
  try {
    const company = await Company.findById(req.params.id);

    if (company) {
      await company.deleteOne();
      res.json({ message: 'Company removed' });
    } else {
      res.status(404).json({ message: 'Company not found' });
    }
  } catch (error) {
    res.status(500).json({ message: 'Server error', error: error.message });
  }
};

// @desc    Seed companies with initial data
// @route   POST /api/companies/seed
// @access  Private (Admin)
const seedCompanies = async (req, res) => {
  try {
    const companiesData = [
      {
        name: 'Amazon',
        industry: 'E-commerce & Cloud',
        description: 'Global technology company focused on e-commerce, cloud computing, and AI',
        roles: ['SDE', 'SDE-1', 'SDE-2', 'Data Engineer', 'DevOps Engineer'],
      },
      {
        name: 'Microsoft',
        industry: 'Software & Cloud',
        description: 'Technology company known for Windows, Azure, and productivity software',
        roles: ['Software Engineer', 'Data Scientist', 'Product Manager', 'Cloud Architect'],
      },
      {
        name: 'Google',
        industry: 'Internet & Software',
        description: 'Search engine and technology company',
        roles: ['Software Engineer', 'Data Engineer', 'Product Manager', 'ML Engineer'],
      },
      {
        name: 'Zoho',
        industry: 'Software',
        description: 'Indian software development company',
        roles: ['Software Developer', 'QA Engineer', 'Technical Support'],
      },
      {
        name: 'TCS',
        industry: 'IT Services',
        description: 'Tata Consultancy Services - IT consulting and services',
        roles: ['System Engineer', 'Developer', 'QA Engineer'],
      },
      {
        name: 'Infosys',
        industry: 'IT Services',
        description: 'Indian multinational IT services company',
        roles: ['Systems Engineer', 'Technology Analyst', 'Consultant'],
      },
      {
        name: 'Accenture',
        industry: 'IT Services',
        description: 'Global professional services company',
        roles: ['Software Engineer', 'Analyst', 'Consultant'],
      },
      {
        name: 'Meta',
        industry: 'Social Media & VR',
        description: 'Technology company focused on social media and virtual reality',
        roles: ['Software Engineer', 'Data Scientist', 'Product Manager'],
      },
      {
        name: 'Apple',
        industry: 'Consumer Electronics',
        description: 'Technology company known for iPhone, Mac, and other devices',
        roles: ['Software Engineer', 'iOS Developer', 'Data Engineer'],
      },
      {
        name: 'Netflix',
        industry: 'Entertainment',
        description: 'Streaming service and entertainment company',
        roles: ['Software Engineer', 'Data Engineer', 'ML Engineer'],
      },
    ];

    const insertedCompanies = await Company.insertMany(companiesData);
    
    res.status(201).json({
      message: 'Companies seeded successfully',
      count: insertedCompanies.length,
      companies: insertedCompanies,
    });
  } catch (error) {
    res.status(500).json({ message: 'Server error', error: error.message });
  }
};

module.exports = {
  getCompanies,
  getCompanyById,
  createCompany,
  updateCompany,
  deleteCompany,
  seedCompanies,
};
