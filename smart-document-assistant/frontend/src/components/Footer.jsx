import React from 'react';
import { useTheme } from '../context/ThemeContext';

const Footer = () => {
  const { isDark } = useTheme();

  return (
    <footer className={`transition-colors duration-300 ${isDark ? 'bg-slate-900 border-t border-slate-700' : 'bg-slate-50 border-t border-slate-200'} mt-auto`}>
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        <div className="grid md:grid-cols-4 gap-8 mb-8">
          {/* Brand */}
          <div>
            <div className="flex items-center gap-2 mb-4">
              <div className={`w-8 h-8 rounded-lg flex items-center justify-center font-bold text-sm ${isDark ? 'bg-primary-600 text-white' : 'bg-primary-600 text-white'}`}>
                📄
              </div>
              <span className={`font-bold text-lg ${isDark ? 'text-white' : 'text-slate-900'}`}>
                AskDocAI
              </span>
            </div>
            <p className={`text-sm ${isDark ? 'text-slate-400' : 'text-slate-600'}`}>
              Intelligent PDF document assistance powered by AI
            </p>
          </div>

          {/* Product */}
          <div>
            <h3 className={`font-semibold mb-4 ${isDark ? 'text-white' : 'text-slate-900'}`}>
              Product
            </h3>
            <ul className={`space-y-2 text-sm ${isDark ? 'text-slate-400' : 'text-slate-600'}`}>
              <li><a href="#" className={`transition-colors ${isDark ? 'hover:text-slate-200' : 'hover:text-slate-900'}`}>Features</a></li>
              <li><a href="#" className={`transition-colors ${isDark ? 'hover:text-slate-200' : 'hover:text-slate-900'}`}>Pricing</a></li>
              <li><a href="#" className={`transition-colors ${isDark ? 'hover:text-slate-200' : 'hover:text-slate-900'}`}>FAQ</a></li>
              <li><a href="#" className={`transition-colors ${isDark ? 'hover:text-slate-200' : 'hover:text-slate-900'}`}>Updates</a></li>
            </ul>
          </div>

          {/* Company */}
          <div>
            <h3 className={`font-semibold mb-4 ${isDark ? 'text-white' : 'text-slate-900'}`}>
              Company
            </h3>
            <ul className={`space-y-2 text-sm ${isDark ? 'text-slate-400' : 'text-slate-600'}`}>
              <li><a href="#" className={`transition-colors ${isDark ? 'hover:text-slate-200' : 'hover:text-slate-900'}`}>About Us</a></li>
              <li><a href="#" className={`transition-colors ${isDark ? 'hover:text-slate-200' : 'hover:text-slate-900'}`}>Blog</a></li>
              <li><a href="#" className={`transition-colors ${isDark ? 'hover:text-slate-200' : 'hover:text-slate-900'}`}>Contact</a></li>
              <li><a href="#" className={`transition-colors ${isDark ? 'hover:text-slate-200' : 'hover:text-slate-900'}`}>Careers</a></li>
            </ul>
          </div>

          {/* Legal */}
          <div>
            <h3 className={`font-semibold mb-4 ${isDark ? 'text-white' : 'text-slate-900'}`}>
              Legal
            </h3>
            <ul className={`space-y-2 text-sm ${isDark ? 'text-slate-400' : 'text-slate-600'}`}>
              <li><a href="#" className={`transition-colors ${isDark ? 'hover:text-slate-200' : 'hover:text-slate-900'}`}>Privacy</a></li>
              <li><a href="#" className={`transition-colors ${isDark ? 'hover:text-slate-200' : 'hover:text-slate-900'}`}>Terms</a></li>
              <li><a href="#" className={`transition-colors ${isDark ? 'hover:text-slate-200' : 'hover:text-slate-900'}`}>Security</a></li>
              <li><a href="#" className={`transition-colors ${isDark ? 'hover:text-slate-200' : 'hover:text-slate-900'}`}>GDPR</a></li>
            </ul>
          </div>
        </div>

        <div className={`border-t ${isDark ? 'border-slate-700' : 'border-slate-200'} pt-8`}>
          <div className="flex flex-col sm:flex-row justify-between items-center gap-4">
            <p className={`text-sm ${isDark ? 'text-slate-500' : 'text-slate-600'}`}>
              © 2026 AskDocAI. All rights reserved. Powered by advanced AI and RAG technology.
            </p>
            <div className="flex gap-4">
              <a href="#" className={`text-sm transition-colors ${isDark ? 'text-slate-500 hover:text-slate-300' : 'text-slate-600 hover:text-slate-900'}`}>
                Twitter
              </a>
              <a href="#" className={`text-sm transition-colors ${isDark ? 'text-slate-500 hover:text-slate-300' : 'text-slate-600 hover:text-slate-900'}`}>
                GitHub
              </a>
              <a href="#" className={`text-sm transition-colors ${isDark ? 'text-slate-500 hover:text-slate-300' : 'text-slate-600 hover:text-slate-900'}`}>
                Discord
              </a>
            </div>
          </div>
        </div>
      </div>
    </footer>
  );
};

export default Footer;
