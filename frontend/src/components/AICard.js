import React from 'react';
import Card from './Card';
import Badge from './Badge';

const AICard = ({ children, title, icon, loading = false, subtitle }) => {
  return (
    <Card strong className="overflow-hidden p-6">
      <div className="flex items-start justify-between gap-4">
        <div className="flex items-start gap-3">
          <div className="flex h-11 w-11 items-center justify-center rounded-2xl border border-violet-400/20 bg-violet-500/15 text-violet-100">
            {icon || <span className="text-lg">AI</span>}
          </div>
          <div>
            <div className="flex flex-wrap items-center gap-2">
              <h3 className="text-lg font-semibold text-white">{title}</h3>
              <Badge tone="purple">AI Insight</Badge>
            </div>
            {subtitle ? <p className="mt-1 text-sm text-slate-300">{subtitle}</p> : null}
          </div>
        </div>
      </div>
      {loading ? (
        <div className="mt-5 animate-pulse space-y-3">
          <div className="h-4 w-5/6 rounded bg-violet-300/20" />
          <div className="h-4 w-2/3 rounded bg-violet-300/20" />
          <div className="h-4 w-4/5 rounded bg-violet-300/20" />
        </div>
      ) : (
        <div className="mt-5 text-slate-100">{children}</div>
      )}
    </Card>
  );
};

export default AICard;
