import React, { useEffect, useMemo, useState } from 'react';
import api from '../lib/api';
import { demoCompanies } from '../data/demoData';
import PageHeader from '../components/PageHeader';
import SearchBar from '../components/SearchBar';
import Card from '../components/Card';
import CompanyCard from '../components/CompanyCard';

const Companies = () => {
  const [companies, setCompanies] = useState([]);
  const [searchTerm, setSearchTerm] = useState('');
  const [industry, setIndustry] = useState('');
  const [difficulty, setDifficulty] = useState('');

  useEffect(() => {
    const loadCompanies = async () => {
      try {
        const response = await api.get('/companies');
        setCompanies(response.data || []);
      } catch (error) {
        console.error('Falling back to demo companies.', error);
        setCompanies([]);
      }
    };

    loadCompanies();
  }, []);

  const baseCompanies = companies.length
    ? companies.map((company) => ({
        ...company,
        difficultyLabel: company.difficultyLabel || 'Balanced',
      }))
    : demoCompanies;

  const filteredCompanies = useMemo(() => {
    return baseCompanies.filter((company) => {
      const matchesSearch = company.name.toLowerCase().includes(searchTerm.toLowerCase());
      const matchesIndustry = industry ? company.industry === industry : true;
      const matchesDifficulty = difficulty ? company.difficultyLabel?.includes(difficulty) : true;
      return matchesSearch && matchesIndustry && matchesDifficulty;
    });
  }, [baseCompanies, searchTerm, industry, difficulty]);

  const industries = [...new Set(baseCompanies.map((company) => company.industry))];

  return (
    <div className="space-y-8">
      <PageHeader
        eyebrow="Companies"
        title="Company Intelligence"
        subtitle="Explore interview patterns, topics, and question trends across companies."
      />

      <Card className="p-5">
        <div className="grid gap-4 lg:grid-cols-[minmax(0,1.4fr)_repeat(2,minmax(180px,1fr))]">
          <SearchBar value={searchTerm} onChange={(event) => setSearchTerm(event.target.value)} placeholder="Search companies..." />
          <select value={industry} onChange={(event) => setIndustry(event.target.value)} className="input-base">
            <option value="">All industries</option>
            {industries.map((item) => (
              <option key={item} value={item}>
                {item}
              </option>
            ))}
          </select>
          <select value={difficulty} onChange={(event) => setDifficulty(event.target.value)} className="input-base">
            <option value="">All difficulty bands</option>
            <option value="Easy">Easy</option>
            <option value="Medium">Medium</option>
            <option value="Hard">Hard</option>
          </select>
        </div>
      </Card>

      <div className="grid gap-4 md:grid-cols-2 xl:grid-cols-3">
        {filteredCompanies.map((company) => (
          <CompanyCard key={company._id} company={company} />
        ))}
      </div>
    </div>
  );
};

export default Companies;
