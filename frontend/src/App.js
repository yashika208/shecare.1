import React from 'react';
import './App.css';

function App() {
  return (
    <div className="app-container">
      <header className="header">
        <h1>SheCare 💖</h1>
        <p className="tagline">Track. Heal. Empower.</p>
        <button className="cta-button">Get Started</button>
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
    </div>
  );
}

export default App;
