import React, { useState } from 'react';
import { Menu, X, Home, Database, Settings, Zap, BarChart3, CheckCircle, FileText, LogOut, User, ChevronDown } from 'lucide-react';
import { Link, useLocation } from 'react-router-dom';
import { motion, AnimatePresence } from 'framer-motion';
import { useAuth } from '../context/AuthContext';

interface MainLayoutProps {
  children: React.ReactNode;
}

const NAVIGATION = [
  { path: '/', label: 'Dashboard', icon: Home, section: 'WORKSPACE' },
  { path: '/dataset-upload', label: 'Dataset Upload', icon: Database, section: 'WORKSPACE' },
  { path: '/data-explorer', label: 'Data Explorer', icon: Database, section: 'WORKSPACE' },
  { path: '/analysis-config', label: 'Configure Analysis', icon: Settings, section: 'WORKSPACE' },
  { path: '/ai-lab', label: 'AI Lab', icon: Zap, section: 'EXPERIMENTS' },
  { path: '/run-monitor', label: 'Run Monitor', icon: BarChart3, section: 'EXPERIMENTS' },
  { path: '/verification-center', label: 'Verification', icon: CheckCircle, section: 'EXPERIMENTS' },
  { path: '/results', label: 'Results', icon: FileText, section: 'EXPERIMENTS' },
];

export default function MainLayout({ children }: MainLayoutProps) {
  const [sidebarOpen, setSidebarOpen] = useState(true);
  const [profileMenuOpen, setProfileMenuOpen] = useState(false);
  const location = useLocation();
  const { user, logout } = useAuth();

  const handleLogout = () => {
    logout();
    setProfileMenuOpen(false);
  };

  const NavLink = ({ path, label, icon: Icon }: any) => {
    const isActive = location.pathname === path;
    return (
      <Link to={path}>
        <motion.div
          className={`flex items-center gap-3 px-4 py-3 rounded-lg transition-all ${
            isActive
              ? 'bg-indigo-500/20 border border-indigo-500/30 text-indigo-300'
              : 'text-gray-400 hover:bg-gray-700/50'
          }`}
          whileHover={{ x: 4 }}
        >
          <Icon className="w-5 h-5" />
          <span className={sidebarOpen ? '' : 'hidden'}>{label}</span>
        </motion.div>
      </Link>
    );
  };

  return (
    <div className="flex h-screen bg-gray-900">
      {/* Sidebar */}
      <AnimatePresence>
        {sidebarOpen && (
          <motion.div
            initial={{ x: -280 }}
            animate={{ x: 0 }}
            exit={{ x: -280 }}
            className="w-64 bg-gradient-to-b from-gray-800 to-gray-900 border-r border-gray-700 flex flex-col p-6 space-y-6 overflow-y-auto"
          >
            {/* Logo */}
            <div className="flex items-center gap-2 mb-4">
              <div className="w-10 h-10 bg-gradient-to-br from-indigo-500 to-purple-500 rounded-lg flex items-center justify-center">
                <span className="text-white font-bold">DA</span>
              </div>
              <div>
                <div className="font-bold text-white">Arena</div>
                <div className="text-xs text-gray-400">v1.0</div>
              </div>
            </div>

            {/* User Profile in Sidebar */}
            {user && (
              <div className="bg-gray-700/50 rounded-lg p-3 border border-gray-600">
                <div className="text-sm font-semibold text-white truncate">{user.full_name || user.username}</div>
                <div className="text-xs text-gray-400 truncate">{user.email}</div>
                <div className="text-xs text-indigo-400 mt-1 font-medium">{user.role}</div>
              </div>
            )}

            {/* Navigation */}
            <nav className="space-y-6 flex-1">
              {['WORKSPACE', 'EXPERIMENTS'].map((section) => (
                <div key={section}>
                  <div className="text-xs font-semibold text-gray-400 uppercase tracking-wider px-4 mb-3">
                    {section}
                  </div>
                  <div className="space-y-2">
                    {NAVIGATION.filter((item) => item.section === section).map((item) => (
                      <NavLink key={item.path} {...item} />
                    ))}
                  </div>
                </div>
              ))}
            </nav>

            {/* Footer */}
            <div className="pt-6 border-t border-gray-700">
              <a href="#" className="text-xs text-gray-400 hover:text-white transition-colors">
                📚 Docs
              </a>
            </div>
          </motion.div>
        )}
      </AnimatePresence>

      {/* Main Content */}
      <div className="flex-1 flex flex-col overflow-hidden">
        {/* Top Bar */}
        <div className="bg-gradient-to-r from-gray-800 to-gray-900 border-b border-gray-700 px-6 py-4 flex items-center justify-between">
          <button
            onClick={() => setSidebarOpen(!sidebarOpen)}
            className="p-2 hover:bg-gray-700 rounded-lg transition-colors text-gray-300"
          >
            {sidebarOpen ? <X className="w-6 h-6" /> : <Menu className="w-6 h-6" />}
          </button>

          <div className="flex items-center gap-4">
            <div className="text-sm text-gray-300">
              🔬 <span className="font-semibold">DataScientist Arena</span>
            </div>
          </div>

          {/* User Menu */}
          <div className="relative">
            <button
              onClick={() => setProfileMenuOpen(!profileMenuOpen)}
              className="flex items-center gap-2 px-4 py-2 bg-gray-700 hover:bg-gray-600 rounded-lg transition-colors text-gray-300"
            >
              <User className="w-4 h-4" />
              {user?.username && <span className="text-sm">{user.username}</span>}
              <ChevronDown className="w-4 h-4" />
            </button>

            {/* Dropdown Menu */}
            {profileMenuOpen && (
              <motion.div
                initial={{ opacity: 0, y: -10 }}
                animate={{ opacity: 1, y: 0 }}
                exit={{ opacity: 0, y: -10 }}
                className="absolute right-0 mt-2 w-56 bg-gray-800 border border-gray-700 rounded-lg shadow-xl z-50"
              >
                <div className="p-4 border-b border-gray-700">
                  <div className="text-sm font-semibold text-white">{user?.full_name || user?.username}</div>
                  <div className="text-xs text-gray-400">{user?.email}</div>
                  <div className="text-xs text-indigo-400 mt-1">Role: {user?.role}</div>
                </div>

                <div className="p-2 space-y-1">
                  <a
                    href="#"
                    className="flex items-center gap-2 px-3 py-2 text-sm text-gray-300 hover:bg-gray-700 rounded transition-colors"
                  >
                    <User className="w-4 h-4" />
                    Profile Settings
                  </a>
                  <a
                    href="#"
                    className="flex items-center gap-2 px-3 py-2 text-sm text-gray-300 hover:bg-gray-700 rounded transition-colors"
                  >
                    <Settings className="w-4 h-4" />
                    Preferences
                  </a>
                  <a
                    href="#"
                    className="flex items-center gap-2 px-3 py-2 text-sm text-gray-300 hover:bg-gray-700 rounded transition-colors"
                  >
                    🔑 API Keys
                  </a>
                </div>

                <div className="p-2 border-t border-gray-700">
                  <button
                    onClick={handleLogout}
                    className="w-full flex items-center gap-2 px-3 py-2 text-sm text-red-400 hover:bg-red-900/20 rounded transition-colors"
                  >
                    <LogOut className="w-4 h-4" />
                    Logout
                  </button>
                </div>
              </motion.div>
            )}
          </div>
        </div>

        {/* Content Area */}
        <div className="flex-1 overflow-y-auto bg-gray-950">
          <div className="p-8">
            {children}
          </div>
        </div>
      </div>
    </div>
  );
}
