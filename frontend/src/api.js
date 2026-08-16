import axios from "axios";

const BASE_URL = process.env.REACT_APP_API_URL || "http://localhost:8000";

const api = axios.create({
  baseURL: BASE_URL,
  timeout: 30000,
});

export const uploadDocument = async (file) => {
  const formData = new FormData();
  formData.append("file", file);
  const response = await api.post("/upload", formData, {
    headers: { "Content-Type": "multipart/form-data" },
  });
  return response.data;
};

export const askQuestion = async (question, documentContext = null) => {
  const response = await api.post("/ask", {
    question,
    document_context: documentContext,
  });
  return response.data;
};

export const summariseDocument = async (documentText, length = "medium") => {
  const response = await api.post("/summarise", {
    document_text: documentText,
    summary_length: length,
  });
  return response.data;
};

export const checkHealth = async () => {
  const response = await api.get("/health");
  return response.data;
};
