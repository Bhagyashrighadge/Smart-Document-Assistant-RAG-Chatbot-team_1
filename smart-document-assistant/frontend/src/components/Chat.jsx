import React, { useState, useRef, useEffect } from 'react';
import { useTheme } from '../context/ThemeContext';
import { askQuestion } from '../services/api';

const Chat = ({ sessionId, documentName, currentLanguage, onLanguageChange }) => {
  const { isDark } = useTheme();
  const [messages, setMessages] = useState(() => [
    {
      id: 1,
      role: 'assistant',
      content: `Welcome! I'm here to help you understand "${documentName}". Feel free to ask me any questions about the document.`,
      timestamp: new Date(),
    },
  ]);
  const [inputValue, setInputValue] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState('');
  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleSendMessage = async () => {
    if (!inputValue.trim() || isLoading) return;

    console.log(`[Chat] Sending question with language: ${currentLanguage}`);

    const userMessage = {
      id: Date.now(),
      role: 'user',
      content: inputValue,
      timestamp: new Date(),
    };

    setMessages((prev) => [...prev, userMessage]);
    setInputValue('');
    setIsLoading(true);
    setError('');

    try {
      console.log('Sending question:', inputValue);
      console.log('Language selected:', currentLanguage);
      const response = await askQuestion(sessionId, inputValue, currentLanguage);

      if (response.success) {
        console.log(`[Chat] Response received in language: ${response.language}`);
        
        if (response.language !== currentLanguage) {
          console.warn(`[Chat] Language mismatch - requested ${currentLanguage}, got ${response.language}`);
        }
        
        const assistantMessage = {
          id: Date.now() + 1,
          role: 'assistant',
          content: response.answer,
          timestamp: new Date(),
          originalAnswer: response.original_answer,
          language: response.language,
        };
        setMessages((prev) => [...prev, assistantMessage]);
      } else {
        const errorMessage = response.message || 'Failed to get response';
        console.error('Error response:', errorMessage);
        setError(errorMessage);
      }
    } catch (error) {
      let errorMessage = 'Failed to process question. Please try again.';
      
      if (error.message) {
        errorMessage = error.message;
      } else if (error.response?.data?.detail) {
        errorMessage = error.response.data.detail;
      } else if (error.response?.data?.message) {
        errorMessage = error.response.data.message;
      }
      
      console.error('Full error:', error);
      console.error('Error message:', errorMessage);
      setError(errorMessage);
    } finally {
      setIsLoading(false);
    }
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSendMessage();
    }
  };

  return (
    <div className={`flex flex-col h-full rounded-xl overflow-hidden ${isDark ? 'bg-slate-800 border border-slate-700' : 'bg-white border border-slate-200'}`}>
      {/* Header */}
      <div className={`${isDark ? 'bg-gradient-to-r from-primary-700 to-primary-600 border-b border-primary-600' : 'bg-gradient-to-r from-primary-600 to-primary-700 border-b border-primary-700'} text-white p-6 shadow-md`}>
        <div className="flex justify-between items-start">
          <div>
            <h2 className="text-2xl font-bold mb-2">Chat with Document</h2>
            <p className="text-primary-100">📄 {documentName}</p>
          </div>
        </div>

        {/* Language Selector */}
        <div className="mt-4 flex gap-2 flex-wrap">
          <span className="text-sm text-primary-100">Language:</span>
          {['en', 'hi', 'mr'].map((lang) => {
            const langNames = { en: '🇬🇧 EN', hi: '🇮🇳 HI', mr: '🇮🇳 MR' };
            return (
              <button
                key={lang}
                onClick={() => onLanguageChange(lang)}
                className={`px-3 py-1 rounded text-sm font-medium transition-all duration-200 ${
                  currentLanguage === lang
                    ? `${isDark ? 'bg-white text-primary-700' : 'bg-white text-primary-700'}`
                    : `${isDark ? 'bg-primary-500/50 text-white hover:bg-primary-400/50' : 'bg-primary-500 text-white hover:bg-primary-400'}`
                }`}
              >
                {langNames[lang]}
              </button>
            );
          })}
        </div>
      </div>

      {/* Messages Area */}
      <div className={`flex-1 overflow-y-auto p-6 space-y-4 ${isDark ? 'bg-slate-800/50' : 'bg-slate-50'}`}>
        {messages.map((message) => (
          <div
            key={message.id}
            className={`flex ${message.role === 'user' ? 'justify-end' : 'justify-start'} animate-slide-up`}
          >
            <div
              className={`max-w-xs lg:max-w-md px-4 py-3 rounded-lg ${
                message.role === 'user'
                  ? `${isDark ? 'bg-primary-600 text-white rounded-br-none' : 'bg-primary-600 text-white rounded-br-none'}`
                  : `${isDark ? 'bg-slate-700 text-slate-100 border border-slate-600 rounded-bl-none' : 'bg-white text-slate-900 border border-slate-200 rounded-bl-none'}`
              }`}
            >
              <p className="text-sm whitespace-pre-wrap break-words">{message.content}</p>
              <p
                className={`text-xs mt-2 ${
                  message.role === 'user'
                    ? isDark ? 'text-primary-200' : 'text-primary-100'
                    : isDark ? 'text-slate-400' : 'text-slate-500'
                }`}
              >
                {message.timestamp.toLocaleTimeString([], {
                  hour: '2-digit',
                  minute: '2-digit',
                })}
              </p>
            </div>
          </div>
        ))}

        {isLoading && (
          <div className="flex justify-start animate-slide-up">
            <div className={`${isDark ? 'bg-slate-700 text-slate-100 border border-slate-600' : 'bg-white text-slate-900 border border-slate-200'} px-4 py-3 rounded-lg rounded-bl-none`}>
              <div className="flex gap-2 items-center">
                <span className="animate-spin">⏳</span>
                <span className="text-sm">Processing your question...</span>
              </div>
            </div>
          </div>
        )}

        {error && (
          <div className={`${isDark ? 'bg-red-900/30 border border-red-700/50 text-red-300' : 'bg-red-50 border border-red-200 text-red-700'} px-4 py-3 rounded-lg text-sm`}>
            ⚠️ {error}
          </div>
        )}

        <div ref={messagesEndRef} />
      </div>

      {/* Input Area */}
      <div className={`border-t ${isDark ? 'border-slate-700 bg-slate-800' : 'border-slate-200 bg-white'} p-6`}>
        <div className="flex gap-2">
          <textarea
            value={inputValue}
            onChange={(e) => setInputValue(e.target.value)}
            onKeyPress={handleKeyPress}
            placeholder="Ask a question about the document..."
            disabled={isLoading}
            rows="2"
            className={`flex-1 px-4 py-3 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary-500 resize-none transition-all duration-200 ${
              isDark
                ? 'bg-slate-700 border border-slate-600 text-white placeholder-slate-400 disabled:bg-slate-700 disabled:opacity-50'
                : 'bg-slate-50 border border-slate-300 text-slate-900 placeholder-slate-500 disabled:bg-slate-100'
            }`}
          />
          <button
            onClick={handleSendMessage}
            disabled={!inputValue.trim() || isLoading}
            className={`px-6 py-3 rounded-lg font-semibold transition-all duration-200 transform ${
              inputValue.trim() && !isLoading
                ? `${isDark ? 'bg-primary-600 hover:bg-primary-700 text-white shadow-lg hover:scale-105' : 'bg-primary-600 hover:bg-primary-700 text-white shadow-md hover:scale-105'} cursor-pointer`
                : `${isDark ? 'bg-slate-700 text-slate-400' : 'bg-slate-200 text-slate-400'} cursor-not-allowed`
            }`}
          >
            {isLoading ? '⏳' : '📤'}
          </button>
        </div>
      </div>
    </div>
  );
};

export default Chat;
