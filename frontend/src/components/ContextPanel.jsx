import React, { useRef, useEffect } from 'react';
import { agents } from '../data/mockData';
import AmbientListener from './AmbientListener';

const ContextPanel = ({ prompt, setPrompt, isSimulating, onSimulate, visibleMessages, contextMemory, onTranscriptAdded }) => {
  const scrollRef = useRef(null);

  useEffect(() => {
    if (scrollRef.current) {
      scrollRef.current.scrollTop = scrollRef.current.scrollHeight;
    }
  }, [visibleMessages]);

  return (
    <div className="right-panel glass-panel">
      <div className="context-memory-section">
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1rem' }}>
          <h2 style={{ margin: 0 }}>
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><circle cx="12" cy="12" r="10"></circle><polyline points="12 6 12 12 16 14"></polyline></svg>
            Context Memory
          </h2>
          <AmbientListener onTranscriptAdded={onTranscriptAdded} />
        </div>
        <div className="context-cards">
          {contextMemory.map(mem => (
            <div key={mem.id} className="context-card">
              <div className="context-card-header">
                <span className={`badge ${mem.type}`}>{mem.type}</span>
                <span style={{color: 'var(--text-muted)'}}>{mem.time}</span>
              </div>
              <div style={{fontWeight: 500, margin: '0.3rem 0', color: 'var(--text-main)'}}>{mem.topic}</div>
              <div className="context-card-desc">{mem.content}</div>
              {mem.suggestion && (
                <button 
                  className="ai-sparkle-btn" 
                  style={{
                    marginTop: '0.8rem', width: '100%', background: 'linear-gradient(90deg, #60efff, #00ff87)', 
                    border: 'none', borderRadius: '4px', padding: '0.6rem', color: '#091e3b', 
                    fontWeight: 700, fontSize: '0.85rem', cursor: 'pointer',
                    boxShadow: '0 4px 15px rgba(0, 255, 135, 0.4)', transition: 'all 0.2sease-in-out'
                  }}
                  onClick={() => alert("Simulating Developer 3 hooking up Google Workspace APIs...")}
                >
                  ✨ {mem.suggestion}
                </button>
              )}
            </div>
          ))}
        </div>
      </div>

      {visibleMessages && visibleMessages.length > 0 && (
        <div 
          ref={scrollRef}
          style={{
            flex: 1, overflowY: 'auto', display: 'flex', flexDirection: 'column', gap: '0.8rem',
            background: '#f8fafc', borderRadius: '6px', padding: '1rem', border: '1px solid var(--border-color)',
            animation: 'fadeIn 0.2s ease-out'
          }}
        >
          <div style={{color: 'var(--text-muted)', fontSize: '0.75rem', fontWeight: 700, textTransform: 'uppercase', marginBottom: '0.2rem'}}>Active Conversation</div>
          {visibleMessages.map((msg, idx) => {
            const agentInfo = agents.find(a => a.id === msg.agentId);
            return (
              <div key={idx} style={{ display: 'flex', flexDirection: 'column', gap: '0.3rem', animation: 'fadeIn 0.3s ease-out' }}>
                <div style={{ fontWeight: 600, fontSize: '0.8rem', color: agentInfo?.color || 'var(--text-main)' }}>
                  {msg.agentName}
                </div>
                <div style={{ background: '#ffffff', border: '1px solid var(--border-color)', padding: '0.8rem', borderRadius: '6px', color: 'var(--text-main)', fontSize: '0.9rem', boxShadow: '0 1px 2px rgba(0,0,0,0.02)' }}>
                  {msg.text}
                </div>
              </div>
            );
          })}
        </div>
      )}

      <div className="prompt-section">
        <h3>Test a Policy or Campaign</h3>
        <textarea 
          className="prompt-input"
          value={prompt}
          onChange={(e) => setPrompt(e.target.value)}
          placeholder="E.g. Launch a 50% discount blitz for 24h via pop-ups..."
          disabled={isSimulating}
        />
        <button 
          className={`simulate-btn ${isSimulating ? 'simulating' : ''}`}
          onClick={onSimulate}
          disabled={isSimulating || !prompt}
        >
          {isSimulating ? 'Running Behavioral Simulation...' : 'Simulate Impact'}
          {!isSimulating && (
             <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2"><polygon points="5 3 19 12 5 21 5 3"></polygon></svg>
          )}
        </button>
      </div>
    </div>
  );
};

export default ContextPanel;
