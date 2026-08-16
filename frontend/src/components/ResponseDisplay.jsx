import React, { useEffect, useRef } from "react";

export default function ResponseDisplay({ results, error }) {
  const bottomRef = useRef(null);

  useEffect(() => {
    if (results.length > 0) bottomRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [results]);

  return (
    <div className="card response-card">
      <h2 className="card-title"><span className="icon">🤖</span> AI Response</h2>
      {error && (
        <div className="error-banner" role="alert"><span>⚠️</span> {error}</div>
      )}
      {results.length === 0 && !error && (
        <div className="empty-state">
          <div className="empty-icon">💡</div>
          <p className="empty-title">Ready to help</p>
          <p className="empty-subtitle">Upload a document and ask a question, or just ask anything directly.</p>
          <div className="empty-examples">
            <p className="examples-label">Try asking:</p>
            <ul>
              <li>"What are the main points of this document?"</li>
              <li>"Summarise this report for my manager"</li>
              <li>"What does AT&S do?"</li>
              <li>"List all action items mentioned"</li>
            </ul>
          </div>
        </div>
      )}
      <div className="results-list">
        {results.map((result, index) => (
          <div key={index} className={`result-item ${result.type}`}>
            <div className="result-header">
              <span className="result-type-badge">{result.type === "answer" ? "❓ Answer" : "📝 Summary"}</span>
              {result.documentName && <span className="result-doc-name">📄 {result.documentName}</span>}
              {result.type === "summary" && result.summaryLength && (
                <span className="result-length-badge">{result.summaryLength} summary</span>
              )}
            </div>
            {result.type === "answer" && result.question && (
              <div className="result-question"><strong>Q:</strong> {result.question}</div>
            )}
            <div className="result-content">
              {result.content.split("\n").map((line, i) => line.trim() ? <p key={i}>{line}</p> : <br key={i} />)}
            </div>
            <button className="copy-btn" onClick={() => navigator.clipboard.writeText(result.content)}>📋 Copy</button>
          </div>
        ))}
        <div ref={bottomRef} />
      </div>
    </div>
  );
}
