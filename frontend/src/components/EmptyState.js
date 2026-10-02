import React from 'react';
import { Link } from 'react-router-dom';
import Card from './Card';

const EmptyState = ({ icon, title, description, actionText, onAction, to }) => {
  return (
    <Card className="p-10 text-center">
      <div className="mx-auto flex h-14 w-14 items-center justify-center rounded-2xl border border-slate-700 bg-slate-900/70 text-slate-300">
        {icon || <span className="text-lg">+</span>}
      </div>
      <h3 className="mt-5 text-xl font-semibold text-white">{title}</h3>
      <p className="mx-auto mt-3 max-w-xl text-sm leading-6 text-slate-400">{description}</p>
      {actionText ? (
        <div className="mt-6">
          {to ? (
            <Link to={to} className="btn-primary">
              {actionText}
            </Link>
          ) : (
            <button onClick={onAction} className="btn-primary">
              {actionText}
            </button>
          )}
        </div>
      ) : null}
    </Card>
  );
};

export default EmptyState;
