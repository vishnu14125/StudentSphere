import React, { useEffect, useState } from 'react';
import { useAuth } from '../context/AuthContext';
import api from '../lib/api';
import PageHeader from '../components/PageHeader';
import Card from '../components/Card';

const Profile = () => {
  const { user, fetchProfile } = useAuth();
  const [formData, setFormData] = useState({
    name: '',
    college: '',
    branch: '',
    graduationYear: '',
    skills: '',
    targetRoles: '',
  });
  const [message, setMessage] = useState('');

  useEffect(() => {
    if (!user) return;
    setFormData({
      name: user.name || '',
      college: user.college || '',
      branch: user.branch || '',
      graduationYear: user.graduationYear || '',
      skills: (user.skills || []).join(', '),
      targetRoles: (user.targetRoles || []).join(', '),
    });
  }, [user]);

  const handleSubmit = async (event) => {
    event.preventDefault();
    await api.put('/auth/profile', {
      ...formData,
      graduationYear: formData.graduationYear ? Number(formData.graduationYear) : undefined,
      skills: formData.skills.split(',').map((item) => item.trim()).filter(Boolean),
      targetRoles: formData.targetRoles.split(',').map((item) => item.trim()).filter(Boolean),
    });
    await fetchProfile();
    setMessage('Profile updated successfully.');
  };

  return (
    <div className="space-y-8">
      <PageHeader eyebrow="Profile" title="Your Preparation Profile" subtitle="Keep your background, focus roles, and target skill areas aligned with the demo flow." />
      <Card className="mx-auto max-w-4xl p-6">
        <form className="grid gap-5 md:grid-cols-2" onSubmit={handleSubmit}>
          {message ? <div className="md:col-span-2 rounded-xl border border-emerald-400/20 bg-emerald-500/10 px-4 py-3 text-sm text-emerald-100">{message}</div> : null}
          <div className="md:col-span-2">
            <label className="label-base">Email</label>
            <input className="input-base" value={user?.email || ''} disabled />
          </div>
          {['name', 'college', 'branch', 'graduationYear', 'skills', 'targetRoles'].map((field) => (
            <div key={field} className={['skills', 'targetRoles'].includes(field) ? 'md:col-span-2' : ''}>
              <label className="label-base">{field === 'graduationYear' ? 'Graduation Year' : field === 'targetRoles' ? 'Target Roles' : field.charAt(0).toUpperCase() + field.slice(1)}</label>
              <input className="input-base" value={formData[field]} onChange={(event) => setFormData((current) => ({ ...current, [field]: event.target.value }))} />
            </div>
          ))}
          <div className="md:col-span-2 flex justify-end">
            <button className="btn-primary" type="submit">Update Profile</button>
          </div>
        </form>
      </Card>
    </div>
  );
};

export default Profile;
