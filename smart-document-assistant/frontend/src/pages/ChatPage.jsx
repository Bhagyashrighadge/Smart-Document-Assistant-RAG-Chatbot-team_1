import React, { useState } from 'react';
import Upload from '../components/Upload';
import Chat from '../components/Chat';
import { useLanguage } from '../context/LanguageContext';
import { useTheme } from '../context/ThemeContext';

const ChatPage = ({ goHome }) => {
  const { isDark } = useTheme();
  const [sessionId, setSessionId] = useState(null);
  const [documentName, setDocumentName] = useState('');
  const { language, setLanguage } = useLanguage();
  const [isLoading, setIsLoading] = useState(false);

  const handleUploadSuccess = (response) => {
    setSessionId(response.session_id);
    setDocumentName(response.document_name);
  };

  return (
    <div className={`min-h-screen ${isDark ? 'bg-slate-900' : 'bg-slate-50'} py-8 px-4 transition-colors duration-300`}>
      <div className="max-w-4xl mx-auto">
        {!sessionId ? (
          <div>
            <button
              onClick={goHome}
              className={`mb-6 px-6 py-2 rounded-lg font-semibold transition-all duration-200 ${isDark ? 'bg-slate-700 hover:bg-slate-600 text-white' : 'bg-slate-200 hover:bg-slate-300 text-slate-900'}`}
            >
              ← Back to Home
            </button>
            <Upload onUploadSuccess={handleUploadSuccess} isLoading={isLoading} />
          </div>
        ) : (
          <div className="space-y-4">
            <button
              onClick={() => {
                setSessionId(null);
                setDocumentName('');
              }}
              className={`px-6 py-2 rounded-lg font-semibold transition-all duration-200 ${isDark ? 'bg-slate-700 hover:bg-slate-600 text-white' : 'bg-slate-200 hover:bg-slate-300 text-slate-900'}`}
            >
              ← Upload New Document
            </button>
            <div style={{ height: 'calc(100vh - 200px)' }}>
              <Chat
                sessionId={sessionId}
                documentName={documentName}
                currentLanguage={language}
                onLanguageChange={setLanguage}
              />
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default ChatPage;
