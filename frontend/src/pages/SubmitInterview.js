import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import api from '../lib/api';
import PageHeader from '../components/PageHeader';
import Card from '../components/Card';
import { demoCompanies } from '../data/demoData';

const SubmitInterview = () => {
  const navigate = useNavigate();
  const [companies, setCompanies] = useState([]);
  const [error, setError] = useState('');
  const [submitting, setSubmitting] = useState(false);
  const [formData, setFormData] = useState({
    company: '',
    role: '',
    experienceTitle: '',
    experienceText: '',
    interviewRounds: '',
    difficulty: 'Medium',
    year: new Date().getFullYear(),
    topics: '',
    questions: '',
    source: 'StudentSphere user submission',
  });

  useEffect(() => {
    const loadCompanies = async () => {
      try {
        const response = await api.get('/companies');
        setCompanies(response.data || []);
      } catch (error) {
        console.error('Using demo companies for submit form.', error);
        setCompanies([]);
      }
    };

    loadCompanies();
  }, []);

  const companyOptions = companies.length ? companies : demoCompanies;

  const handleSubmit = async (event) => {
    event.preventDefault();
    setSubmitting(true); setError('');
    try {
      await api.post('/interviews', {
        ...formData,
        year: Number(formData.year),
        interviewRounds: formData.interviewRounds.split('\n').map((item) => item.trim()).filter(Boolean),
        topics: formData.topics.split(',').map((item) => item.trim()).filter(Boolean),
        questions: formData.questions.split('\n').map((item) => item.trim()).filter(Boolean),
      });
      navigate('/interviews');
    } catch (requestError) { setError(requestError.response?.data?.message || 'Unable to submit the interview experience.'); }
    finally { setSubmitting(false); }
  };

  return (
    <div className="space-y-8">
      <PageHeader eyebrow="Submit Experience" title="Add Interview Experience" subtitle="Capture original candidate experience and let StudentSphere layer AI insights on top." />
      <Card className="mx-auto max-w-4xl p-6">
        <form className="grid gap-5 md:grid-cols-2" onSubmit={handleSubmit}>
          <div>
            <label className="label-base">Company</label>
            <select className="input-base" value={formData.company} onChange={(event) => setFormData((current) => ({ ...current, company: event.target.value }))} required>
              <option value="">Select company</option>
              {companyOptions.map((company) => (
                <option key={company._id} value={company.name}>
                  {company.name}
                </option>
              ))}
            </select>
          </div>
          <div>
            <label className="label-base">Role</label>
            <input className="input-base" value={formData.role} onChange={(event) => setFormData((current) => ({ ...current, role: event.target.value }))} required />
          </div>
          <div className="md:col-span-2">
            <label className="label-base">Experience Title</label>
            <input className="input-base" value={formData.experienceTitle} onChange={(event) => setFormData((current) => ({ ...current, experienceTitle: event.target.value }))} required />
          </div>
          <div className="md:col-span-2">
            <label className="label-base">Original Experience</label>
            <textarea className="input-base min-h-[220px]" value={formData.experienceText} onChange={(event) => setFormData((current) => ({ ...current, experienceText: event.target.value }))} required />
          </div>
          <div className="md:col-span-2">
            <label className="label-base">Interview Rounds</label>
            <textarea className="input-base min-h-[120px]" value={formData.interviewRounds} onChange={(event) => setFormData((current) => ({ ...current, interviewRounds: event.target.value }))} />
          </div>
          <div>
            <label className="label-base">Difficulty</label>
            <select className="input-base" value={formData.difficulty} onChange={(event) => setFormData((current) => ({ ...current, difficulty: event.target.value }))}>
              <option value="Easy">Easy</option>
              <option value="Medium">Medium</option>
              <option value="Hard">Hard</option>
            </select>
          </div>
          <div>
            <label className="label-base">Year</label>
            <input className="input-base" type="number" value={formData.year} onChange={(event) => setFormData((current) => ({ ...current, year: event.target.value }))} />
          </div>
          <div className="md:col-span-2">
            <label className="label-base">Topics</label>
            <input className="input-base" value={formData.topics} onChange={(event) => setFormData((current) => ({ ...current, topics: event.target.value }))} placeholder="Arrays, Trees, DBMS" />
          </div>
          <div className="md:col-span-2">
            <label className="label-base">Questions</label>
            <textarea className="input-base min-h-[120px]" value={formData.questions} onChange={(event) => setFormData((current) => ({ ...current, questions: event.target.value }))} />
          </div>
          <div className="md:col-span-2">`n            <label className="label-base">Source / attribution</label>`n            <input className="input-base" value={formData.source} onChange={(event) => setFormData((current) => ({ ...current, source: event.target.value }))} placeholder="Original candidate submission or permitted source" />`n          </div>`n          {error ? <p className="md:col-span-2 text-sm text-rose-300">{error}</p> : null}`n          <div className="md:col-span-2 flex justify-end gap-3">
            <button type="button" className="btn-secondary" onClick={() => navigate('/interviews')}>Cancel</button>
            <button type="submit" className="btn-primary" disabled={submitting}>{submitting ? 'Submitting...' : 'Submit Experience'}</button>
          </div>
        </form>
      </Card>
    </div>
  );
};

export default SubmitInterview;

