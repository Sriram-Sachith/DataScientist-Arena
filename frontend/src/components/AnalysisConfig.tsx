import React from 'react';
import { motion } from 'framer-motion';

export default function AnalysisConfig() {
  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      className="space-y-6"
    >
      <h1>Analysis Configuration</h1>
      <div className="card">
        <p className="text-text-secondary">Configure experiment parameters before AI and baseline runs</p>
        <div className="mt-6 space-y-4">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <label className="block text-sm font-semibold mb-2">Dataset</label>
              <select className="input-field">
                <option>Select dataset...</option>
              </select>
            </div>
            <div>
              <label className="block text-sm font-semibold mb-2">Target Column</label>
              <select className="input-field">
                <option>Select target...</option>
              </select>
            </div>
          </div>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <div>
              <label className="block text-sm font-semibold mb-2">Task Type</label>
              <select className="input-field">
                <option>Classification</option>
                <option>Regression</option>
              </select>
            </div>
            <div>
              <label className="block text-sm font-semibold mb-2">Train/Test Split</label>
              <input type="number" defaultValue="0.8" min="0.5" max="0.95" step="0.05" className="input-field" />
            </div>
            <div>
              <label className="block text-sm font-semibold mb-2">Random Seed</label>
              <input type="number" defaultValue="42" className="input-field" />
            </div>
          </div>
          <button className="btn-primary w-full">Continue to AI Analysis Lab</button>
        </div>
      </div>
    </motion.div>
  );
}
