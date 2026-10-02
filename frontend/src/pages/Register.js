import React, { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';

const Register = () => {
  const [formData, setFormData] = useState({
    name: '',
    email: '',
    password: '',
    college: '',
    branch: '',
    graduationYear: '',
  });
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);
  const { register } = useAuth();
  const navigate = useNavigate();

  const handleSubmit = async (event) => {
    event.preventDefault();
    setError('');
    setLoading(true);
    const result = await register(formData);

    if (result.success) {
      navigate('/dashboard');
    } else {
      setError(result.error);
    }

    setLoading(false);
  };

  return (
    <div className="flex min-h-screen items-center justify-center px-4 py-10">
      <div className="surface-strong w-full max-w-2xl p-8">
        <p className="eyebrow">Create Account</p>
        <h1 className="mt-2 text-3xl font-semibold text-white">Join StudentSphere</h1>
        <form className="mt-8 grid gap-5 md:grid-cols-2" onSubmit={handleSubmit}>
          {error ? <div className="md:col-span-2 rounded-xl border border-rose-400/20 bg-rose-500/10 px-4 py-3 text-sm text-rose-100">{error}</div> : null}
          {['name', 'email', 'password', 'college', 'branch', 'graduationYear'].map((field) => (
            <div key={field} className={field === 'name' ? 'md:col-span-2' : ''}>
              <label className="label-base" htmlFor={field}>{field === 'graduationYear' ? 'Graduation Year' : field.charAt(0).toUpperCase() + field.slice(1)}</label>
              <input
                id={field}
                type={field === 'email' ? 'email' : field === 'password' ? 'password' : field === 'graduationYear' ? 'number' : 'text'}
                className="input-base"
                value={formData[field]}
                onChange={(event) => setFormData((current) => ({ ...current, [field]: event.target.value }))}
                required={['name', 'email', 'password'].includes(field)}
              />
            </div>
          ))}
          <div className="md:col-span-2 flex items-center justify-between">
            <p className="text-sm text-slate-400">
              Already have an account? <Link to="/login" className="text-blue-300">Sign in</Link>
            </p>
            <button type="submit" className="btn-primary" disabled={loading}>
              {loading ? 'Creating account...' : 'Create account'}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
};

export default Register;
