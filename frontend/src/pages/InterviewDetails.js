import React, { useEffect, useMemo, useState } from 'react';
import { Link, useNavigate, useParams } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import api from '../lib/api';
import { demoInterviews } from '../data/demoData';
import Card from '../components/Card';
import Badge from '../components/Badge';
import AICard from '../components/AICard';

const InterviewDetails = () => {
  const { id } = useParams();
  const { user } = useAuth();
  const navigate = useNavigate();
  const [interview, setInterview] = useState(null);

  useEffect(() => {
    const loadInterview = async () => {
      try {
        const response = await api.get(`/interviews/${id}`);
        setInterview(response.data);
      } catch (error) {
        console.error('Falling back to demo interview detail.', error);
        setInterview(demoInterviews.find((item) => item._id === id) || demoInterviews[0]);
      }
    };

    loadInterview();
  }, [id]);

  const activeInterview = interview || demoInterviews[0];
  const isOwner = useMemo(() => {
    if (!user || !activeInterview?.user?._id) {
      return false;
    }
    return user._id === activeInterview.user._id;
  }, [user, activeInterview]);

  const handleDelete = async () => {
    if (!window.confirm('Delete this interview experience?')) {
      return;
    }

    try {
      await api.delete(`/interviews/${id}`);
      navigate('/interviews');
    } catch (error) {
      console.error('Delete failed.', error);
    }
  };

  return (
    <div className="space-y-8">
      <div className="flex flex-wrap items-start justify-between gap-4">
        <div>
          <Link to="/interviews" className="text-sm text-blue-300">
            Back to Interviews
          </Link>
          <h1 className="mt-3 text-3xl font-semibold text-white">{activeInterview.company?.name} {activeInterview.role} Interview Experience</h1>
          <div className="mt-3 flex flex-wrap items-center gap-2 text-sm text-slate-400">
            <span>{activeInterview.year}</span>
            <span>·</span>
            <Badge tone={activeInterview.difficulty === 'Hard' ? 'red' : activeInterview.difficulty === 'Medium' ? 'amber' : 'green'}>
              {activeInterview.difficulty}
            </Badge>
          </div>
        </div>
        {isOwner ? (
          <div className="flex gap-3">
            <button className="btn-secondary" onClick={handleDelete}>
              Delete
            </button>
          </div>
        ) : null}
      </div>

      <div className="grid gap-6 xl:grid-cols-[minmax(0,1.45fr)_minmax(320px,0.95fr)]">
        <div className="space-y-6">
          <Card className="p-6">
            <p className="eyebrow">Original Experience</p>
            <div className="mt-4 whitespace-pre-wrap text-sm leading-7 text-slate-200">{activeInterview.experienceText}</div>
          </Card>

          {activeInterview.interviewRounds?.length ? (
            <Card className="p-6">
              <h2 className="section-title">Interview Pattern</h2>
              <div className="mt-5 space-y-3">
                {activeInterview.interviewRounds.map((round, index) => (
                  <div key={round} className="surface-muted p-4 text-sm text-slate-100">
                    <span className="text-slate-500">{index + 1}.</span> {round}
                  </div>
                ))}
              </div>
            </Card>
          ) : null}
        </div>

        <div className="space-y-6">
          <AICard title="AI Summary" subtitle="Clearly separated from the original candidate text.">
            <p className="text-sm leading-6 text-slate-100">{activeInterview.aiSummary}</p>
          </AICard>

          <Card className="p-6">
            <h2 className="section-title">Key Topics</h2>
            <div className="mt-5 flex flex-wrap gap-2">
              {(activeInterview.aiExtractedTopics?.length ? activeInterview.aiExtractedTopics : activeInterview.topics || []).map((topic) => (
                <Badge key={topic} tone="blue">
                  {topic}
                </Badge>
              ))}
            </div>
          </Card>

          <Card className="p-6">
            <h2 className="section-title">Frequent Questions</h2>
            <div className="mt-5 space-y-3">
              {(activeInterview.aiExtractedQuestions?.length ? activeInterview.aiExtractedQuestions : activeInterview.questions || []).map((question) => (
                <div key={question} className="surface-muted p-4 text-sm text-slate-100">
                  {question}
                </div>
              ))}
            </div>
          </Card>

          <AICard title="AI Insights" subtitle="Generated takeaways for preparation planning.">
            <ul className="space-y-2 text-sm text-slate-100">
              <li>Strong DSA emphasis across technical rounds.</li>
              <li>Multiple follow-up questions reward structured explanation.</li>
              <li>Core CS fundamentals appear alongside coding problems.</li>
            </ul>
          </AICard>
        </div>
      </div>
    </div>
  );
};

export default InterviewDetails;
