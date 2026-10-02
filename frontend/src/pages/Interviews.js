import React, { useEffect, useMemo, useState } from 'react';
import api from '../lib/api';
import { demoCompanies, demoInterviews } from '../data/demoData';
import PageHeader from '../components/PageHeader';
import Card from '../components/Card';
import SearchBar from '../components/SearchBar';
import InterviewCard from '../components/InterviewCard';
import EmptyState from '../components/EmptyState';

const Interviews = () => {
  const [interviews, setInterviews] = useState([]);
  const [companies, setCompanies] = useState([]);
  const [filters, setFilters] = useState({
    search: '',
    company: '',
    role: '',
    difficulty: '',
    year: '',
  });

  useEffect(() => {
    const loadData = async () => {
      try {
        const [companiesResponse, interviewsResponse] = await Promise.all([
          api.get('/companies'),
          api.get('/interviews', { params: { limit: 24 } }),
        ]);

        setCompanies(companiesResponse.data || []);
        setInterviews(interviewsResponse.data?.interviews || []);
      } catch (error) {
        console.error('Falling back to demo interview list.', error);
        setCompanies([]);
        setInterviews([]);
      }
    };

    loadData();
  }, []);

  const companyOptions = companies.length ? companies : demoCompanies;
  const sourceInterviews = interviews.length ? interviews : demoInterviews;

  const filteredInterviews = useMemo(() => {
    return sourceInterviews.filter((item) => {
      const haystack = `${item.experienceTitle} ${item.company?.name || ''} ${item.role} ${item.aiSummary || ''}`.toLowerCase();
      const matchesSearch = haystack.includes(filters.search.toLowerCase());
      const matchesCompany = filters.company ? (item.company?.name || item.company) === filters.company : true;
      const matchesRole = filters.role ? item.role.toLowerCase().includes(filters.role.toLowerCase()) : true;
      const matchesDifficulty = filters.difficulty ? item.difficulty === filters.difficulty : true;
      const matchesYear = filters.year ? String(item.year) === filters.year : true;
      return matchesSearch && matchesCompany && matchesRole && matchesDifficulty && matchesYear;
    });
  }, [sourceInterviews, filters]);

  return (
    <div className="space-y-8">
      <PageHeader
        eyebrow="Interview Experiences"
        title="Interview Experience Library"
        subtitle="Search and review interview stories with AI summaries, extracted topics, and company context."
      />

      <Card className="p-5">
        <div className="grid gap-4 lg:grid-cols-5">
          <SearchBar
            value={filters.search}
            onChange={(event) => setFilters((current) => ({ ...current, search: event.target.value }))}
            placeholder="Search experiences..."
          />
          <select className="input-base" value={filters.company} onChange={(event) => setFilters((current) => ({ ...current, company: event.target.value }))}>
            <option value="">All companies</option>
            {companyOptions.map((company) => (
              <option key={company._id} value={company.name}>
                {company.name}
              </option>
            ))}
          </select>
          <input className="input-base" placeholder="Role" value={filters.role} onChange={(event) => setFilters((current) => ({ ...current, role: event.target.value }))} />
          <select className="input-base" value={filters.difficulty} onChange={(event) => setFilters((current) => ({ ...current, difficulty: event.target.value }))}>
            <option value="">All difficulties</option>
            <option value="Easy">Easy</option>
            <option value="Medium">Medium</option>
            <option value="Hard">Hard</option>
          </select>
          <select className="input-base" value={filters.year} onChange={(event) => setFilters((current) => ({ ...current, year: event.target.value }))}>
            <option value="">All years</option>
            {[2026, 2025, 2024, 2023, 2022].map((year) => (
              <option key={year} value={year}>
                {year}
              </option>
            ))}
          </select>
        </div>
      </Card>

      {filteredInterviews.length ? (
        <div className="grid gap-4 xl:grid-cols-2">
          {filteredInterviews.map((interview) => (
            <InterviewCard key={interview._id} interview={interview} />
          ))}
        </div>
      ) : (
        <EmptyState
          title="No interview experiences yet"
          description="Explore our demo interview dataset to keep the milestone flow full and professional."
          actionText="Load Demo Data"
          onAction={() => setInterviews(demoInterviews)}
        />
      )}
    </div>
  );
};

export default Interviews;
