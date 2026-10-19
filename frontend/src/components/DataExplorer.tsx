import React, { useState } from 'react';
import { motion } from 'framer-motion';

export default function DataExplorer() {
  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      className="space-y-6"
    >
      <h1>Dataset Explorer</h1>
      <div className="card">
        <p className="text-text-secondary">Explore dataset distributions, relationships, and data quality issues</p>
        <div className="mt-6 space-y-4">
          <div className="bg-slate-700/30 rounded-lg p-6 text-center">
            <p className="text-text-secondary">Tabs: Overview | Data Quality | Distributions | Relationships | Risk Indicators</p>
          </div>
        </div>
      </div>
    </motion.div>
  );
}
