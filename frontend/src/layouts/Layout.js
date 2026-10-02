import React, { useMemo, useState } from 'react';
import { Link, Outlet, useLocation } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import Badge from '../components/Badge';

const navigation = [
  { name: 'Dashboard', href: '/dashboard' },
  { name: 'Companies', href: '/companies' },
  { name: 'Interviews', href: '/interviews' },
  { name: 'AI Insights', href: '/ai-insights' },
  { name: 'Analytics', href: '/analytics' },
  { name: 'Roadmap', href: '/roadmap' },
];

const Layout = () => {
  const { user, logout } = useAuth();
  const location = useLocation();
  const [open, setOpen] = useState(false);

  const activeLabel = useMemo(() => {
    return navigation.find((item) => location.pathname.startsWith(item.href))?.name || 'Dashboard';
  }, [location.pathname]);

  const isActive = (href) => location.pathname.startsWith(href);

  return (
    <div className="app-shell">
      <header className="sticky top-0 z-30 border-b border-slate-800/80 bg-slate-950/80 backdrop-blur-xl">
        <div className="app-container flex h-16 items-center justify-between gap-4">
          <div className="flex items-center gap-4">
            <button
              type="button"
              className="btn-ghost md:hidden"
              onClick={() => setOpen((value) => !value)}
              aria-label="Toggle navigation"
            >
              Menu
            </button>
            <Link to="/dashboard" className="flex items-center gap-3">
              <div className="flex h-10 w-10 items-center justify-center rounded-2xl border border-blue-400/20 bg-blue-500/15 text-sm font-semibold text-blue-100">
                SS
              </div>
              <div>
                <p className="text-base font-semibold text-white">StudentSphere</p>
                <p className="text-xs text-slate-400">Placement Intelligence Platform</p>
              </div>
            </Link>
          </div>

          <nav className="hidden items-center gap-1 md:flex">
            {navigation.map((item) => (
              <Link
                key={item.href}
                to={item.href}
                className={`rounded-xl px-3 py-2 text-sm font-medium transition ${
                  isActive(item.href)
                    ? 'bg-blue-500/15 text-blue-100'
                    : 'text-slate-300 hover:bg-slate-900/70 hover:text-white'
                }`}
              >
                {item.name}
              </Link>
            ))}
          </nav>

          <div className="flex items-center gap-3">
            <Link to="/submit-interview" className="btn-primary hidden sm:inline-flex">
              Submit Experience
            </Link>
            <div className="hidden items-center gap-3 rounded-2xl border border-slate-800 bg-slate-900/70 px-3 py-2 sm:flex">
              <div className="text-right">
                <p className="text-sm font-medium text-white">{user?.name || 'Student'}</p>
                <p className="text-xs text-slate-400">Profile</p>
              </div>
              <Badge tone="green">{activeLabel}</Badge>
            </div>
            <button onClick={logout} className="btn-secondary">
              Logout
            </button>
          </div>
        </div>

        {open ? (
          <div className="app-container pb-4 md:hidden">
            <div className="surface p-2">
              {navigation.map((item) => (
                <Link
                  key={item.href}
                  to={item.href}
                  onClick={() => setOpen(false)}
                  className={`block rounded-xl px-3 py-2 text-sm ${
                    isActive(item.href) ? 'bg-blue-500/15 text-blue-100' : 'text-slate-300'
                  }`}
                >
                  {item.name}
                </Link>
              ))}
            </div>
          </div>
        ) : null}
      </header>

      <main className="app-container py-8">
        <Outlet />
      </main>
    </div>
  );
};

export default Layout;
