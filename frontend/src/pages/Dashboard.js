import React, { useEffect, useMemo, useState } from 'react';
import { Link } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import api from '../lib/api';
import { demoAIRecommendations, demoDashboardStats, demoInterviews } from '../data/demoData';
import PageHeader from '../components/PageHeader';
import StatCard from '../components/StatCard';
import AICard from '../components/AICard';
import Card from '../components/Card';
import ProgressBar from '../components/ProgressBar';
import SectionHeader from '../components/SectionHeader';
import InterviewCard from '../components/InterviewCard';
import SkeletonLoader from '../components/SkeletonLoader';
import Badge from '../components/Badge';

const Dashboard = () => {
  const { user } = useAuth();
  const [stats, setStats] = useState(null);
  const [recentInterviews, setRecentInterviews] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const loadDashboard = async () => {
      try {
        const [statsResponse, interviewsResponse] = await Promise.all([
          api.get('/interviews/stats'),
          api.get('/interviews', { params: { limit: 5 } }),
        ]);

        setStats(statsResponse.data);
        setRecentInterviews(interviewsResponse.data?.interviews || []);
      } catch (error) {
        console.error('Failed to load dashboard, using demo data.', error);
        setStats(null);
        setRecentInterviews([]);
      } finally {
        setLoading(false);
      }
    };

    loadDashboard();
  }, []);

  const mergedStats = useMemo(() => {
    const source = stats || demoDashboardStats;
    const totalQuestions = source.totalQuestions || source.topicStats.reduce((sum, item) => sum + item.count, 0);
    const totalTopics = source.totalTopics || source.topicStats.length;

    return {
      ...source,
      totalQuestions,
      totalTopics,
    };
  }, [stats]);

  const displayInterviews = recentInterviews.length ? recentInterviews : demoInterviews;

  if (loading) {
    return (
      <div className="space-y-8">
        <PageHeader
          eyebrow="Dashboard"
          title="Preparing your placement intelligence view"
          subtitle="We are assembling interview patterns, topic momentum, and AI insights."
        />
        <SkeletonLoader type="stat" count={4} />
      </div>
    );
  }

  return (
    <div className="space-y-8">
      <PageHeader
        eyebrow="Dashboard"
        title={`Good morning, ${user?.name?.split(' ')[0] || 'Vishnu'}`}
        subtitle="Your interview preparation intelligence at a glance."
        actions={
          <>
            <Link to="/companies" className="btn-secondary">
              Explore Companies
            </Link>
            <Link to="/submit-interview" className="btn-primary">
              Submit Experience
            </Link>
          </>
        }
      />

      <div className="grid gap-4 md:grid-cols-2 xl:grid-cols-4">
        <StatCard title="Interview Experiences" value={mergedStats.totalInterviews} color="blue" helper="Tracked interview stories" icon={<span>128</span>} />
        <StatCard title="Companies" value={mergedStats.totalCompanies} color="green" helper="Company intelligence nodes" icon={<span>24</span>} />
        <StatCard title="Questions Analyzed" value={mergedStats.totalQuestions} color="amber" helper="Questions recognized by topic" icon={<span>842</span>} />
        <StatCard title="Topics Identified" value={mergedStats.totalTopics} color="purple" helper="Preparation themes across interviews" icon={<span>36</span>} />
      </div>

      <div className="page-grid">
        <div className="space-y-6">
          <Card className="p-6">
            <SectionHeader title="Trending Interview Topics" description="What is appearing most often in the current interview knowledge base." />
            <div className="mt-6 space-y-4">
              {mergedStats.topicStats.slice(0, 5).map((topic, index) => (
                <ProgressBar
                  key={topic._id}
                  label={topic._id}
                  value={topic.count}
                  tone={index < 2 ? 'blue' : index === 2 ? 'green' : 'purple'}
                  hint={`${topic.count}%`}
                />
              ))}
            </div>
          </Card>

          <Card className="p-6">
            <SectionHeader title="Interview Difficulty" description="Current mix of easy, medium, and hard interview experiences." />
            <div className="mt-6 grid gap-4 md:grid-cols-3">
              {mergedStats.difficultyStats.map((item) => (
                <div key={item._id} className="surface-muted p-4">
                  <p className="metric-kicker">{item._id}</p>
                  <p className="mt-2 text-3xl font-semibold text-white">{item.count}%</p>
                  <div className="mt-4 h-2 rounded-full bg-slate-800">
                    <div
                      className={`h-full rounded-full ${
                        item._id === 'Easy' ? 'bg-emerald-500' : item._id === 'Medium' ? 'bg-amber-500' : 'bg-rose-500'
                      }`}
                      style={{ width: `${item.count}%` }}
                    />
                  </div>
                </div>
              ))}
            </div>
          </Card>

          <Card className="p-6">
            <SectionHeader
              title="Recent Experiences"
              description="The latest interview stories available for your demo flow."
              action={<Link to="/interviews" className="btn-ghost">Browse all</Link>}
            />
            <div className="mt-6 grid gap-4 xl:grid-cols-2">
              {displayInterviews.slice(0, 4).map((interview) => (
                <InterviewCard key={interview._id} interview={interview} />
              ))}
            </div>
          </Card>
        </div>

        <div className="space-y-6">
          <AICard
            title="StudentSphere AI recommends"
            subtitle="Demo-ready recommendations backed by the current topic mix."
          >
            <div className="space-y-4">
              {demoAIRecommendations.map((item) => (
                <div key={item} className="surface-muted p-4">
                  <Badge tone="purple">AI Insight</Badge>
                  <p className="mt-3 text-sm leading-6 text-slate-200">{item}</p>
                </div>
              ))}
            </div>
          </AICard>

          <Card className="p-6">
            <SectionHeader title="Popular Roles" description="Which interview roles show up most often." />
            <div className="mt-5 flex flex-wrap gap-2">
              {mergedStats.roleStats.slice(0, 6).map((role) => (
                <Badge key={role._id} tone="blue">
                  {role._id} · {role.count}
                </Badge>
              ))}
            </div>
          </Card>

          <Card className="p-6">
            <SectionHeader title="Quick Actions" description="Start the next part of your project demo in one click." />
            <div className="mt-5 grid gap-3">
              <Link to="/companies" className="btn-secondary justify-between">
                <span>Explore Companies</span>
                <span>View</span>
              </Link>
              <Link to="/ai-insights" className="btn-secondary justify-between">
                <span>Ask StudentSphere AI</span>
                <span>Open</span>
              </Link>
              <Link to="/interviews" className="btn-secondary justify-between">
                <span>Browse Interviews</span>
                <span>Review</span>
              </Link>
              <Link to="/roadmap" className="btn-secondary justify-between">
                <span>Create Preparation Roadmap</span>
                <span>Plan</span>
              </Link>
            </div>
          </Card>
        </div>
      </div>
    </div>
  );
};

export default Dashboard;
