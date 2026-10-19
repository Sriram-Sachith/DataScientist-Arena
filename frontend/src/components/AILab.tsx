import React, { useState } from 'react';
import { motion } from 'framer-motion';
import { useNavigate } from 'react-router-dom';
import { apiClient } from '../api/client';
import { useApp } from '../context/AppContext';

export const AILab: React.FC = () => {
  const navigate = useNavigate();
  const { datasets, addExperiment, setLoading, setError, setMessage, loading } =
    useApp();
  const [step, setStep] = useState(1);
  const [formData, setFormData] = useState({
    name: '',
    research_question: '',
    dataset_id: '',
    approach: 'ai_baseline',
  });

  const [generatedPlan, setGeneratedPlan] = useState<any>(null);

  const handleInputChange = (
    e: React.ChangeEvent<
      HTMLInputElement | HTMLTextAreaElement | HTMLSelectElement
    >
  ) => {
    const { name, value } = e.target;
    setFormData((prev) => ({ ...prev, [name]: value }));
  };

  const handleGeneratePlan = async () => {
    if (!formData.research_question || !formData.dataset_id) {
      setError('Please fill in all required fields');
      return;
    }

    setLoading(true);
    setError(null);

    try {
      const result = await apiClient.createAnalysisPlan({
        experiment_id: `exp_${Date.now()}`,
        research_question: formData.research_question,
        dataset_profile: {
          rows: 1000,
          columns: 15,
        },
      });

      if (result.error) {
        setError(result.error);
      } else if (result.data) {
        setGeneratedPlan(result.data);
        setStep(3);
      }
    } catch (err) {
      setError('Failed to generate plan');
    } finally {
      setLoading(false);
    }
  };

  const handleExecute = async () => {
    if (!generatedPlan) return;

    setLoading(true);
    setError(null);

    try {
      const result = await apiClient.executeAnalysisPlan(generatedPlan.id);

      if (result.error) {
        setError(result.error);
      } else {
        setMessage('Analysis execution started!');
        const newExperiment = {
          id: `exp_${Date.now()}`,
          name: formData.name,
          research_question: formData.research_question,
          dataset_id: formData.dataset_id,
          status: 'running',
          created_at: new Date().toISOString(),
        };
        addExperiment(newExperiment);
        setTimeout(() => navigate('/run-monitor'), 1500);
      }
    } catch (err) {
      setError('Failed to execute analysis');
    } finally {
      setLoading(false);
    }
  };

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

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-950 via-gray-900 to-gray-950 p-8">
      <motion.div
        variants={containerVariants}
        initial="hidden"
        animate="visible"
        className="max-w-4xl mx-auto"
      >
        {/* Header */}
        <motion.div variants={itemVariants} className="mb-8">
          <h1 className="text-4xl font-bold text-white mb-2">AI Lab</h1>
          <p className="text-gray-400">
            Design and execute your data science experiments
          </p>
        </motion.div>

        {/* Step Indicator */}
        <motion.div
          variants={itemVariants}
          className="flex justify-between mb-12"
        >
          {[
            { num: 1, title: 'Setup' },
            { num: 2, title: 'Configure' },
            { num: 3, title: 'Review' },
            { num: 4, title: 'Execute' },
          ].map((s) => (
            <div key={s.num} className="flex flex-col items-center flex-1">
              <motion.div
                className={`w-12 h-12 rounded-full flex items-center justify-center font-bold text-lg mb-2 transition-all ${
                  step >= s.num
                    ? 'bg-indigo-600 text-white'
                    : 'bg-gray-700 text-gray-400'
                }`}
                animate={{
                  scale: step === s.num ? 1.1 : 1,
                  boxShadow:
                    step === s.num ? '0 0 20px rgba(99, 102, 241, 0.5)' : 'none',
                }}
              >
                {s.num}
              </motion.div>
              <p
                className={`text-sm ${
                  step >= s.num ? 'text-white' : 'text-gray-500'
                }`}
              >
                {s.title}
              </p>
            </div>
          ))}
        </motion.div>

        {/* Step 1: Setup */}
        {step === 1 && (
          <motion.div
            variants={containerVariants}
            initial="hidden"
            animate="visible"
            className="space-y-6 bg-gray-800/50 border border-gray-700 rounded-xl p-8"
          >
            <motion.h2 variants={itemVariants} className="text-2xl font-bold text-white">
              Experiment Setup
            </motion.h2>

            <motion.div variants={itemVariants}>
              <label className="block text-white font-semibold mb-2">
                Experiment Name *
              </label>
              <input
                type="text"
                name="name"
                value={formData.name}
                onChange={handleInputChange}
                placeholder="e.g., Customer Churn Prediction Q4"
                className="w-full bg-gray-700 border border-gray-600 rounded-lg px-4 py-3 text-white placeholder-gray-500 focus:outline-none focus:border-indigo-500"
              />
            </motion.div>

            <motion.div variants={itemVariants}>
              <label className="block text-white font-semibold mb-2">
                Select Dataset *
              </label>
              <select
                name="dataset_id"
                value={formData.dataset_id}
                onChange={handleInputChange}
                className="w-full bg-gray-700 border border-gray-600 rounded-lg px-4 py-3 text-white focus:outline-none focus:border-indigo-500"
              >
                <option value="">Choose a dataset...</option>
                {datasets.map((d) => (
                  <option key={d.id} value={d.id}>
                    {d.name} ({d.rows} rows)
                  </option>
                ))}
              </select>
              {datasets.length === 0 && (
                <p className="text-amber-400 text-sm mt-2">
                  No datasets available. Please upload one first.
                </p>
              )}
            </motion.div>

            <motion.div
              variants={itemVariants}
              className="flex gap-4 justify-end pt-4"
            >
              <button
                onClick={() => navigate(-1)}
                className="px-6 py-3 rounded-lg text-white border border-gray-600 hover:border-gray-500 transition-colors"
              >
                Cancel
              </button>
              <button
                onClick={() => setStep(2)}
                disabled={!formData.name || !formData.dataset_id}
                className="px-6 py-3 bg-indigo-600 hover:bg-indigo-700 text-white font-semibold rounded-lg transition-colors disabled:opacity-50"
              >
                Next →
              </button>
            </motion.div>
          </motion.div>
        )}

        {/* Step 2: Configure */}
        {step === 2 && (
          <motion.div
            variants={containerVariants}
            initial="hidden"
            animate="visible"
            className="space-y-6 bg-gray-800/50 border border-gray-700 rounded-xl p-8"
          >
            <motion.h2 variants={itemVariants} className="text-2xl font-bold text-white">
              Define Your Research Question
            </motion.h2>

            <motion.div variants={itemVariants}>
              <label className="block text-white font-semibold mb-2">
                Research Question *
              </label>
              <textarea
                name="research_question"
                value={formData.research_question}
                onChange={handleInputChange}
                placeholder="What specific question do you want to answer with this data?"
                rows={4}
                className="w-full bg-gray-700 border border-gray-600 rounded-lg px-4 py-3 text-white placeholder-gray-500 focus:outline-none focus:border-indigo-500"
              />
            </motion.div>

            <motion.div variants={itemVariants}>
              <label className="block text-white font-semibold mb-2">
                Experiment Approach
              </label>
              <div className="space-y-3">
                {[
                  {
                    value: 'ai_baseline',
                    label: 'AI Baseline',
                    desc: 'Standard AI analysis',
                  },
                  {
                    value: 'independent_verification',
                    label: 'Independent Verification',
                    desc: 'AI + Independent Verification',
                  },
                  {
                    value: 'manual',
                    label: 'Manual Review',
                    desc: 'Expert human analysis',
                  },
                ].map((approach) => (
                  <label
                    key={approach.value}
                    className="flex items-center cursor-pointer"
                  >
                    <input
                      type="radio"
                      name="approach"
                      value={approach.value}
                      checked={formData.approach === approach.value}
                      onChange={handleInputChange}
                      className="w-4 h-4"
                    />
                    <span className="ml-3 text-white font-medium">
                      {approach.label}
                      <p className="text-gray-400 text-sm">{approach.desc}</p>
                    </span>
                  </label>
                ))}
              </div>
            </motion.div>

            <motion.div
              variants={itemVariants}
              className="flex gap-4 justify-end pt-4"
            >
              <button
                onClick={() => setStep(1)}
                className="px-6 py-3 rounded-lg text-white border border-gray-600 hover:border-gray-500 transition-colors"
              >
                ← Back
              </button>
              <button
                onClick={handleGeneratePlan}
                disabled={!formData.research_question || loading}
                className="px-6 py-3 bg-indigo-600 hover:bg-indigo-700 text-white font-semibold rounded-lg transition-colors disabled:opacity-50"
              >
                {loading ? 'Generating...' : 'Generate Plan →'}
              </button>
            </motion.div>
          </motion.div>
        )}

        {/* Step 3: Review Plan */}
        {step === 3 && generatedPlan && (
          <motion.div
            variants={containerVariants}
            initial="hidden"
            animate="visible"
            className="space-y-6"
          >
            <motion.h2 variants={itemVariants} className="text-2xl font-bold text-white">
              Review Generated Plan
            </motion.h2>

            <motion.div
              variants={itemVariants}
              className="bg-gray-800/50 border border-gray-700 rounded-xl p-6"
            >
              <h3 className="text-lg font-semibold text-indigo-400 mb-4">
                Proposed Techniques
              </h3>
              <ul className="space-y-2 text-gray-300">
                {generatedPlan.proposed_techniques?.map(
                  (technique: string, idx: number) => (
                    <li key={idx} className="flex items-start">
                      <span className="text-indigo-400 mr-3">✓</span>
                      <span>{technique}</span>
                    </li>
                  )
                )}
              </ul>
            </motion.div>

            <motion.div
              variants={itemVariants}
              className="grid grid-cols-2 gap-4"
            >
              <div className="bg-blue-900/30 border border-blue-700/50 rounded-lg p-4">
                <p className="text-gray-400 text-sm mb-1">Estimated Time</p>
                <p className="text-2xl font-bold text-blue-400">
                  {generatedPlan.estimated_time_minutes} min
                </p>
              </div>
              <div className="bg-green-900/30 border border-green-700/50 rounded-lg p-4">
                <p className="text-gray-400 text-sm mb-1">Confidence Score</p>
                <p className="text-2xl font-bold text-green-400">92%</p>
              </div>
            </motion.div>

            <motion.div
              variants={itemVariants}
              className="flex gap-4 justify-end pt-4"
            >
              <button
                onClick={() => setStep(2)}
                className="px-6 py-3 rounded-lg text-white border border-gray-600 hover:border-gray-500 transition-colors"
              >
                ← Back
              </button>
              <button
                onClick={handleExecute}
                disabled={loading}
                className="px-6 py-3 bg-green-600 hover:bg-green-700 text-white font-semibold rounded-lg transition-colors disabled:opacity-50"
              >
                {loading ? 'Executing...' : '▶ Execute Analysis'}
              </button>
            </motion.div>
          </motion.div>
        )}
      </motion.div>
    </div>
  );
};
