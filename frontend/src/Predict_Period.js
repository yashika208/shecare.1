import React, { useState } from 'react';
import './App.css';
import PeriodTracker from './Predict_Period';

function App() {
  const [showTracker, setShowTracker] = useState(false);

  const handleGetStarted = () => {
    setShowTracker(true);
  };

  return (
    <div className="app-container">
      {!showTracker ? (
        <>
          <header className="header">
            <h1>SheCare 💖</h1>
            <p className="tagline">Track. Heal. Empower.</p>
            <button className="cta-button" onClick={handleGetStarted}>
              Get Started
            </button>
          </header>

          <section className="features">
            <h2>Why SheCare?</h2>
            <ul>
              <li>📅 Smart Period & PCOS Tracker</li>
              <li>🤖 AI Suggestions for Lifestyle & Diet</li>
              <li>🌸 Relaxing Music, Activities & Reminders</li>
              <li>📊 Insights & Monthly Reports</li>
            </ul>
          </section>
        </>
      ) : (
        <PeriodTracker />
      )}
    </div>
  );
}

export default App;
