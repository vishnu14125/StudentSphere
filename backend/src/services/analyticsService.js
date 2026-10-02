const InterviewExperience = require('../models/InterviewExperience');

const matchFor = ({ companyId, role, year } = {}) => {
  const match = {};
  if (companyId) match.company = companyId;
  if (role) match.role = { $regex: role, $options: 'i' };
  if (year) match.year = Number(year);
  return match;
};

const withPercentages = (rows, total) => rows.map((row) => ({ ...row, percentage: total ? Math.round((row.count / total) * 100) : 0 }));

const getAnalytics = async (filters = {}) => {
  const match = matchFor(filters);
  const totalInterviews = await InterviewExperience.countDocuments(match);
  const base = [{ $match: match }];
  const [difficultyRows, topicStats, questionStats, roleStats, companyStats, yearStats, roundStats] = await Promise.all([
    InterviewExperience.aggregate([...base, { $group: { _id: '$difficulty', count: { $sum: 1 } } }]),
    InterviewExperience.aggregate([...base, { $project: { values: { $setUnion: [{ $ifNull: ['$topics', []] }, { $ifNull: ['$aiExtractedTopics', []] }] } } }, { $unwind: '$values' }, { $group: { _id: '$values', count: { $sum: 1 } } }, { $sort: { count: -1, _id: 1 } }, { $limit: 12 }]),
    InterviewExperience.aggregate([...base, { $project: { values: { $setUnion: [{ $ifNull: ['$questions', []] }, { $ifNull: ['$aiExtractedQuestions', []] }] } } }, { $unwind: '$values' }, { $group: { _id: '$values', count: { $sum: 1 } } }, { $sort: { count: -1, _id: 1 } }, { $limit: 12 }]),
    InterviewExperience.aggregate([...base, { $group: { _id: '$role', count: { $sum: 1 } } }, { $sort: { count: -1, _id: 1 } }, { $limit: 10 }]),
    InterviewExperience.aggregate([...base, { $lookup: { from: 'companies', localField: 'company', foreignField: '_id', as: 'companyInfo' } }, { $unwind: '$companyInfo' }, { $group: { _id: '$company', companyName: { $first: '$companyInfo.name' }, count: { $sum: 1 } } }, { $sort: { count: -1, companyName: 1 } }, { $limit: 10 }]),
    InterviewExperience.aggregate([...base, { $group: { _id: '$year', count: { $sum: 1 } } }, { $sort: { _id: 1 } }]),
    InterviewExperience.aggregate([...base, { $unwind: '$interviewRounds' }, { $group: { _id: '$interviewRounds', count: { $sum: 1 } } }, { $sort: { count: -1, _id: 1 } }, { $limit: 8 }]),
  ]);
  const difficultyDistribution = ['Easy', 'Medium', 'Hard'].map((name) => {
    const count = difficultyRows.find((row) => row._id === name)?.count || 0;
    return { _id: name, count, percentage: totalInterviews ? Math.round((count / totalInterviews) * 100) : 0 };
  });
  return { totalInterviews, difficultyDistribution, topicStats: withPercentages(topicStats, totalInterviews), questionStats, roleStats, companyStats, yearStats, roundStats };
};

module.exports = { getAnalytics, matchFor };
