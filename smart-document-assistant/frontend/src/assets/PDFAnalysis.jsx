import React from 'react';

const PDFAnalysisIllustration = ({ isDark }) => {
  return (
    <svg viewBox="0 0 400 300" xmlns="http://www.w3.org/2000/svg" className="w-full h-full">
      {/* Monitor Base */}
      <rect x="120" y="220" width="160" height="12" fill={isDark ? '#4b5563' : '#9ca3af'} rx="2"/>
      <rect x="180" y="232" width="40" height="16" fill={isDark ? '#4b5563' : '#9ca3af'} rx="2"/>
      
      {/* Monitor Screen */}
      <rect x="80" y="40" width="240" height="180" fill={isDark ? '#60a5fa' : '#93c5fd'} rx="8"/>
      <rect x="85" y="45" width="230" height="170" fill={isDark ? '#3b82f6' : '#bfdbfe'} rx="6"/>
      
      {/* Monitor Top Bar */}
      <rect x="85" y="45" width="230" height="25" fill={isDark ? '#1e40af' : '#1e3a8a'} rx="6"/>
      <circle cx="95" cy="57" r="3" fill={isDark ? '#60a5fa' : '#93c5fd'}/>
      <circle cx="105" cy="57" r="3" fill={isDark ? '#60a5fa' : '#93c5fd'}/>
      <circle cx="115" cy="57" r="3" fill={isDark ? '#60a5fa' : '#93c5fd'}/>
      
      {/* PDF Document on Screen - Left Side */}
      <g>
        {/* PDF Icon */}
        <rect x="100" y="85" width="50" height="65" fill="#f5f5f5" stroke={isDark ? '#4b5563' : '#d1d5db'} strokeWidth="2" rx="2"/>
        <text x="125" y="125" textAnchor="middle" fill="#dc2626" fontSize="24" fontWeight="bold">PDF</text>
        
        {/* Lines representing text */}
        <line x1="105" y1="140" x2="145" y2="140" stroke={isDark ? '#9ca3af' : '#d1d5db'} strokeWidth="2"/>
        <line x1="105" y1="145" x2="145" y2="145" stroke={isDark ? '#9ca3af' : '#d1d5db'} strokeWidth="1"/>
      </g>
      
      {/* Main PDF Document on Screen - Center */}
      <g>
        <rect x="170" y="70" width="95" height="120" fill="white" stroke={isDark ? '#4b5563' : '#9ca3af'} strokeWidth="2" rx="3"/>
        
        {/* Document Header */}
        <rect x="170" y="70" width="95" height="15" fill={isDark ? '#374151' : '#e5e7eb'} rx="2"/>
        
        {/* Document Lines */}
        <line x1="180" y1="92" x2="255" y2="92" stroke={isDark ? '#9ca3af' : '#d1d5db'} strokeWidth="1.5"/>
        <line x1="180" y1="100" x2="255" y2="100" stroke={isDark ? '#9ca3af' : '#d1d5db'} strokeWidth="1"/>
        <line x1="180" y1="107" x2="255" y2="107" stroke={isDark ? '#9ca3af' : '#d1d5db'} strokeWidth="1"/>
        <line x1="180" y1="114" x2="240" y2="114" stroke={isDark ? '#9ca3af' : '#d1d5db'} strokeWidth="1"/>
        
        {/* Magnifying glass on document */}
        <circle cx="250" cy="130" r="22" fill="none" stroke="#fbbf24" strokeWidth="3"/>
        <line x1="268" y1="148" x2="285" y2="165" stroke="#fbbf24" strokeWidth="3" strokeLinecap="round"/>
      </g>
      
      {/* Floating Documents around monitor */}
      {/* Top Right Document */}
      <g transform="translate(300, 20)">
        <rect x="0" y="0" width="45" height="60" fill="#f5f5f5" stroke={isDark ? '#4b5563' : '#9ca3af'} strokeWidth="1.5" rx="2"/>
        <line x1="5" y1="45" x2="40" y2="45" stroke={isDark ? '#9ca3af' : '#d1d5db'} strokeWidth="1"/>
        <line x1="5" y1="50" x2="40" y2="50" stroke={isDark ? '#9ca3af' : '#d1d5db'} strokeWidth="1"/>
        <line x1="5" y1="55" x2="35" y2="55" stroke={isDark ? '#9ca3af' : '#d1d5db'} strokeWidth="1"/>
      </g>
      
      {/* Bottom Right Document */}
      <g transform="translate(310, 220)">
        <rect x="0" y="0" width="50" height="65" fill="#f5f5f5" stroke={isDark ? '#4b5563' : '#9ca3af'} strokeWidth="1.5" rx="2"/>
        <line x1="5" y1="48" x2="45" y2="48" stroke={isDark ? '#9ca3af' : '#d1d5db'} strokeWidth="1"/>
        <line x1="5" y1="53" x2="45" y2="53" stroke={isDark ? '#9ca3af' : '#d1d5db'} strokeWidth="1"/>
        <line x1="5" y1="58" x2="40" y2="58" stroke={isDark ? '#9ca3af' : '#d1d5db'} strokeWidth="1"/>
      </g>
      
      {/* Top Left Gear/Settings Icon */}
      <g transform="translate(55, 35)">
        <circle cx="0" cy="0" r="12" fill="none" stroke={isDark ? '#9ca3af' : '#9ca3af'} strokeWidth="2"/>
        
        {/* Gear teeth */}
        <line x1="0" y1="-14" x2="0" y2="-18" stroke={isDark ? '#9ca3af' : '#9ca3af'} strokeWidth="2"/>
        <line x1="10" y1="-10" x2="13" y2="-13" stroke={isDark ? '#9ca3af' : '#9ca3af'} strokeWidth="2"/>
        <line x1="14" y1="0" x2="18" y2="0" stroke={isDark ? '#9ca3af' : '#9ca3af'} strokeWidth="2"/>
        <line x1="10" y1="10" x2="13" y2="13" stroke={isDark ? '#9ca3af' : '#9ca3af'} strokeWidth="2"/>
        <line x1="0" y1="14" x2="0" y2="18" stroke={isDark ? '#9ca3af' : '#9ca3af'} strokeWidth="2"/>
        <line x1="-10" y1="10" x2="-13" y2="13" stroke={isDark ? '#9ca3af' : '#9ca3af'} strokeWidth="2"/>
        <line x1="-14" y1="0" x2="-18" y2="0" stroke={isDark ? '#9ca3af' : '#9ca3af'} strokeWidth="2"/>
        <line x1="-10" y1="-10" x2="-13" y2="-13" stroke={isDark ? '#9ca3af' : '#9ca3af'} strokeWidth="2"/>
        
        {/* Center circle */}
        <circle cx="0" cy="0" r="4" fill={isDark ? '#4b5563' : '#9ca3af'}/>
      </g>
      
      {/* Chart/Analytics Icon */}
      <g transform="translate(340, 60)">
        <rect x="-18" y="-8" width="36" height="20" fill="none" stroke={isDark ? '#9ca3af' : '#9ca3af'} strokeWidth="2" rx="2"/>
        {/* Bar chart */}
        <line x1="-12" y1="4" x2="-12" y2="-4" stroke="#3b82f6" strokeWidth="3" strokeLinecap="round"/>
        <line x1="-4" y1="4" x2="-4" y2="-2" stroke="#60a5fa" strokeWidth="3" strokeLinecap="round"/>
        <line x1="4" y1="4" x2="4" y2="0" stroke="#93c5fd" strokeWidth="3" strokeLinecap="round"/>
        <line x1="12" y1="4" x2="12" y2="-6" stroke="#3b82f6" strokeWidth="3" strokeLinecap="round"/>
      </g>
      
      {/* Keyboard */}
      <ellipse cx="200" cy="260" rx="100" ry="15" fill={isDark ? '#4b5563' : '#9ca3af'} opacity="0.6"/>
      <g transform="translate(160, 250)">
        <rect x="0" y="0" width="80" height="12" fill={isDark ? '#374151' : '#6b7280'} rx="2"/>
        <line x1="10" y1="2" x2="10" y2="10" stroke={isDark ? '#4b5563' : '#9ca3af'} strokeWidth="0.5"/>
        <line x1="20" y1="2" x2="20" y2="10" stroke={isDark ? '#4b5563' : '#9ca3af'} strokeWidth="0.5"/>
        <line x1="30" y1="2" x2="30" y2="10" stroke={isDark ? '#4b5563' : '#9ca3af'} strokeWidth="0.5"/>
        <line x1="40" y1="2" x2="40" y2="10" stroke={isDark ? '#4b5563' : '#9ca3af'} strokeWidth="0.5"/>
        <line x1="50" y1="2" x2="50" y2="10" stroke={isDark ? '#4b5563' : '#9ca3af'} strokeWidth="0.5"/>
        <line x1="60" y1="2" x2="60" y2="10" stroke={isDark ? '#4b5563' : '#9ca3af'} strokeWidth="0.5"/>
        <line x1="70" y1="2" x2="70" y2="10" stroke={isDark ? '#4b5563' : '#9ca3af'} strokeWidth="0.5"/>
      </g>
    </svg>
  );
};

export default PDFAnalysisIllustration;
