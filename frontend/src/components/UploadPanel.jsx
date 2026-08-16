import React, { useCallback, useRef, useState } from "react";
import { uploadDocument } from "../api";

const SUPPORTED_TYPES = [
  "application/pdf",
  "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
  "text/plain",
];

export default function UploadPanel({ onUploadSuccess, onUploadError }) {
  const [isDragging, setIsDragging] = useState(false);
  const [isUploading, setIsUploading] = useState(false);
  const [uploadedFile, setUploadedFile] = useState(null);
  const fileInputRef = useRef(null);

  const handleFile = useCallback(
    async (file) => {
      if (!file) return;
      if (!SUPPORTED_TYPES.includes(file.type)) {
        onUploadError("Unsupported file type. Please upload: .pdf, .docx, .txt");
        return;
      }
      if (file.size > 10 * 1024 * 1024) {
        onUploadError("File too large. Maximum size is 10MB.");
        return;
      }
      setIsUploading(true);
      setUploadedFile(null);
      try {
        const result = await uploadDocument(file);
        setUploadedFile({ name: result.filename, type: result.file_type, chars: result.character_count });
        onUploadSuccess(result.extracted_text, result.filename);
      } catch (err) {
        onUploadError(err.response?.data?.detail || "Upload failed. Please try again.");
      } finally {
        setIsUploading(false);
      }
    },
    [onUploadSuccess, onUploadError]
  );

  const handleDragOver = (e) => { e.preventDefault(); setIsDragging(true); };
  const handleDragLeave = () => setIsDragging(false);
  const handleDrop = (e) => { e.preventDefault(); setIsDragging(false); handleFile(e.dataTransfer.files[0]); };
  const handleInputChange = (e) => { handleFile(e.target.files[0]); e.target.value = ""; };

  return (
    <div className="card">
      <h2 className="card-title"><span className="icon">📄</span> Upload Document</h2>
      <p className="card-subtitle">Upload a PDF, Word, or text file to ask questions about it.</p>
      <div
        className={`drop-zone ${isDragging ? "dragging" : ""} ${isUploading ? "uploading" : ""}`}
        onDragOver={handleDragOver}
        onDragLeave={handleDragLeave}
        onDrop={handleDrop}
        onClick={() => !isUploading && fileInputRef.current?.click()}
        role="button"
        tabIndex={0}
      >
        <input ref={fileInputRef} type="file" accept=".pdf,.docx,.txt" onChange={handleInputChange} style={{ display: "none" }} />
        {isUploading ? (
          <div className="upload-state"><div className="spinner" /><p>Reading your document...</p></div>
        ) : uploadedFile ? (
          <div className="upload-state success">
            <span className="upload-icon">✅</span>
            <p className="upload-filename">{uploadedFile.name}</p>
            <p className="upload-meta">{uploadedFile.type.toUpperCase()} &bull; {uploadedFile.chars.toLocaleString()} characters</p>
            <p className="upload-hint">Click to upload a different document</p>
          </div>
        ) : (
          <div className="upload-state">
            <span className="upload-icon">☁️</span>
            <p className="upload-primary">{isDragging ? "Drop your file here" : "Click or drag a file here"}</p>
            <p className="upload-hint">Supports PDF, DOCX, TXT &bull; Max 10MB</p>
          </div>
        )}
      </div>
    </div>
  );
}
