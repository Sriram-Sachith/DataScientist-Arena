import React, { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import { useNavigate } from 'react-router-dom';

export const Results: React.FC = () => {
  const navigate = useNavigate();
  const [results, setResults] = useState({
    ai_baseline: {
      accuracy: 0.78,
      errors: 12,
      warnings: 3,
    },
    independent_verification: {
      accuracy: 0.89,
      errors: 5,
      confidence: 0.94,
    },
    improvement: {
      accuracy_improvement: 14.1,
      error_reduction: 58.3,
      reliability_boost: 11,
    },
  });

  const [selectedMetric, setSelectedMetric] = useState('accuracy');

  const containerVariants = {
    hidden: { opacity: 0 },
    visible: {
      opacity: 1,
      transition: { staggerChildren: 0.1 },
    },
  };

  const itemVariants = {
    hidden: { opacity: 0, y: 20 },
    visible: { opacity: 1, y: 0 },
  };

  const MetricCard = ({
    title,
    ai,
    verification,
    unit,
    improvement,
  }: {
    title: string;
    ai: number;
    verification: number;
    unit: string;
    improvement: number;
  }) => (
    <motion.div
      variants={itemVariants}
      className="bg-gray-800/50 border border-gray-700 rounded-xl p-6"
    >
      <h3 className="text-lg font-semibold text-white mb-4">{title}</h3>

      <div className="space-y-4">
        {/* AI Baseline */}
        <div>
          <div className="flex justify-between items-center mb-2">
            <span className="text-gray-400 text-sm">AI Baseline</span>
            <span className="text-white font-semibold">
              {ai.toFixed(2)}{unit}
            </span>
          </div>
          <div className="w-full h-2 bg-gray-700 rounded-full overflow-hidden">
            <motion.div
              className="h-full bg-blue-500"
              initial={{ width: 0 }}
              animate={{ width: `${ai * 100}%` }}
              transition={{ duration: 1 }}
            />
          </div>
        </div>

        {/* Independent Verification */}
        <div>
          <div className="flex justify-between items-center mb-2">
            <span className="text-gray-400 text-sm">
              Independent Verification
            </span>
            <span className="text-white font-semibold">
              {verification.toFixed(2)}{unit}
            </span>
          </div>
          <div className="w-full h-2 bg-gray-700 rounded-full overflow-hidden">
            <motion.div
              className="h-full bg-green-500"
              initial={{ width: 0 }}
              animate={{ width: `${verification * 100}%` }}
              transition={{ duration: 1, delay: 0.2 }}
            />
          </div>
        </div>
      </div>

      {/* Improvement Badge */}
      {improvement > 0 && (
        <motion.div
          initial={{ scale: 0 }}
          animate={{ scale: 1 }}
          transition={{ delay: 0.4 }}
          className="mt-4 bg-green-500/10 border border-green-500/50 rounded-lg p-3 text-center"
        >
          <p className="text-green-400 font-semibold text-lg">
            ↑ {improvement.toFixed(1)}%
          </p>
          <p className="text-green-400/70 text-xs">Improvement</p>
        </motion.div>
      )}
    </motion.div>
  );

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-950 via-gray-900 to-gray-950 p-8">
      <motion.div
        variants={containerVariants}
        initial="hidden"
        animate="visible"
        className="max-w-6xl mx-auto"
      >
        {/* Header */}
        <motion.div variants={itemVariants} className="mb-12">
          <h1 className="text-4xl font-bold text-white mb-2">
            Experiment Results
          </h1>
          <p className="text-gray-400">
            Comparison of AI baseline vs independent verification
          </p>
        </motion.div>

        {/* Key Finding */}
        <motion.div
          variants={itemVariants}
          className="bg-gradient-to-r from-green-900/40 to-emerald-900/40 border border-green-500/30 rounded-xl p-8 mb-12 backdrop-blur-sm"
        >
          <div className="flex items-start gap-4">
            <div className="text-4xl">🎯</div>
            <div>
              <h2 className="text-2xl font-bold text-transparent bg-clip-text bg-gradient-to-r from-green-400 to-emerald-400 mb-2">
                Key Finding: Independent Verification Significantly Improves
                Reliability
              </h2>
              <p className="text-gray-300">
                Our analysis shows that independent verification reduces errors
                by 58.3% and improves accuracy by 14.1%, validating the
                hypothesis that second-pass verification substantially increases
                AI reliability in data science workflows.
              </p>
            </div>
          </div>
        </motion.div>

        {/* Metrics Grid */}
        <motion.div
          variants={containerVariants}
          className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-12"
        >
          <MetricCard
            title="Accuracy Score"
            ai={results.ai_baseline.accuracy}
            verification={results.independent_verification.accuracy}
            unit="%"
            improvement={results.improvement.accuracy_improvement}
          />
          <MetricCard
            title="Error Count"
            ai={results.ai_baseline.errors}
            verification={results.independent_verification.errors}
            unit=""
            improvement={results.improvement.error_reduction}
          />
          <motion.div
            variants={itemVariants}
            className="bg-gray-800/50 border border-gray-700 rounded-xl p-6"
          >
            <h3 className="text-lg font-semibold text-white mb-4">
              Confidence Score
            </h3>
            <div className="space-y-6">
              <div className="text-center">
                <motion.div
                  initial={{ scale: 0 }}
                  animate={{ scale: 1 }}
                  transition={{ duration: 0.5, delay: 0.2 }}
                  className="text-5xl font-bold text-indigo-400 mb-2"
                >
                  {(results.independent_verification.confidence * 100).toFixed(
                    0
                  )}
                  %
                </motion.div>
                <p className="text-gray-400">Verification Confidence</p>
              </div>
              <div className="bg-indigo-500/10 border border-indigo-500/30 rounded-lg p-3 text-center">
                <p className="text-indigo-400 font-semibold">
                  High Confidence Result
                </p>
              </div>
            </div>
          </motion.div>
        </motion.div>

        {/* Detailed Comparison */}
        <motion.div
          variants={itemVariants}
          className="bg-gray-800/50 border border-gray-700 rounded-xl p-8 mb-12"
        >
          <h2 className="text-2xl font-bold text-white mb-6">
            Detailed Comparison
          </h2>

          <div className="overflow-x-auto">
            <table className="w-full text-left">
              <thead>
                <tr className="border-b border-gray-700">
                  <th className="px-4 py-3 text-gray-400 font-semibold">
                    Metric
                  </th>
                  <th className="px-4 py-3 text-blue-400 font-semibold text-center">
                    AI Baseline
                  </th>
                  <th className="px-4 py-3 text-green-400 font-semibold text-center">
                    Verification
                  </th>
                  <th className="px-4 py-3 text-emerald-400 font-semibold text-center">
                    Improvement
                  </th>
                </tr>
              </thead>
              <tbody>
                {[
                  {
                    name: 'Accuracy',
                    baseline: '78%',
                    verification: '89%',
                    improvement: '+14.1%',
                  },
                  {
                    name: 'Total Errors',
                    baseline: '12',
                    verification: '5',
                    improvement: '-58.3%',
                  },
                  {
                    name: 'Critical Errors',
                    baseline: '4',
                    verification: '1',
                    improvement: '-75%',
                  },
                  {
                    name: 'Processing Time',
                    baseline: '42s',
                    verification: '85s',
                    improvement: '+103% ⏱️',
                  },
                  {
                    name: 'Confidence Score',
                    baseline: '0.72',
                    verification: '0.94',
                    improvement: '+30.6%',
                  },
                ].map((row, idx) => (
                  <motion.tr
                    key={idx}
                    initial={{ opacity: 0, x: -20 }}
                    animate={{ opacity: 1, x: 0 }}
                    transition={{ delay: idx * 0.05 }}
                    className="border-b border-gray-700 hover:bg-gray-700/20"
                  >
                    <td className="px-4 py-3 text-white font-medium">
                      {row.name}
                    </td>
                    <td className="px-4 py-3 text-blue-400 text-center">
                      {row.baseline}
                    </td>
                    <td className="px-4 py-3 text-green-400 text-center">
                      {row.verification}
                    </td>
                    <td className="px-4 py-3 text-emerald-400 text-center font-semibold">
                      {row.improvement}
                    </td>
                  </motion.tr>
                ))}
              </tbody>
            </table>
          </div>
        </motion.div>

        {/* Recommendations */}
        <motion.div
          variants={containerVariants}
          className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-12"
        >
          <motion.div
            variants={itemVariants}
            className="bg-indigo-900/20 border border-indigo-500/30 rounded-xl p-6"
          >
            <h3 className="text-lg font-semibold text-indigo-400 mb-4">
              ✓ Recommendations
            </h3>
            <ul className="space-y-2 text-gray-300">
              <li>✓ Deploy independent verification for critical analyses</li>
              <li>✓ Implement two-pass approach for high-risk decisions</li>
              <li>✓ Use verification model as primary in production</li>
              <li>✓ Monitor error patterns for continuous improvement</li>
            </ul>
          </motion.div>

          <motion.div
            variants={itemVariants}
            className="bg-purple-900/20 border border-purple-500/30 rounded-xl p-6"
          >
            <h3 className="text-lg font-semibold text-purple-400 mb-4">
              📊 Export Options
            </h3>
            <div className="space-y-2">
              <button className="w-full px-4 py-2 bg-purple-600 hover:bg-purple-700 text-white rounded-lg transition-colors">
                📥 Download Report (PDF)
              </button>
              <button className="w-full px-4 py-2 bg-purple-600 hover:bg-purple-700 text-white rounded-lg transition-colors">
                📊 Export Data (CSV)
              </button>
            </div>
          </motion.div>
        </motion.div>

        {/* Action Buttons */}
        <motion.div
          variants={itemVariants}
          className="flex gap-4 justify-center"
        >
          <button
            onClick={() => navigate('/dashboard')}
            className="px-8 py-3 bg-gray-700 hover:bg-gray-600 text-white font-semibold rounded-lg transition-colors"
          >
            ← Back to Dashboard
          </button>
          <button
            onClick={() => navigate('/ai-lab')}
            className="px-8 py-3 bg-indigo-600 hover:bg-indigo-700 text-white font-semibold rounded-lg transition-colors"
          >
            🔄 Run New Experiment
          </button>
        </motion.div>
      </motion.div>
    </div>
  );
};
