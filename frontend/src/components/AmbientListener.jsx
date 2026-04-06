import React, { useState, useEffect, useRef } from 'react';

const AmbientListener = ({ onTranscriptAdded }) => {
  const [isListening, setIsListening] = useState(false);
  const [transcript, setTranscript] = useState('');
  const [hasSupport, setHasSupport] = useState(true);
  const [micError, setMicError] = useState(false);
  const recognitionRef = useRef(null);

  useEffect(() => {
    if (!('webkitSpeechRecognition' in window) && !('SpeechRecognition' in window)) {
      setHasSupport(false);
      return;
    }

    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    const recognition = new SpeechRecognition();
    recognition.continuous = true;
    recognition.interimResults = true;
    recognition.lang = 'en-US';

    recognition.onresult = (event) => {
      let currentInterim = '';
      let finalTranscript = '';

      for (let i = event.resultIndex; i < event.results.length; ++i) {
        if (event.results[i].isFinal) {
          finalTranscript += event.results[i][0].transcript;
        } else {
          currentInterim += event.results[i][0].transcript;
        }
      }

      setTranscript(currentInterim || finalTranscript);

      if (finalTranscript.trim()) {
        onTranscriptAdded(finalTranscript.trim());
        setTranscript('');
      }
    };

    recognition.onerror = (event) => {
      console.error('Speech recognition error setup:', event.error);
      if (event.error === 'not-allowed' || event.error === 'service-not-allowed') {
        setIsListening(false);
        setMicError(true);
      } else if (event.error === 'aborted') {
        // Prevent infinite restart loop if the browser engine forcefully aborts
        setIsListening(false);
      }
    };

    recognition.onend = () => {
      // Auto-restart seamless background recording if enabled
      if (isListening) {
        try {
          recognitionRef.current?.start();
        } catch(e) {}
      }
    };

    recognitionRef.current = recognition;

    return () => {
      recognition.stop();
    };
  }, [onTranscriptAdded, isListening]);

  useEffect(() => {
    if (!hasSupport) return;
    
    if (isListening && recognitionRef.current) {
      setMicError(false);
      try {
        recognitionRef.current.start();
      } catch (e) {}
    } else if (!isListening && recognitionRef.current) {
      recognitionRef.current.stop();
      setTranscript('');
    }
  }, [isListening, hasSupport]);

  if (!hasSupport) {
    return (
      <div style={{ fontSize: '0.75rem', color: 'var(--accent-orange)' }}>
        Web Speech API unsupported on this browser.
      </div>
    );
  }

  return (
    <div style={{ display: 'flex', alignItems: 'center', gap: '0.8rem' }}>
      {micError && (
        <div style={{ fontSize: '0.75rem', color: 'red', fontWeight: 600 }}>Mic Blocked! Allow in Browser URL Bar</div>
      )}
      {isListening && transcript && (
        <div style={{
          fontSize: '0.75rem', 
          color: 'var(--accent-blue)',
          maxWidth: '180px',
          whiteSpace: 'nowrap',
          overflow: 'hidden',
          textOverflow: 'ellipsis',
          fontStyle: 'italic',
          animation: 'fadeIn 0.2s',
          fontWeight: 500
        }}>
          "{transcript}"
        </div>
      )}

      <button 
        onClick={() => setIsListening(!isListening)}
        style={{
          display: 'flex', alignItems: 'center', gap: '0.4rem',
          background: isListening ? '#fee2e2' : '#f8fafc',
          border: `1px solid ${isListening ? '#fca5a5' : 'var(--border-color)'}`,
          color: isListening ? '#dc2626' : 'var(--text-muted)',
          padding: '0.3rem 0.6rem',
          borderRadius: '20px',
          fontSize: '0.75rem',
          fontWeight: 600,
          boxShadow: isListening ? 'inset 0 1px 3px rgba(0,0,0,0.1)' : '0 1px 2px rgba(0,0,0,0.05)'
        }}
      >
        <span style={{
          width: '6px', height: '6px', borderRadius: '50%',
          background: isListening ? '#dc2626' : 'var(--border-color)',
          boxShadow: isListening ? '0 0 4px #dc2626' : 'none'
        }}></span>
        {isListening ? 'Ambient Mic ON' : 'Ambient Mic OFF'}
      </button>
    </div>
  );
};

export default AmbientListener;
