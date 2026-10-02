import React, { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';
import api from '../lib/api';
import PageHeader from '../components/PageHeader';
import Card from '../components/Card';
import Badge from '../components/Badge';
import ProgressBar from '../components/ProgressBar';
import InterviewCard from '../components/InterviewCard';
import AICard from '../components/AICard';
import EmptyState from '../components/EmptyState';

const CompanyDetails = () => {
  const { id } = useParams();
  const [data, setData] = useState(null); const [error, setError] = useState('');
  useEffect(() => { api.get(`/companies/${id}/intelligence`).then((response) => setData(response.data)).catch((requestError) => setError(requestError.response?.data?.message || 'Unable to load company intelligence.')); }, [id]);
  if (error) return <EmptyState icon="!" title="Company intelligence unavailable" description={error} />;
  if (!data) return <div className="text-sm text-slate-300">Loading company intelligence...</div>;
  const difficulty = ['Easy', 'Medium', 'Hard'].map((label) => ({ label, count: data.difficultyDistribution?.[label] || 0 }));
  const total = data.totalExperiences || 0;
  return <div className="space-y-8">
    <PageHeader eyebrow="Company Intelligence" title={data.company.name} subtitle="Live analytics calculated from recorded interview experiences." />
    <div className="grid gap-4 md:grid-cols-2 xl:grid-cols-4">
      {[['Experiences', total], ['Topics', data.topicFrequency?.length || 0], ['Questions', data.commonQuestions?.length || 0], ['Roles', data.roleBreakdown?.length || 0]].map(([label, value]) => <Card key={label} className="p-5"><p className="metric-kicker">{label}</p><p className="mt-3 text-3xl font-semibold text-white">{value}</p></Card>)}
    </div>
    {!total ? <EmptyState icon="i" title="No company data yet" description="Submit a sourced interview experience for this company to generate analytics." /> : <div className="page-grid">
      <div className="space-y-6"><Card className="p-6"><h2 className="section-title">Interview Difficulty</h2><div className="mt-5 space-y-4">{difficulty.map((item) => <ProgressBar key={item.label} label={item.label} value={total ? Math.round((item.count / total) * 100) : 0} hint={`${item.count} experience(s)`} tone={item.label === 'Easy' ? 'green' : item.label === 'Medium' ? 'amber' : 'red'} />)}</div></Card>
      <Card className="p-6"><h2 className="section-title">Most Asked Questions</h2><div className="mt-5 space-y-3">{data.commonQuestions?.length ? data.commonQuestions.map((question, index) => <div key={`${question.question}-${index}`} className="surface-muted flex items-center justify-between gap-3 p-4"><span className="text-sm text-slate-100">{question.question}</span><Badge tone="blue">{question.frequency} mentions</Badge></div>) : <p className="text-sm text-slate-400">Questions have not been recorded yet.</p>}</div></Card>
      <Card className="p-6"><h2 className="section-title">Recent Experiences</h2><div className="mt-5 grid gap-4 xl:grid-cols-2">{data.recentExperiences?.map((item) => <InterviewCard key={item._id} interview={item} />)}</div></Card></div>
      <div className="space-y-6"><Card className="p-6"><h2 className="section-title">Most Asked Topics</h2><div className="mt-5 space-y-4">{data.topicFrequency?.map((item) => <ProgressBar key={item.topic} label={item.topic} value={item.percentage} hint={`${item.count} mentions`} tone="purple" />)}</div></Card>
      <Card className="p-6"><h2 className="section-title">Interview Pattern</h2><div className="mt-5 space-y-3">{data.interviewPattern?.map((step) => <div key={step} className="surface-muted p-4 text-sm text-slate-100">{step}</div>)}</div></Card>
      <AICard title="Evidence-based insight" subtitle="Generated from the available company records."><p className="text-sm leading-6 text-slate-100">{data.aiInsight}</p></AICard></div>
    </div>}
  </div>;
};
export default CompanyDetails;
