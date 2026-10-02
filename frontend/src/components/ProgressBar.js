import React from 'react';

const toneStyles = {
  blue: 'bg-blue-500',
  green: 'bg-emerald-500',
  amber: 'bg-amber-500',
  purple: 'bg-violet-500',
  red: 'bg-rose-500',
};

const ProgressBar = ({ label, value, tone = 'blue', hint }) => {
  return (
    <div className="space-y-2">
      <div className="flex items-center justify-between gap-3 text-sm">
        <span className="font-medium text-slate-100">{label}</span>
        <span className="text-slate-400">{hint || `${value}%`}</span>
      </div>
      <div className="h-2.5 overflow-hidden rounded-full bg-slate-800">
        <div
          className={`h-full rounded-full ${toneStyles[tone] || toneStyles.blue}`}
          style={{ width: `${Math.max(0, Math.min(100, value))}%` }}
        />
      </div>
    </div>
  );
};

export default ProgressBar;
