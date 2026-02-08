import React, { useRef, useState } from 'react';
import { useTheme } from '../context/ThemeContext';
import { uploadPDF } from '../services/api';

const Upload = ({ onUploadSuccess, isLoading }) => {
  const { isDark } = useTheme();
  const fileInputRef = useRef(null);
  const [fileName, setFileName] = useState('');
  const [error, setError] = useState('');
  const [uploading, setUploading] = useState(false);

  const handleFileSelect = (e) => {
    const file = e.target.files?.[0];
    if (file) {
      setFileName(file.name);
      setError('');
    }
  };

  const handleUpload = async () => {
    if (!fileInputRef.current?.files?.[0]) {
      setError('Please select a PDF file');
      return;
    }

    const file = fileInputRef.current.files[0];

    // Validate file type
    if (!file.type.includes('pdf') && !file.name.toLowerCase().endsWith('.pdf')) {
      setError('Please upload a valid PDF file');
      return;
    }

    // Validate file size (max 50MB)
    if (file.size > 50 * 1024 * 1024) {
      setError('File size must be less than 50MB');
      return;
    }

    setUploading(true);
    setError('');

    try {
      const response = await uploadPDF(file);
      setFileName('');
      if (fileInputRef.current) {
        fileInputRef.current.value = '';
      }
      onUploadSuccess(response);
    } catch (error) {
      setError(
        error.response?.data?.detail ||
        error.message ||
        'Failed to upload PDF. Please try again.'
      );
    } finally {
      setUploading(false);
    }
  };

  return (
    <div className={`rounded-xl shadow-lg p-10 max-w-2xl mx-auto ${isDark ? 'bg-slate-800 border border-slate-700' : 'bg-white border border-slate-200'}`}>
      <div className="text-center">
        <div className="mb-8">
          <div className="text-6xl mb-4 animate-bounce">📄</div>
          <h2 className={`text-3xl font-bold mb-2 ${isDark ? 'text-white' : 'text-slate-900'}`}>
            Upload Your Document
          </h2>
          <p className={isDark ? 'text-slate-400' : 'text-slate-600'}>
            Select a PDF to unlock intelligent insights and instant answers
          </p>
        </div>

        <div className={`border-2 border-dashed rounded-xl p-10 mb-6 transition-all duration-300 ${isDark ? 'border-primary-600/50 hover:border-primary-500 bg-slate-700/30' : 'border-primary-300 hover:border-primary-600 bg-primary-50'}`}>
          <input
            ref={fileInputRef}
            type="file"
            accept=".pdf,application/pdf"
            onChange={handleFileSelect}
            className="hidden"
            id="pdf-input"
            disabled={isLoading || uploading}
          />

          <label htmlFor="pdf-input" className="cursor-pointer block">
            <div className={`text-lg font-semibold mb-2 ${isDark ? 'text-primary-400' : 'text-primary-700'}`}>
              {fileName || 'Click to browse or drag PDF here'}
            </div>
            {fileName && <div className={`text-sm ${isDark ? 'text-slate-400' : 'text-slate-500'}`}>✓ Ready to upload</div>}
          </label>
        </div>

        {error && (
          <div className={`${isDark ? 'bg-red-900/30 border border-red-700/50 text-red-300' : 'bg-red-50 border border-red-200 text-red-700'} px-4 py-3 rounded-lg mb-6 text-sm`}>
            ⚠️ {error}
          </div>
        )}

        <button
          onClick={handleUpload}
          disabled={!fileName || isLoading || uploading}
          className={`w-full py-4 px-6 rounded-lg font-semibold text-lg transition-all duration-200 transform ${
            fileName && !isLoading && !uploading
              ? `${isDark ? 'bg-primary-600 hover:bg-primary-700 text-white shadow-lg hover:shadow-primary-500/20 hover:scale-105' : 'bg-primary-600 hover:bg-primary-700 text-white shadow-md hover:shadow-primary-500/30 hover:scale-105'} cursor-pointer`
              : `${isDark ? 'bg-slate-700 text-slate-400' : 'bg-slate-200 text-slate-400'} cursor-not-allowed`
          }`}
        >
          {uploading ? (
            <span className="flex items-center justify-center gap-2">
              <span className="animate-spin">⏳</span> Uploading...
            </span>
          ) : (
            'Upload PDF'
          )}
        </button>

        <p className={`text-xs mt-4 ${isDark ? 'text-slate-500' : 'text-slate-500'}`}>
          ✓ Secure • ✓ Fast Processing • ✓ Up to 50MB
        </p>
      </div>
    </div>
  );
};

export default Upload;
