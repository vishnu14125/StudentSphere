import React from 'react';
import { Link } from 'react-router-dom';
import Card from './Card';
import Badge from './Badge';

const difficultyTone = {
  Easy: 'green',
  Medium: 'amber',
  Hard: 'red',
};

const InterviewCard = ({ interview }) => {
  return (
    <Link to={`/interviews/${interview._id}`} className="block">
      <Card className="h-full p-5 transition hover:-translate-y-0.5 hover:border-blue-400/30 hover:bg-slate-900/95">
        <div className="flex items-start justify-between gap-4">
          <div>
            <p className="text-sm font-medium text-blue-200">{interview.company?.name || 'Company'}</p>
            <h3 className="mt-1 text-lg font-semibold text-white">{interview.experienceTitle}</h3>
            <p className="mt-2 text-sm text-slate-300">
              {interview.role} · {interview.year}
            </p>
          </div>
          <Badge tone={difficultyTone[interview.difficulty] || 'neutral'}>{interview.difficulty}</Badge>
        </div>

        {interview.topics?.length ? (
          <div className="mt-4 flex flex-wrap gap-2">
            {interview.topics.slice(0, 4).map((topic) => (
              <Badge key={topic} tone="blue">
                {topic}
              </Badge>
            ))}
          </div>
        ) : null}

        {interview.aiSummary ? (
          <p className="mt-4 text-sm leading-6 text-slate-300">{interview.aiSummary}</p>
        ) : null}

        <div className="mt-5 flex items-center justify-between text-sm">
          <span className="text-slate-500">AI-ready interview detail</span>
          <span className="font-medium text-blue-300">View Experience</span>
        </div>
      </Card>
    </Link>
  );
};

export default InterviewCard;
