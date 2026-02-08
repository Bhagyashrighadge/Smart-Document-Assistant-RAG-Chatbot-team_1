import React, { useState } from 'react';
import Navbar from './components/Navbar';
import Footer from './components/Footer';
import Home from './pages/Home';
import ChatPage from './pages/ChatPage';
import { LanguageProvider } from './context/LanguageContext';
import { ThemeProvider, useTheme } from './context/ThemeContext';
import './index.css';

function AppContent() {
  const [currentPage, setCurrentPage] = useState('home');
  const { isDark } = useTheme();

  const goToChat = () => setCurrentPage('chat');
  const goToHome = () => setCurrentPage('home');

  return (
    <div className={`flex flex-col min-h-screen transition-colors duration-300 ${isDark ? 'dark bg-slate-900' : 'bg-white'}`}>
      <Navbar />
      
      <main className="flex-1">
        {currentPage === 'home' ? (
          <Home onStartChat={goToChat} />
        ) : (
          <ChatPage goHome={goToHome} />
        )}
      </main>

      <Footer />
    </div>
  );
}

function App() {
  return (
    <ThemeProvider>
      <LanguageProvider>
        <AppContent />
      </LanguageProvider>
    </ThemeProvider>
  );
}

export default App;
