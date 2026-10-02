import React from 'react';
import { Link } from 'react-router-dom';
import Card from './Card';
import Badge from './Badge';

const companyInitial = (name = '') => name.slice(0, 2).toUpperCase();

const CompanyCard = ({ company }) => {
  return (
    <Link to={`/companies/${company._id}`} className="block">
      <Card className="h-full p-5 transition hover:-translate-y-0.5 hover:border-blue-400/30 hover:bg-slate-900/95">
        <div className="flex items-start gap-4">
          <div className="flex h-12 w-12 items-center justify-center rounded-2xl border border-blue-400/20 bg-blue-500/15 text-sm font-semibold text-blue-100">
            {companyInitial(company.name)}
          </div>
          <div className="min-w-0 flex-1">
            <div className="flex items-start justify-between gap-3">
              <div>
                <h3 className="text-lg font-semibold text-white">{company.name}</h3>
                <p className="mt-1 text-sm text-slate-400">{company.industry}</p>
              </div>
              <Badge tone="purple">{company.interviewCount} interviews</Badge>
            </div>

            {company.popularTopics?.length ? (
              <div className="mt-4">
                <p className="text-xs uppercase tracking-[0.16em] text-slate-500">Top Topics</p>
                <div className="mt-2 flex flex-wrap gap-2">
                  {company.popularTopics.slice(0, 3).map((topic) => (
                    <Badge key={topic} tone="blue">
                      {topic}
                    </Badge>
                  ))}
                </div>
              </div>
            ) : null}

            <div className="mt-4 flex items-center justify-between text-sm">
              <span className="text-slate-300">{company.difficultyLabel || 'Balanced difficulty'}</span>
              <span className="font-medium text-blue-300">View Intelligence</span>
            </div>
          </div>
        </div>
      </Card>
    </Link>
  );
};

export default CompanyCard;
