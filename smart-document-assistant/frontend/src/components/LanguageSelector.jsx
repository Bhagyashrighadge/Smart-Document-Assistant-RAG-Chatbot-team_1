import React from 'react';

const LanguageSelector = ({ currentLanguage, onLanguageChange }) => {
  const languages = [
    { code: 'en', name: 'English', flag: '🇬🇧' },
    { code: 'hi', name: 'हिंदी', flag: '🇮🇳' },
    { code: 'mr', name: 'मराठी', flag: '🇮🇳' },
  ];

  return (
    <div className="flex gap-2 items-center">
      <span className="text-sm font-medium text-gray-700">Language:</span>
      <div className="flex gap-2">
        {languages.map((lang) => (
          <button
            key={lang.code}
            onClick={() => onLanguageChange(lang.code)}
            className={`px-3 py-2 rounded-lg text-sm font-medium transition ${
              currentLanguage === lang.code
                ? 'bg-indigo-600 text-white'
                : 'bg-gray-200 text-gray-800 hover:bg-gray-300'
            }`}
            title={lang.name}
          >
            {lang.flag} {lang.name}
          </button>
        ))}
      </div>
    </div>
  );
};

export default LanguageSelector;
