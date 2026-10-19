import React from 'react';
import { motion } from 'framer-motion';
import { CheckCircle, AlertCircle, AlertTriangle } from 'lucide-react';

export default function VerificationCenter() {
  const checks = [
    { name: 'Schema Integrity', status: 'passed' },
    { name: 'Data Splitting', status: 'passed' },
    { name: 'Preprocessing Leakage', status: 'passed' },
    { name: 'Metric Correctness', status: 'passed' },
  ];

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      className="space-y-6"
    >
      <h1>Independent Verification Center</h1>
      <div className="card">
        <p className="text-text-secondary mb-6">Verify AI-generated results independently</p>
        
        <div className="space-y-3">
          {checks.map((check) => (
            <div key={check.name} className="flex items-center gap-3 p-3 bg-slate-700/30 rounded-lg">
              {check.status === 'passed' && <CheckCircle className="w-5 h-5 text-emerald-400" />}
              {check.status === 'warning' && <AlertTriangle className="w-5 h-5 text-amber-400" />}
              <span>{check.name}</span>
              <span className="ml-auto text-sm text-text-secondary capitalize">{check.status}</span>
            </div>
          ))}
        </div>
      </div>
    </motion.div>
  );
}
