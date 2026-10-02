const Company = require('../models/Company');
const InterviewExperience = require('../models/InterviewExperience');
const { getAnalytics } = require('./analyticsService');

const calculateCompanyIntelligence = async (companyId) => {
  const company = await Company.findById(companyId);
  if (!company) return null;
  const data = await getAnalytics({ companyId: company._id });
  const topicFrequency = data.topicStats.map((item) => ({ topic: item._id, count: item.count, percentage: item.percentage }));
  const commonQuestions = data.questionStats.map((item) => ({ question: item._id, frequency: item.count }));
  const difficultyDistribution = Object.fromEntries(data.difficultyDistribution.map((item) => [item._id, item.count]));
  const topTopics = topicFrequency.slice(0, 3).map((item) => item.topic);
  const interviewPattern = data.roundStats.length
    ? data.roundStats.slice(0, 4).map((item, index) => `${index + 1}. ${item._id} reported in ${item.count} experience(s).`)
    : ['Interview-round information is not available yet.'];
  return { company: { _id: company._id, name: company.name, industry: company.industry, roles: company.roles }, totalExperiences: data.totalInterviews, difficultyDistribution, topicFrequency, commonQuestions, interviewPattern, roleBreakdown: data.roleStats, roundBreakdown: data.roundStats, aiInsight: data.totalInterviews ? `${company.name} has ${data.totalInterviews} recorded experience(s). Prioritize ${topTopics.join(', ') || 'the listed topics'} and practise the reported round sequence.` : `Add interview experiences for ${company.name} to generate a reliable insight.`, lastAnalyzed: new Date() };
};

const persistCompanyIntelligence = async (companyId) => {
  const data = await calculateCompanyIntelligence(companyId);
  if (!data) return null;
  await Company.findByIdAndUpdate(companyId, { intelligence: { difficultyDistribution: data.difficultyDistribution, topicFrequency: data.topicFrequency, commonQuestions: data.commonQuestions, interviewPattern: data.interviewPattern, aiInsight: data.aiInsight }, lastAnalyzed: data.lastAnalyzed });
  return data;
};

const recentCompanyExperiences = (companyId) => InterviewExperience.find({ company: companyId }).populate('user', 'name college').populate('company', 'name logo').sort({ createdAt: -1 }).limit(6);
module.exports = { calculateCompanyIntelligence, persistCompanyIntelligence, recentCompanyExperiences };
