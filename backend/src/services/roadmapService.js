const Company = require('../models/Company');
const { getAnalytics } = require('./analyticsService');
const generateRoadmap = async ({ company, role, durationDays = 28, skills = [], weakAreas = [] }) => {
  const companyDoc = company ? await Company.findOne({ name: new RegExp(`^${company}$`, 'i') }) : null;
  const companyData = await getAnalytics({ companyId: companyDoc?._id, role });
  const roleData = !companyData.totalInterviews && role ? await getAnalytics({ role }) : null;
  const data = roleData || companyData;
  const priorities = data.topicStats.map((item) => item._id).filter(Boolean).slice(0, 10);
  const topics = priorities.length ? priorities : ['Data Structures and Algorithms', 'Core CS Fundamentals', 'Problem Solving', 'Communication'];
  const days = Math.max(7, Math.min(Number(durationDays) || 28, 84));
  const weekCount = Math.max(1, Math.ceil(days / 7));
  const roadmap = Array.from({ length: weekCount }, (_, index) => {
    const focus = topics.filter((_, topicIndex) => topicIndex % weekCount === index).slice(0, 3);
    const last = index === weekCount - 1;
    return { week: index + 1, title: last ? 'Revision and interview simulation' : `Week ${index + 1} preparation`, focus: last ? [...focus, 'Mock interview', 'Revision'] : (focus.length ? focus : topics.slice(0, 2)), practice: last ? ['Timed mock interview', 'Review weak areas'] : ['Learn concepts', 'Solve timed problems', 'Explain solutions aloud'] };
  });
  return { targetCompany: companyDoc?.name || company || 'General preparation', targetRole: role || 'Target role', durationDays: days, dataScope: companyData.totalInterviews ? 'company and role data' : roleData?.totalInterviews ? 'role-level data because company-specific data is limited' : 'general preparation guidance because matching data is limited', priorityTopics: topics, weakAreas: weakAreas.length ? weakAreas : topics.filter((topic) => !skills.some((skill) => skill.toLowerCase() === topic.toLowerCase())).slice(0, 3), roadmap };
};
module.exports = { generateRoadmap };
