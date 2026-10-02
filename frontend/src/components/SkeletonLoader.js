import React from 'react';

const variants = {
  card: (
    <div className="surface animate-pulse p-5">
      <div className="h-4 w-1/3 rounded bg-slate-800" />
      <div className="mt-4 h-7 w-2/3 rounded bg-slate-800" />
      <div className="mt-4 h-4 w-full rounded bg-slate-900" />
      <div className="mt-2 h-4 w-5/6 rounded bg-slate-900" />
    </div>
  ),
  stat: (
    <div className="surface animate-pulse p-5">
      <div className="flex items-center justify-between">
        <div className="space-y-3">
          <div className="h-3 w-24 rounded bg-slate-800" />
          <div className="h-8 w-20 rounded bg-slate-800" />
        </div>
        <div className="h-11 w-11 rounded-2xl bg-slate-800" />
      </div>
    </div>
  ),
};

const SkeletonLoader = ({ type = 'card', count = 1, className = '' }) => {
  return (
    <div className={className}>
      <div className="grid gap-4 md:grid-cols-2 xl:grid-cols-4">
        {Array.from({ length: count }).map((_, index) => (
          <div key={index}>{variants[type] || variants.card}</div>
        ))}
      </div>
    </div>
  );
};

export default SkeletonLoader;
