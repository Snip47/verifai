import React, { useState } from 'react';
import { analyzeText, analyzeUrl, AnalysisResult } from './api';
import ResultCard from './components/ResultCard';
import HistoryList from './components/HistoryList';
import { Search, Link, FileText, Shield } from 'lucide-react';

type Tab = 'text' | 'url';

const App: React.FC = () => {
  const [tab, setTab]         = useState<Tab>('text');
  const [text, setText]       = useState('');
  const [url, setUrl]         = useState('');
  const [result, setResult]   = useState<AnalysisResult | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError]     = useState('');
  const [showHistory, setShowHistory] = useState(false);

  const handleAnalyze = async () => {
    setError('');
    setResult(null);
    setLoading(true);

    try {
      const res = tab === 'text'
        ? await analyzeText(text)
        : await analyzeUrl(url);
      setResult(res.data);
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Something went wrong. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  const isDisabled = loading || (tab === 'text' ? text.trim().length < 20 : url.trim().length < 10);

  return (
    <div className="min-h-screen bg-gray-100">

      {/* Navbar */}
      <nav className="bg-[#1B4F72] text-white px-6 py-4 shadow-lg">
        <div className="max-w-2xl mx-auto flex items-center justify-between">
          <div className="flex items-center gap-2">
            <Shield className="w-7 h-7" />
            <span className="text-xl font-bold tracking-tight">VerifAI</span>
            <span className="text-blue-200 text-sm ml-1">Fake News Detector</span>
          </div>
          <button
            onClick={() => setShowHistory(!showHistory)}
            className="text-sm bg-white/10 hover:bg-white/20 px-3 py-1.5 rounded-lg transition"
          >
            {showHistory ? 'Analyzer' : 'History'}
          </button>
        </div>
      </nav>

      <div className="max-w-2xl mx-auto px-4 py-8">

        {!showHistory ? (
          <>
            {/* Hero */}
            <div className="text-center mb-8">
              <h1 className="text-3xl font-bold text-gray-800 mb-2">
                Is this news real?
              </h1>
              <p className="text-gray-500">
                Paste an article or URL and our AI will analyze it for misinformation.
              </p>
            </div>

            {/* Tab switcher */}
            <div className="flex bg-white rounded-xl shadow-sm p-1 mb-4">
              <button
                onClick={() => { setTab('text'); setResult(null); setError(''); }}
                className={`flex-1 flex items-center justify-center gap-2 py-2.5 rounded-lg text-sm font-medium transition ${
                  tab === 'text'
                    ? 'bg-[#1B4F72] text-white shadow'
                    : 'text-gray-500 hover:text-gray-700'
                }`}
              >
                <FileText className="w-4 h-4" />
                Paste Text
              </button>
              <button
                onClick={() => { setTab('url'); setResult(null); setError(''); }}
                className={`flex-1 flex items-center justify-center gap-2 py-2.5 rounded-lg text-sm font-medium transition ${
                  tab === 'url'
                    ? 'bg-[#1B4F72] text-white shadow'
                    : 'text-gray-500 hover:text-gray-700'
                }`}
              >
                <Link className="w-4 h-4" />
                Enter URL
              </button>
            </div>

            {/* Input area */}
            <div className="bg-white rounded-2xl shadow-sm p-4">
              {tab === 'text' ? (
                <textarea
                  value={text}
                  onChange={e => setText(e.target.value)}
                  placeholder="Paste a news article, headline, or any text you want to verify..."
                  className="w-full h-40 text-sm text-gray-700 placeholder-gray-400 resize-none outline-none leading-relaxed"
                />
              ) : (
                <input
                  value={url}
                  onChange={e => setUrl(e.target.value)}
                  placeholder="https://www.example.com/news/article"
                  className="w-full text-sm text-gray-700 placeholder-gray-400 outline-none py-2"
                />
              )}

              <div className="flex items-center justify-between mt-3 pt-3 border-t border-gray-100">
                <span className="text-xs text-gray-400">
                  {tab === 'text' ? `${text.length} characters` : 'Enter a full article URL'}
                </span>
                <button
                  onClick={handleAnalyze}
                  disabled={isDisabled}
                  className={`flex items-center gap-2 px-5 py-2.5 rounded-xl text-sm font-semibold transition ${
                    isDisabled
                      ? 'bg-gray-200 text-gray-400 cursor-not-allowed'
                      : 'bg-[#1B4F72] text-white hover:bg-[#154360] shadow-md'
                  }`}
                >
                  {loading ? (
                    <>
                      <svg className="animate-spin w-4 h-4" viewBox="0 0 24 24" fill="none">
                        <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"/>
                        <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8v8z"/>
                      </svg>
                      Analyzing...
                    </>
                  ) : (
                    <>
                      <Search className="w-4 h-4" />
                      Analyze
                    </>
                  )}
                </button>
              </div>
            </div>

            {/* Error */}
            {error && (
              <div className="mt-4 bg-red-50 border border-red-200 text-red-700 text-sm rounded-xl px-4 py-3">
                {error}
              </div>
            )}

            {/* Result */}
            {result && <ResultCard result={result} />}
          </>
        ) : (
          <HistoryList />
        )}
      </div>
    </div>
  );
};

export default App;