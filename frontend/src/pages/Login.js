import React, { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';

const Login = () => {
  const [formData, setFormData] = useState({ email: '', password: '' });
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);
  const { login } = useAuth();
  const navigate = useNavigate();

  const handleSubmit = async (event) => {
    event.preventDefault();
    setError('');
    setLoading(true);
    const result = await login(formData.email, formData.password);

    if (result.success) {
      navigate('/dashboard');
    } else {
      setError(result.error);
    }

    setLoading(false);
  };

  return (
    <div className="flex min-h-screen items-center justify-center px-4">
      <div className="surface-strong w-full max-w-md p-8">
        <p className="eyebrow">StudentSphere</p>
        <h1 className="mt-2 text-3xl font-semibold text-white">Sign in to your workspace</h1>
        <p className="mt-2 text-sm text-slate-400">
          Review interview intelligence, company patterns, and AI-driven preparation guidance.
        </p>

        <form className="mt-8 space-y-5" onSubmit={handleSubmit}>
          {error ? <div className="rounded-xl border border-rose-400/20 bg-rose-500/10 px-4 py-3 text-sm text-rose-100">{error}</div> : null}
          <div>
            <label className="label-base" htmlFor="email">Email</label>
            <input id="email" type="email" required className="input-base" value={formData.email} onChange={(event) => setFormData((current) => ({ ...current, email: event.target.value }))} />
          </div>
          <div>
            <label className="label-base" htmlFor="password">Password</label>
            <input id="password" type="password" required className="input-base" value={formData.password} onChange={(event) => setFormData((current) => ({ ...current, password: event.target.value }))} />
          </div>
          <button type="submit" className="btn-primary w-full" disabled={loading}>
            {loading ? 'Signing in...' : 'Sign in'}
          </button>
        </form>

        <p className="mt-6 text-sm text-slate-400">
          New here? <Link to="/register" className="text-blue-300">Create an account</Link>
        </p>
      </div>
    </div>
  );
};

export default Login;
