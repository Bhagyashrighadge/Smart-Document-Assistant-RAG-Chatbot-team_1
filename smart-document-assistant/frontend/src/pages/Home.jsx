import React from 'react';
import { useTheme } from '../context/ThemeContext';

const Home = ({ onStartChat }) => {
  const { isDark } = useTheme();

  return (
    <div className={`min-h-screen transition-colors duration-300 ${isDark ? 'dark bg-slate-900' : 'bg-white'}`}>
      {/* Hero Section */}
      <section className={`relative overflow-hidden py-20 sm:py-32 ${isDark ? 'bg-gradient-to-br from-slate-900 via-slate-800 to-slate-900' : 'bg-gradient-to-br from-white via-primary-50 to-accent-50'}`}>
        <div className="absolute inset-0 bg-gradient-subtle dark:bg-gradient-dark-subtle opacity-40"></div>
        <div className="relative max-w-6xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="grid lg:grid-cols-2 gap-12 items-center">
            <div className="space-y-6 animate-fade-in">
              <div className="inline-block">
                <span className={`inline-block px-4 py-2 rounded-full text-sm font-semibold ${isDark ? 'bg-primary-900/50 text-primary-200 border border-primary-700' : 'bg-primary-100 text-primary-700 border border-primary-200'}`}>
                  🚀 Smart Document Intelligence
                </span>
              </div>
              <h1 className={`text-5xl sm:text-6xl font-bold tracking-tight ${isDark ? 'text-white' : 'text-slate-900'}`}>
                AskDocAI
              </h1>
              <p className={`text-xl leading-relaxed ${isDark ? 'text-slate-300' : 'text-slate-600'}`}>
                Upload PDF documents and unlock instant intelligent insights. Ask questions, get precise answers, and master your documents faster with AI-powered assistance.
              </p>
              <div className="flex flex-col sm:flex-row gap-4 pt-4">
                <button
                  onClick={onStartChat}
                  className={`px-8 py-4 rounded-lg font-semibold text-lg transition-all duration-200 transform hover:scale-105 ${isDark ? 'bg-primary-600 hover:bg-primary-700 text-white shadow-lg hover:shadow-primary-500/20' : 'bg-primary-600 hover:bg-primary-700 text-white shadow-md hover:shadow-primary-500/30'}`}
                >
                  Start Now
                </button>
                <button
                  className={`px-8 py-4 rounded-lg font-semibold text-lg transition-all duration-200 border-2 ${isDark ? 'border-primary-500 text-primary-400 hover:bg-primary-500/10' : 'border-primary-600 text-primary-600 hover:bg-primary-50'}`}
                >
                  Learn More
                </button>
              </div>
              <div className={`pt-4 text-sm ${isDark ? 'text-slate-400' : 'text-slate-500'}`}>
                ✓ Upload any PDF • ✓ Instant Answers • ✓ Multiple Languages
              </div>
            </div>
            
            {/* Illustration placeholder */}
            <div className={`relative h-80 sm:h-96 rounded-2xl overflow-hidden ${isDark ? 'bg-gradient-to-br from-primary-900/30 to-accent-900/30 border border-slate-700' : 'bg-gradient-to-br from-primary-100 to-accent-100 border border-slate-200'}`}>
              <div className="absolute inset-0 flex items-center justify-center">
                <div className="text-center">
                  <div className="text-6xl mb-4">📄</div>
                  <div className={`text-sm font-semibold ${isDark ? 'text-primary-300' : 'text-primary-600'}`}>
                    PDF Intelligence Hub
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section className={`py-20 sm:py-32 ${isDark ? 'bg-slate-800/50' : 'bg-slate-50'}`}>
        <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-16">
            <h2 className={`text-4xl font-bold mb-4 ${isDark ? 'text-white' : 'text-slate-900'}`}>
              Powerful Features
            </h2>
            <p className={`text-xl max-w-2xl mx-auto ${isDark ? 'text-slate-300' : 'text-slate-600'}`}>
              Everything you need to extract maximum value from your PDF documents
            </p>
          </div>

          <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-8">
            {[
              {
                icon: '❓',
                title: 'Ask Questions',
                description: 'Query your documents in natural language and get accurate, contextual answers instantly.'
              },
              {
                icon: '📊',
                title: 'Smart Summaries',
                description: 'Get concise summaries of lengthy documents to save time and extract key insights.'
              },
              {
                icon: '🎯',
                title: 'Topic Guidance',
                description: 'Navigate complex topics with intelligent guidance directly from your document.'
              },
              {
                icon: '🌍',
                title: 'Multilingual Support',
                description: 'Read and query documents in English, Hindi, and Marathi—your choice.'
              },
              {
                icon: '⚡',
                title: 'Lightning Fast',
                description: 'Powered by advanced AI and semantic search for instant retrieval of information.'
              },
              {
                icon: '✓',
                title: 'Accurate Answers',
                description: 'Intelligent processing ensures responses are precise and relevant to your queries.'
              }
            ].map((feature, idx) => (
              <div key={idx} className={`p-8 rounded-xl transition-all duration-300 transform hover:scale-105 ${isDark ? 'bg-slate-700/50 border border-slate-600 hover:border-primary-500/50 hover:shadow-xl hover:shadow-primary-500/10' : 'bg-white border border-slate-200 hover:border-primary-300 hover:shadow-xl hover:shadow-primary-500/10'}`}>
                <div className="text-4xl mb-4">{feature.icon}</div>
                <h3 className={`text-lg font-bold mb-2 ${isDark ? 'text-white' : 'text-slate-900'}`}>
                  {feature.title}
                </h3>
                <p className={isDark ? 'text-slate-300' : 'text-slate-600'}>
                  {feature.description}
                </p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* How It Works Section */}
      <section className={`py-20 sm:py-32 ${isDark ? 'bg-slate-800' : 'bg-white'}`}>
        <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-16">
            <h2 className={`text-4xl font-bold mb-4 ${isDark ? 'text-white' : 'text-slate-900'}`}>
              How It Works
            </h2>
            <p className={`text-xl max-w-2xl mx-auto ${isDark ? 'text-slate-300' : 'text-slate-600'}`}>
              Four simple steps to unlock your document's potential
            </p>
          </div>

          <div className="grid md:grid-cols-4 gap-8">
            {[
              { step: '1', title: 'Upload PDF', desc: 'Select and upload your PDF document in seconds' },
              { step: '2', title: 'Ask Questions', desc: 'Pose any question about your document naturally' },
              { step: '3', title: 'Get Answers', desc: 'Receive intelligent, context-aware responses' },
              { step: '4', title: 'Learn Faster', desc: 'Master content in minutes instead of hours' }
            ].map((item, idx) => (
              <div key={idx} className="relative">
                <div className={`flex flex-col items-center text-center ${isDark ? 'text-slate-100' : 'text-slate-900'}`}>
                  <div className={`w-16 h-16 rounded-full flex items-center justify-center font-bold text-xl mb-6 ${isDark ? 'bg-primary-600 text-white' : 'bg-primary-600 text-white'}`}>
                    {item.step}
                  </div>
                  <h3 className="font-bold text-lg mb-2">{item.title}</h3>
                  <p className={isDark ? 'text-slate-400' : 'text-slate-600'}>{item.desc}</p>
                </div>
                {idx < 3 && (
                  <div className={`hidden md:block absolute top-8 right-0 transform translate-x-1/2 ${isDark ? 'text-slate-600' : 'text-slate-300'}`}>
                    →
                  </div>
                )}
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Benefits Section */}
      <section className={`py-20 sm:py-32 ${isDark ? 'bg-gradient-to-br from-slate-800 to-slate-900 bg-slate-800/50' : 'bg-gradient-to-br from-primary-50 to-accent-50'}`}>
        <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-16">
            <h2 className={`text-4xl font-bold mb-4 ${isDark ? 'text-white' : 'text-slate-900'}`}>
              Built for Everyone
            </h2>
            <p className={`text-xl max-w-2xl mx-auto ${isDark ? 'text-slate-300' : 'text-slate-600'}`}>
              Designed to empower students, professionals, researchers, and business leaders
            </p>
          </div>

          <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-6">
            {[
              { icon: '🎓', role: 'Students', benefit: 'Study smarter with instant document comprehension' },
              { icon: '💼', role: 'Professionals', benefit: 'Boost productivity and document processing efficiency' },
              { icon: '🔬', role: 'Researchers', benefit: 'Navigate complex research materials effortlessly' },
              { icon: '📈', role: 'Business Teams', benefit: 'Accelerate decision-making with document insights' }
            ].map((item, idx) => (
              <div key={idx} className={`p-6 rounded-xl text-center ${isDark ? 'bg-slate-700/50 border border-slate-600' : 'bg-white border border-slate-200'}`}>
                <div className="text-4xl mb-3">{item.icon}</div>
                <h3 className={`font-bold text-lg mb-2 ${isDark ? 'text-white' : 'text-slate-900'}`}>
                  {item.role}
                </h3>
                <p className={isDark ? 'text-slate-400' : 'text-slate-600'}>
                  {item.benefit}
                </p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className={`py-16 sm:py-24 ${isDark ? 'bg-slate-900' : 'bg-slate-900'}`}>
        <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
          <h2 className="text-4xl font-bold text-white mb-4">
            Ready to Master Your Documents?
          </h2>
          <p className="text-xl text-slate-300 mb-8">
            Join thousands of users who are saving hours every week with DocuAssist
          </p>
          <button
            onClick={onStartChat}
            className="px-10 py-4 bg-primary-600 hover:bg-primary-700 text-white font-bold text-lg rounded-lg transition-all duration-200 transform hover:scale-105 shadow-lg hover:shadow-primary-500/30"
          >
            Get Started Now
          </button>
        </div>
      </section>
    </div>
  );
};

export default Home;
