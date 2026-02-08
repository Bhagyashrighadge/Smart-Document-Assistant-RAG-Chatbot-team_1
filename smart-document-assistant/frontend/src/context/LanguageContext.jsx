import React, { createContext, useState, useContext, useEffect } from 'react';

/**
 * Global Language Context for strict language control across the application
 * 
 * Features:
 * - Persists language selection to localStorage
 * - Restores language on page refresh
 * - Allows components to access and change language globally
 * - Ensures language consistency across all API calls
 */

const LanguageContext = createContext();

export const useLanguage = () => {
  const context = useContext(LanguageContext);
  if (!context) {
    throw new Error('useLanguage must be used within LanguageProvider');
  }
  return context;
};

export const LanguageProvider = ({ children }) => {
  // Initialize language from localStorage or default to 'en'
  const [language, setLanguageState] = useState(() => {
    if (typeof window !== 'undefined') {
      const stored = localStorage.getItem('selectedLanguage');
      return stored || 'en';
    }
    return 'en';
  });

  // Update language and persist to localStorage
  const setLanguage = (newLanguage) => {
    if (!['en', 'hi', 'mr'].includes(newLanguage)) {
      console.error(`Invalid language: ${newLanguage}. Must be one of: en, hi, mr`);
      return;
    }

    setLanguageState(newLanguage);
    
    // Persist to localStorage
    if (typeof window !== 'undefined') {
      localStorage.setItem('selectedLanguage', newLanguage);
      console.log(`[LanguageContext] Language changed to: ${newLanguage}`);
    }
  };

  // Restore language from localStorage on mount
  useEffect(() => {
    if (typeof window !== 'undefined') {
      const stored = localStorage.getItem('selectedLanguage');
      if (stored && ['en', 'hi', 'mr'].includes(stored)) {
        setLanguageState(stored);
        console.log(`[LanguageContext] Restored language from localStorage: ${stored}`);
      }
    }
  }, []);

  const value = {
    language,
    setLanguage,
    // Helper method to get language name
    getLanguageName: () => {
      const names = {
        en: 'English',
        hi: 'हिंदी (Hindi)',
        mr: 'मराठी (Marathi)'
      };
      return names[language] || 'Unknown';
    },
    // Helper method to get language display
    getLanguageDisplay: () => {
      const displays = {
        en: '🇬🇧 EN',
        hi: '🇮🇳 HI',
        mr: '🇮🇳 MR'
      };
      return displays[language] || language.toUpperCase();
    }
  };

  return (
    <LanguageContext.Provider value={value}>
      {children}
    </LanguageContext.Provider>
  );
};
