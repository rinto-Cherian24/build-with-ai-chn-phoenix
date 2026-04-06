import { useState, useEffect } from 'react';
import './App.css';
import AgentArena from './components/AgentArena';
import ContextPanel from './components/ContextPanel';
import SimulationResultModal from './components/SimulationResultModal';
import { db } from './firebase';
import { ref, onValue } from 'firebase/database';

function App() {
  const [prompt, setPrompt] = useState('Launch a 50% discount blitz for 24h via pop-ups and push notifications.');
  const [isSimulating, setIsSimulating] = useState(false);
  const [showSummary, setShowSummary] = useState(false);
  const [activeSpeaker, setActiveSpeaker] = useState(null);
  const [visibleMessages, setVisibleMessages] = useState([]);
  
  // Phase 3: Realtime Database Connection
  const [contextMemory, setContextMemory] = useState([]);
  const [simulationSummary, setSimulationSummary] = useState(null);

  // Read Firebase RTDB using WebSockets (onValue)
  useEffect(() => {
    const contextRef = ref(db, 'extracted_context');
    const unsubscribe = onValue(contextRef, (snapshot) => {
      const data = snapshot.val();
      if (data) {
        const rawArray = Object.values(data);
        const finalMemory = [];
        
        // Convert to UI memory format
        rawArray.forEach((meeting, idx) => {
             if (meeting.extracted_items) {
                 meeting.extracted_items.forEach((item, innerIdx) => {
                     finalMemory.push({
                         id: `fb-${idx}-${innerIdx}`,
                         type: item.type,
                         topic: item.assignee || 'General Task',
                         content: item.content,
                         time: item.deadline || 'No Deadline',
                         suggestion: item.proactive_suggestion || null
                     });
                 });
             }
        });
        
        // Reverse so newest items are at the top
        setContextMemory(finalMemory.reverse());
      }
    });

    // Cleanup listener on unmount
    return () => unsubscribe();
  }, []);

  const handleTranscriptAdded = async (transcriptText) => {
    // Send to Context Extractor backend
    try {
        await fetch('http://127.0.0.1:8000/api/process-meeting', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ meeting_id: `live_${Date.now()}`, transcript: transcriptText })
        });
        // Note: No need to setContextMemory here manually!
        // Firebase onValue listener above will instantly catch the DB update and trigger the UI.
    } catch(err) {
        console.error("Backend Context Extractor offline", err);
    }
  };

  const handleSimulate = async () => {
    if (!prompt.trim()) return;
    setIsSimulating(true);
    setShowSummary(false);
    setVisibleMessages([]);
    setActiveSpeaker(null);
    
    try {
        // Send to Praxis Swarm Backend
        const response = await fetch('http://127.0.0.1:8000/api/simulate-praxis', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ prompt: prompt })
        });
        const result = await response.json();
        setSimulationSummary(result);
        
        // Feed the chat logs into the UI
        result.conversation.forEach((msg) => {
          setTimeout(() => setActiveSpeaker(msg.agentId), Math.max(0, msg.timeOffset - 1000));
          setTimeout(() => setVisibleMessages(prev => [...prev, msg]), msg.timeOffset);
        });
        
        const finalOffset = result.conversation[result.conversation.length - 1].timeOffset;
        setTimeout(() => setActiveSpeaker(null), finalOffset + 1500);
        setTimeout(() => {
          setIsSimulating(false);
          setShowSummary(true);
        }, finalOffset + 3000);

    } catch(err) {
        console.error("Simulation failed", err);
        setIsSimulating(false);
    }
  };

  const handleRewrite = () => {
    if (simulationSummary && simulationSummary.saferVariant) {
        setPrompt(simulationSummary.saferVariant);
    }
    setShowSummary(false);
  };

  return (
    <div className="layout-container">
      <AgentArena activeSpeaker={activeSpeaker} />
      <ContextPanel 
        prompt={prompt}
        setPrompt={setPrompt}
        isSimulating={isSimulating}
        onSimulate={handleSimulate}
        visibleMessages={visibleMessages}
        contextMemory={contextMemory}
        onTranscriptAdded={handleTranscriptAdded}
      />
      {showSummary && simulationSummary && (
        <SimulationResultModal 
          onClose={() => setShowSummary(false)}
          onRewrite={handleRewrite}
          summary={simulationSummary}
        />
      )}
    </div>
  );
}

export default App;
