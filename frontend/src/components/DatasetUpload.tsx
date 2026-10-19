import React, { useState } from 'react';
import { motion } from 'framer-motion';
import { useNavigate } from 'react-router-dom';
import { apiClient } from '../api/client';
import { useApp } from '../context/AppContext';

export const DatasetUpload: React.FC = () => {
  const navigate = useNavigate();
  const { addDataset, setLoading, setError, setMessage, loading } = useApp();
  const [file, setFile] = useState<File | null>(null);
  const [name, setName] = useState('');
  const [description, setDescription] = useState('');
  const [dragActive, setDragActive] = useState(false);
  const [uploadProgress, setUploadProgress] = useState(0);

  const handleDrag = (e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    if (e.type === 'dragenter' || e.type === 'dragover') {
      setDragActive(true);
    } else if (e.type === 'dragleave') {
      setDragActive(false);
    }
  };

  const handleDrop = (e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    setDragActive(false);

    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      setFile(e.dataTransfer.files[0]);
    }
  };

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files[0]) {
      setFile(e.target.files[0]);
    }
  };

  const handleUpload = async (e: React.FormEvent) => {
    e.preventDefault();

    if (!file) {
      setError('Please select a file');
      return;
    }

    if (!name) {
      setError('Please enter a dataset name');
      return;
    }

    setLoading(true);
    setError(null);

    try {
      const result = await apiClient.uploadDataset(file, {
        name,
        description,
      });

      if (result.error) {
        setError(result.error);
      } else if (result.data) {
        addDataset(result.data);
        setMessage('Dataset uploaded successfully!');
        setTimeout(() => navigate('/data-explorer'), 1500);
      }
    } catch (err) {
      setError('Upload failed');
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
      },
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
        className="max-w-2xl mx-auto"
      >
        {/* Header */}
        <motion.div variants={itemVariants} className="mb-8">
          <h1 className="text-4xl font-bold text-white mb-2">Upload Dataset</h1>
          <p className="text-gray-400">
            Upload your CSV file to begin your data science experiment
          </p>
        </motion.div>

        {/* Upload Area */}
        <motion.form
          variants={containerVariants}
          onSubmit={handleUpload}
          className="space-y-6"
        >
          {/* Drag and Drop */}
          <motion.div
            variants={itemVariants}
            onDragEnter={handleDrag}
            onDragLeave={handleDrag}
            onDragOver={handleDrag}
            onDrop={handleDrop}
            className={`border-2 border-dashed rounded-xl p-12 text-center transition-all ${
              dragActive
                ? 'border-indigo-500 bg-indigo-500/10'
                : 'border-gray-600 bg-gray-800/50 hover:border-gray-500'
            }`}
          >
            <div className="text-5xl mb-4">📁</div>
            <p className="text-gray-300 mb-2">
              Drag and drop your CSV file here
            </p>
            <p className="text-gray-500 text-sm mb-4">or</p>
            <label className="inline-block">
              <input
                type="file"
                accept=".csv"
                onChange={handleFileChange}
                className="hidden"
                disabled={loading}
              />
              <span className="bg-indigo-600 hover:bg-indigo-700 text-white font-semibold py-2 px-6 rounded-lg cursor-pointer transition-colors">
                Choose File
              </span>
            </label>
          </motion.div>

          {file && (
            <motion.div
              variants={itemVariants}
              className="bg-gray-800/50 border border-gray-700 rounded-lg p-4"
            >
              <p className="text-white">
                <strong>Selected:</strong> {file.name}
              </p>
              <p className="text-gray-400 text-sm">
                Size: {(file.size / 1024 / 1024).toFixed(2)} MB
              </p>
            </motion.div>
          )}

          {/* Form Fields */}
          <motion.div variants={itemVariants}>
            <label className="block text-white font-semibold mb-2">
              Dataset Name *
            </label>
            <input
              type="text"
              value={name}
              onChange={(e) => setName(e.target.value)}
              placeholder="e.g., Customer Churn Data"
              className="w-full bg-gray-800 border border-gray-700 rounded-lg px-4 py-3 text-white placeholder-gray-500 focus:outline-none focus:border-indigo-500 disabled:opacity-50"
              disabled={loading}
            />
          </motion.div>

          <motion.div variants={itemVariants}>
            <label className="block text-white font-semibold mb-2">
              Description
            </label>
            <textarea
              value={description}
              onChange={(e) => setDescription(e.target.value)}
              placeholder="Brief description of your dataset..."
              rows={4}
              className="w-full bg-gray-800 border border-gray-700 rounded-lg px-4 py-3 text-white placeholder-gray-500 focus:outline-none focus:border-indigo-500 disabled:opacity-50"
              disabled={loading}
            />
          </motion.div>

          {/* Error Message */}
          {/* Success Message */}

          {/* Progress Bar */}
          {uploadProgress > 0 && uploadProgress < 100 && (
            <motion.div variants={itemVariants} className="w-full h-2 bg-gray-700 rounded-full overflow-hidden">
              <motion.div
                className="h-full bg-gradient-to-r from-indigo-600 to-indigo-400"
                style={{ width: `${uploadProgress}%` }}
                animate={{ width: `${uploadProgress}%` }}
              />
            </motion.div>
          )}

          {/* Buttons */}
          <motion.div
            variants={itemVariants}
            className="flex gap-4 justify-end pt-4"
          >
            <button
              type="button"
              onClick={() => navigate(-1)}
              className="px-6 py-3 rounded-lg text-white border border-gray-600 hover:border-gray-500 transition-colors disabled:opacity-50"
              disabled={loading}
            >
              Cancel
            </button>
            <button
              type="submit"
              className="px-6 py-3 bg-gradient-to-r from-indigo-600 to-indigo-500 hover:from-indigo-700 hover:to-indigo-600 text-white font-semibold rounded-lg transition-all transform hover:scale-105 disabled:opacity-50"
              disabled={loading || !file}
            >
              {loading ? 'Uploading...' : 'Upload Dataset'}
            </button>
          </motion.div>
        </motion.form>

        {/* Tips */}
        <motion.div
          variants={containerVariants}
          initial="hidden"
          animate="visible"
          className="mt-12 bg-gray-800/50 border border-gray-700 rounded-xl p-6"
        >
          <motion.h3 variants={itemVariants} className="text-xl font-bold text-white mb-4">
            📋 Dataset Requirements
          </motion.h3>
          <motion.ul variants={containerVariants} className="space-y-2 text-gray-300">
            <motion.li variants={itemVariants}>
              ✓ CSV format (.csv)
            </motion.li>
            <motion.li variants={itemVariants}>
              ✓ At least 100 rows of data
            </motion.li>
            <motion.li variants={itemVariants}>
              ✓ Maximum 1 million rows
            </motion.li>
            <motion.li variants={itemVariants}>
              ✓ Clear column headers
            </motion.li>
            <motion.li variants={itemVariants}>
              ✓ Consistent data formatting
            </motion.li>
          </motion.ul>
        </motion.div>
      </motion.div>
    </div>
  );
};
