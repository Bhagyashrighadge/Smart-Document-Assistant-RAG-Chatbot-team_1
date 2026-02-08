import axios from 'axios';

const API_BASE_URL = '/api';

const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 60000,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Health check
export const healthCheck = async () => {
  try {
    const response = await api.get('/health');
    return response.data;
  } catch (error) {
    console.error('Health check failed:', error);
    throw error;
  }
};

// Upload PDF
export const uploadPDF = async (file) => {
  try {
    const formData = new FormData();
    formData.append('file', file);
    
    const response = await axios.post(`${API_BASE_URL}/upload-pdf`, formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
    
    return response.data;
  } catch (error) {
    console.error('Upload failed:', error);
    throw error;
  }
};

// Ask question
export const askQuestion = async (sessionId, question, language = 'en') => {
  try {
    const response = await api.post('/ask-question', {
      session_id: sessionId,
      question: question,
      language: language,
    });
    
    return response.data;
  } catch (error) {
    console.error('Question failed:', error);
    
    // Enhanced error handling
    let errorMessage = 'Failed to process question. Please try again.';
    
    if (error.response?.data?.detail) {
      errorMessage = error.response.data.detail;
    } else if (error.response?.data?.message) {
      errorMessage = error.response.data.message;
    } else if (error.message) {
      errorMessage = error.message;
    }
    
    // Create error object with proper structure
    const customError = new Error(errorMessage);
    customError.response = error.response;
    
    throw customError;
  }
};

// Translate text
export const translateText = async (text, targetLanguage) => {
  try {
    const response = await api.post('/translate', {
      text: text,
      target_language: targetLanguage,
    });
    
    return response.data;
  } catch (error) {
    console.error('Translation failed:', error);
    throw error;
  }
};

// Get session info
export const getSessionInfo = async (sessionId) => {
  try {
    const response = await api.get(`/session/${sessionId}`);
    return response.data;
  } catch (error) {
    console.error('Get session info failed:', error);
    throw error;
  }
};

// Delete session
export const deleteSession = async (sessionId) => {
  try {
    const response = await api.delete(`/session/${sessionId}`);
    return response.data;
  } catch (error) {
    console.error('Delete session failed:', error);
    throw error;
  }
};

export default api;
