import React from 'react';

const styles = {
  neutral: 'border-slate-700/80 bg-slate-900/70 text-slate-200',
  blue: 'border-blue-400/20 bg-blue-500/15 text-blue-100',
  green: 'border-emerald-400/20 bg-emerald-500/15 text-emerald-100',
  amber: 'border-amber-400/20 bg-amber-500/15 text-amber-100',
  purple: 'border-violet-400/20 bg-violet-500/15 text-violet-100',
  red: 'border-rose-400/20 bg-rose-500/15 text-rose-100',
};

const Badge = ({ children, tone = 'neutral' }) => {
  return <span className={`badge-base ${styles[tone] || styles.neutral}`}>{children}</span>;
};

export default Badge;
