import React, { useState } from "react";
import { askQuestion, summariseDocument } from "../api";

const SUMMARY_LENGTHS = [
  { value: "short", label: "Short", desc: "3-5 sentences" },
  { value: "medium", label: "Medium", desc: "1-2 paragraphs" },
  { value: "detailed", label: "Detailed", desc: "Full summary" },
];

export default function QuestionInput({ documentContext, documentName, onResult, onError }) {
  const [mode, setMode] = useState("ask");
  const [question, setQuestion] = useState("");
  const [summaryLength, setSummaryLength] = useState("medium");
  const [isLoading, setIsLoading] = useState(false);

  const handleAsk = async () => {
    if (!question.trim()) { onError("Please enter a question."); return; }
    setIsLoading(true);
    try {
      const result = await askQuestion(question.trim(), documentContext);
      onResult({ type: "answer", question: result.question, content: result.answer, hasContext: result.has_document_context, documentName });
      setQuestion("");
    } catch (err) {
      onError(err.response?.data?.detail || "Could not get an answer. Please try again.");
    } finally {
      setIsLoading(false);
    }
  };

  const handleSummarise = async () => {
    if (!documentContext) { onError("Please upload a document first."); return; }
    setIsLoading(true);
    try {
      const result = await summariseDocument(documentContext, summaryLength);
      onResult({ type: "summary", content: result.summary, documentName, summaryLength, originalLength: result.original_length });
    } catch (err) {
      onError(err.response?.data?.detail || "Could not summarise. Please try again.");
    } finally {
      setIsLoading(false);
    }
  };

  const handleKeyDown = (e) => {
    if (e.key === "Enter" && !e.shiftKey && mode === "ask") { e.preventDefault(); handleAsk(); }
  };

  return (
    <div className="card">
      <h2 className="card-title"><span className="icon">💬</span> Ask or Summarise</h2>
      {documentContext ? (
        <div className="context-badge"><span>📄</span> Using: <strong>{documentName}</strong></div>
      ) : (
        <div className="context-badge no-context"><span>💡</span> No document — asking general questions</div>
      )}
      <div className="mode-toggle" role="tablist">
        <button role="tab" className={`mode-btn ${mode === "ask" ? "active" : ""}`} onClick={() => setMode("ask")}>❓ Ask a Question</button>
        <button role="tab" className={`mode-btn ${mode === "summarise" ? "active" : ""}`} onClick={() => setMode("summarise")} disabled={!documentContext}>📝 Summarise</button>
      </div>
      {mode === "ask" && (
        <div className="input-group">
          <textarea className="question-input" value={question} onChange={(e) => setQuestion(e.target.value)} onKeyDown={handleKeyDown}
            placeholder={documentContext ? "Ask anything about your document..." : "Ask any question..."} rows={3} disabled={isLoading} />
          <button className="btn-primary" onClick={handleAsk} disabled={isLoading || !question.trim()}>
            {isLoading ? <><div className="spinner-sm" /> Thinking...</> : "Ask →"}
          </button>
        </div>
      )}
      {mode === "summarise" && (
        <div className="input-group">
          <p className="summarise-label">Choose summary length:</p>
          <div className="length-options">
            {SUMMARY_LENGTHS.map((opt) => (
              <label key={opt.value} className={`length-option ${summaryLength === opt.value ? "selected" : ""}`}>
                <input type="radio" name="summaryLength" value={opt.value} checked={summaryLength === opt.value} onChange={() => setSummaryLength(opt.value)} style={{ display: "none" }} />
                <span className="length-label">{opt.label}</span>
                <span className="length-desc">{opt.desc}</span>
              </label>
            ))}
          </div>
          <button className="btn-primary" onClick={handleSummarise} disabled={isLoading}>
            {isLoading ? <><div className="spinner-sm" /> Summarising...</> : "Summarise →"}
          </button>
        </div>
      )}
    </div>
  );
}
