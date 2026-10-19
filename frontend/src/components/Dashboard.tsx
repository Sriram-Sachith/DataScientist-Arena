import React, { useEffect, useState } from 'react';
import { motion } from 'framer-motion';
import { useNavigate } from 'react-router-dom';
import { apiClient } from '../api/client';
import { useApp } from '../context/AppContext';

export const Dashboard: React.FC = () => {
  const navigate = useNavigate();
  const { datasets, experiments, setLoading, loading } = useApp();
  const [stats, setStats] = useState({
    totalDatasets: 0,
    totalExperiments: 0,
    completedRuns: 0,
    accuracyImprovement: 0,
  });

  useEffect(() => {
    loadDashboardData();
  }, []);

  const loadDashboardData = async () => {
    setLoading(true);
    try {
      const datasetsResult = await apiClient.getDatasets();
      if (datasetsResult.data) {
        setStats((prev) => ({
          ...prev,
          totalDatasets: datasetsResult.data.length,
        }));
      }
    } catch (error) {
      console.error('Failed to load dashboard data:', error);
    } finally {
      setLoading(false);
    }
  };

  const containerVariants = {
    hidden: { opacity: 0 },
    visible: {
      opacity: 1,
      transition: {
        staggerChildren: 0.1,
        delayChildren: 0.2,
      },
    },
  };

  const itemVariants = {
    hidden: { opacity: 0, y: 20 },
    visible: { opacity: 1, y: 0, transition: { duration: 0.5 } },
  };

  const statCards = [
    {
      title: 'Total Datasets',
      value: datasets.length,
      icon: '📊',
      color: 'from-blue-600 to-blue-400',
    },
    {
      title: 'Experiments',
      value: experiments.length,
      icon: '🔬',
      color: 'from-purple-600 to-purple-400',
    },
    {
      title: 'Completed Runs',
      value: stats.completedRuns,
      icon: '✅',
      color: 'from-green-600 to-green-400',
    },
    {
      title: 'Avg. Improvement',
      value: `${stats.accuracyImprovement}%`,
      icon: '📈',
      color: 'from-orange-600 to-orange-400',
    },
  ];

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-950 via-gray-900 to-gray-950 p-8">
      {/* Header */}
      <motion.div
        initial={{ opacity: 0, y: -20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5 }}
        className="mb-12"
      >
        <h1 className="text-4xl font-bold text-white mb-2">
          DataScientist Arena
        </h1>
        <p className="text-gray-400 text-lg">
          Testing AI Reliability in Data Science Workflows
        </p>
      </motion.div>

      {/* Research Question Section */}
      <motion.div
        variants={containerVariants}
        initial="hidden"
        animate="visible"
        className="bg-gradient-to-r from-indigo-900/40 to-purple-900/40 border border-indigo-500/30 rounded-xl p-8 mb-12 backdrop-blur-sm"
      >
        <motion.div variants={itemVariants} className="mb-4">
          <h2 className="text-2xl font-bold text-transparent bg-clip-text bg-gradient-to-r from-indigo-400 to-purple-400 mb-4">
            Core Research Question
          </h2>
          <p className="text-gray-300 text-lg leading-relaxed">
            Does independent verification substantially reduce errors in
            AI-generated data science workflows?
          </p>
        </motion.div>

        <motion.div variants={itemVariants} className="grid grid-cols-1 md:grid-cols-3 gap-6 mt-8">
          <div className="bg-indigo-500/10 border border-indigo-500/30 rounded-lg p-4">
            <h3 className="font-semibold text-indigo-400 mb-2">Approach 1</h3>
            <p className="text-gray-300 text-sm">
              AI Baseline: Standard AI analysis without verification
            </p>
          </div>
          <div className="bg-purple-500/10 border border-purple-500/30 rounded-lg p-4">
            <h3 className="font-semibold text-purple-400 mb-2">Approach 2</h3>
            <p className="text-gray-300 text-sm">
              Independent Verification: Second AI system validates results
            </p>
          </div>
          <div className="bg-pink-500/10 border border-pink-500/30 rounded-lg p-4">
            <h3 className="font-semibold text-pink-400 mb-2">Approach 3</h3>
            <p className="text-gray-300 text-sm">
              Manual Review: Expert human verification of analysis
            </p>
          </div>
        </motion.div>
      </motion.div>

      {/* Stats Grid */}
      <motion.div
        variants={containerVariants}
        initial="hidden"
        animate="visible"
        className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-12"
      >
        {statCards.map((card) => (
          <motion.div
            key={card.title}
            variants={itemVariants}
            className={`bg-gradient-to-br ${card.color} rounded-xl p-6 text-white shadow-lg hover:shadow-xl transition-shadow`}
          >
            <div className="text-3xl mb-2">{card.icon}</div>
            <p className="text-sm opacity-90 mb-1">{card.title}</p>
            <p className="text-3xl font-bold">{card.value}</p>
          </motion.div>
        ))}
      </motion.div>

      {/* Action Buttons */}
      <motion.div
        variants={containerVariants}
        initial="hidden"
        animate="visible"
        className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-12"
      >
        <motion.button
          variants={itemVariants}
          onClick={() => navigate('/dataset-upload')}
          className="bg-gradient-to-r from-indigo-600 to-indigo-500 hover:from-indigo-700 hover:to-indigo-600 text-white font-semibold py-4 px-8 rounded-xl transition-all transform hover:scale-105 shadow-lg"
        >
          📤 Upload Dataset
        </motion.button>
        <motion.button
          variants={itemVariants}
          onClick={() => navigate('/ai-lab')}
          className="bg-gradient-to-r from-purple-600 to-purple-500 hover:from-purple-700 hover:to-purple-600 text-white font-semibold py-4 px-8 rounded-xl transition-all transform hover:scale-105 shadow-lg"
        >
          🧪 Start Experiment
        </motion.button>
        <motion.button
          variants={itemVariants}
          onClick={() => navigate('/verification-center')}
          className="bg-gradient-to-r from-pink-600 to-pink-500 hover:from-pink-700 hover:to-pink-600 text-white font-semibold py-4 px-8 rounded-xl transition-all transform hover:scale-105 shadow-lg"
        >
          ✓ Verification Center
        </motion.button>
      </motion.div>

      {/* Quick Start Guide */}
      <motion.div
        variants={containerVariants}
        initial="hidden"
        animate="visible"
        className="bg-gray-800/50 border border-gray-700 rounded-xl p-8 backdrop-blur-sm"
      >
        <motion.h3 variants={itemVariants} className="text-2xl font-bold text-white mb-6">
          🚀 Quick Start Guide
        </motion.h3>
        <motion.div
          variants={containerVariants}
          className="grid grid-cols-1 md:grid-cols-4 gap-6"
        >
          {[
            { step: 1, title: 'Upload Data', desc: 'Add your CSV dataset' },
            {
              step: 2,
              title: 'Configure Experiment',
              desc: 'Set research question',
            },
            {
              step: 3,
              title: 'Run Analysis',
              desc: 'Execute AI workflows',
            },
            {
              step: 4,
              title: 'Compare Results',
              desc: 'View improvements',
            },
          ].map((item) => (
            <motion.div
              key={item.step}
              variants={itemVariants}
              className="bg-gray-700/50 rounded-lg p-4 border border-gray-600"
            >
              <div className="text-2xl font-bold text-indigo-400 mb-2">
                {item.step}
              </div>
              <p className="font-semibold text-white mb-1">{item.title}</p>
              <p className="text-sm text-gray-400">{item.desc}</p>
            </motion.div>
          ))}
        </motion.div>
      </motion.div>

      {loading && (
        <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50">
          <div className="bg-gray-900 rounded-xl p-8">
            <div className="animate-spin text-4xl">⏳</div>
            <p className="text-white mt-4">Loading...</p>
          </div>
        </div>
      )}
    </div>
  );
};
