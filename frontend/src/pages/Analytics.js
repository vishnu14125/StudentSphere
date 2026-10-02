import React, { useEffect, useState } from 'react';
import api from '../lib/api';
import PageHeader from '../components/PageHeader';
import Card from '../components/Card';
import ProgressBar from '../components/ProgressBar';
import Badge from '../components/Badge';
import EmptyState from '../components/EmptyState';
const Analytics = () => {
  const [data, setData] = useState(null); const [error, setError] = useState('');
  useEffect(() => { api.get('/analytics/overview').then((response) => setData(response.data)).catch((requestError) => setError(requestError.response?.data?.message || 'Unable to load analytics.')); }, []);
  if (error) return <EmptyState icon="!" title="Analytics unavailable" description={error} />;
  if (!data) return <div className="text-sm text-slate-300">Calculating live analytics...</div>;
  return <div className="space-y-8"><PageHeader eyebrow="Analytics" title="Interview Analytics" subtitle="Live trends calculated from the StudentSphere interview repository." />
    <div className="grid gap-4 md:grid-cols-3"><Card className="p-5"><p className="metric-kicker">Experiences analysed</p><p className="mt-3 text-3xl font-semibold text-white">{data.totalInterviews}</p></Card><Card className="p-5"><p className="metric-kicker">Questions identified</p><p className="mt-3 text-3xl font-semibold text-white">{data.questionStats.length}</p></Card><Card className="p-5"><p className="metric-kicker">Years represented</p><p className="mt-3 text-3xl font-semibold text-white">{data.yearStats.length}</p></Card></div>
    {!data.totalInterviews ? <EmptyState icon="i" title="No analytics yet" description="Add interview experiences to populate this dashboard." /> : <div className="grid gap-6 xl:grid-cols-2"><Card className="p-6"><h2 className="section-title">Topic Frequency</h2><div className="mt-6 space-y-4">{data.topicStats.map((item) => <ProgressBar key={item._id} label={item._id} value={item.percentage} hint={`${item.count} mentions`} tone="blue" />)}</div></Card><Card className="p-6"><h2 className="section-title">Difficulty Distribution</h2><div className="mt-6 grid gap-4 md:grid-cols-3">{data.difficultyDistribution.map((item) => <div key={item._id} className="surface-muted p-4"><p className="metric-kicker">{item._id}</p><p className="mt-3 text-3xl font-semibold text-white">{item.percentage}%</p><p className="mt-1 text-xs text-slate-400">{item.count} experience(s)</p></div>)}</div></Card><Card className="p-6"><h2 className="section-title">Popular Roles</h2><div className="mt-5 flex flex-wrap gap-2">{data.roleStats.map((item) => <Badge key={item._id} tone="green">{item._id} · {item.count}</Badge>)}</div><h2 className="section-title mt-7">Common Questions</h2><div className="mt-4 space-y-2">{data.questionStats.slice(0, 5).map((item) => <div key={item._id} className="surface-muted p-3 text-sm text-slate-200">{item._id} <span className="text-slate-500">({item.count})</span></div>)}</div></Card><Card className="p-6"><h2 className="section-title">Company Comparison</h2><div className="mt-6 space-y-4">{data.companyStats.map((item) => <ProgressBar key={item.companyName} label={item.companyName} value={Math.round((item.count / data.totalInterviews) * 100)} hint={`${item.count} experience(s)`} tone="purple" />)}</div></Card></div>}
  </div>;
};
export default Analytics;
