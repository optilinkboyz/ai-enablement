import React, { useState } from "react";
import UploadPanel from "./components/UploadPanel";
import QuestionInput from "./components/QuestionInput";
import ResponseDisplay from "./components/ResponseDisplay";
import "./index.css";

export default function App() {
  const [documentContext, setDocumentContext] = useState(null);
  const [documentName, setDocumentName] = useState(null);
  const [results, setResults] = useState([]);
  const [error, setError] = useState(null);

  const handleUploadSuccess = (extractedText, filename) => {
    setDocumentContext(extractedText);
    setDocumentName(filename);
    setError(null);
  };

  const handleUploadError = (message) => {
    setError(message);
    setTimeout(() => setError(null), 5000);
  };

  const handleResult = (result) => {
    setResults((prev) => [...prev, result]);
    setError(null);
  };

  const handleError = (message) => {
    setError(message);
    setTimeout(() => setError(null), 5000);
  };

  const handleClearResults = () => { setResults([]); setError(null); };
  const handleClearDocument = () => { setDocumentContext(null); setDocumentName(null); };

  return (
    <div className="app">
      <header className="app-header">
        <div className="header-content">
          <div className="header-logo">
            <span className="logo-icon">⚡</span>
            <div>
              <h1 className="header-title">AT&S AI Assistant</h1>
              <p className="header-subtitle">Digital & AI Enablement — Corporate IT</p>
            </div>
          </div>
          {results.length > 0 && (
            <button className="btn-clear" onClick={handleClearResults}>🗑️ Clear Results</button>
          )}
        </div>
      </header>
      <main className="app-main">
        <div className="left-column">
          <UploadPanel onUploadSuccess={handleUploadSuccess} onUploadError={handleUploadError} />
          {documentContext && (
            <div className="doc-clear-bar">
              <span>📄 Document loaded: <strong>{documentName}</strong></span>
              <button className="btn-text" onClick={handleClearDocument}>✕ Remove</button>
            </div>
          )}
          <QuestionInput
            documentContext={documentContext}
            documentName={documentName}
            onResult={handleResult}
            onError={handleError}
          />
        </div>
        <div className="right-column">
          <ResponseDisplay results={results} error={error} />
        </div>
      </main>
      <footer className="app-footer">
        <p>AT&S AI Enablement Starter Kit &bull; Corporate IT &bull; <span className="footer-version">v1.0.0</span></p>
      </footer>
    </div>
  );
}
