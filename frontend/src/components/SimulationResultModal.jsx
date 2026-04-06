import React from 'react';

const SimulationResultModal = ({ onClose, onRewrite, summary }) => {
  if (!summary) return null;
  
  return (
    <div className="modal-overlay" onClick={onClose}>
      <div className="summary-modal glass-panel" onClick={e => e.stopPropagation()}>
        <h2>Simulation Results</h2>
        
        <div className="risk-score">
          <div>
            <div style={{color: 'var(--text-muted)', fontSize: '0.75rem', fontWeight: 700, textTransform: 'uppercase', marginBottom: '0.2rem'}}>Systemic Risk Score</div>
            <div style={{color: 'var(--text-main)', fontSize: '1rem', fontWeight: 500}}>{summary.sayDoGap}</div>
          </div>
          <div className={`risk-value ${summary.riskLevel || 'medium'}`}>
            {summary.riskScore}%
          </div>
        </div>

        <div className="insight-section">
          <h4>Behavioral Insight</h4>
          <div className="insight-content">
            {summary.insight}
          </div>
        </div>

        <div className="insight-section" style={{marginBottom: 0}}>
          <h4>Safer Variant Recommendation</h4>
          <div className="better-variant">
            {summary.saferVariant}
          </div>
        </div>

        <div className="modal-actions">
          <button className="btn-secondary" onClick={onClose}>Dismiss</button>
          <button className="btn-primary" onClick={onRewrite}>Apply Rewrite</button>
        </div>
      </div>
    </div>
  );
};

export default SimulationResultModal;
