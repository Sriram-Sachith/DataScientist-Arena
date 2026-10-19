import React from 'react';
import { motion } from 'framer-motion';

export default function RunMonitor() {
  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      className="space-y-6"
    >
      <h1>Experiment Run Monitor</h1>
      <div className="card">
        <p className="text-text-secondary mb-6">Track execution of three approaches in real-time</p>
        
        <div className="space-y-4">
          {['Baseline ML', 'AI-Generated', 'Verified AI'].map((approach) => (
            <div key={approach} className="bg-slate-700/30 rounded-lg p-4">
              <div className="flex items-center justify-between mb-2">
                <span className="font-semibold">{approach}</span>
                <span className="text-sm text-emerald-400">In Progress</span>
              </div>
              <div className="w-full bg-slate-800 rounded-full h-2">
                <div className="bg-gradient-to-r from-emerald-500 to-blue-500 h-2 rounded-full" style={{ width: '65%' }}></div>
              </div>
              <p className="text-xs text-text-secondary mt-2">Data preparation 65%</p>
            </div>
          ))}
        </div>
      </div>
    </motion.div>
  );
}
