import React from 'react';
import Card from './Card';

const accentMap = {
  blue: 'from-blue-500/20 to-blue-500/5 border-blue-400/20',
  green: 'from-emerald-500/20 to-emerald-500/5 border-emerald-400/20',
  amber: 'from-amber-500/20 to-amber-500/5 border-amber-400/20',
  purple: 'from-violet-500/20 to-violet-500/5 border-violet-400/20',
};

const StatCard = ({ title, value, icon, color = 'blue', helper }) => {
  return (
    <Card className={`overflow-hidden border bg-gradient-to-br p-5 ${accentMap[color] || accentMap.blue}`}>
      <div className="flex items-start justify-between gap-4">
        <div>
          <p className="metric-kicker">{title}</p>
          <p className="mt-3 text-3xl font-semibold tracking-tight text-white">{value}</p>
          {helper ? <p className="mt-2 text-sm text-slate-300">{helper}</p> : null}
        </div>
        <div className="flex h-11 w-11 items-center justify-center rounded-2xl border border-white/10 bg-slate-950/40 text-blue-100">
          {icon}
        </div>
      </div>
    </Card>
  );
};

export default StatCard;
