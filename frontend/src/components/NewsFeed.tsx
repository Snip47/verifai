import React, { useEffect, useState } from 'react';
import { fetchNews, analyzeNewsArticle, AnalysisResult } from '../api';
import ResultCard from './ResultCard';
import { Search, Newspaper, ExternalLink, RefreshCw } from 'lucide-react';

interface Article {
  title: string;
  description: string;
  url: string;
  source: string;
  publishedAt: string;
  content: string;
}

const linkStyle = [
  "flex items-center gap-1.5 text-xs font-medium",
  "text-gray-500 hover:text-gray-700 px-3 py-1.5",
  "rounded-lg border border-gray-200 hover:border-gray-300 transition"
].join(' ');

const NewsFeed: React.FC = () => {
  const [articles, setArticles] = useState<Article[]>([]);
  const [loading, setLoading] = useState(true);
  const [query, setQuery] = useState('');
  const [searching, setSearching] = useState(false);
  const [analyzing, setAnalyzing] = useState<number | null>(null);
  const [results, setResults] = useState<Record<number, AnalysisResult>>({});
  const [error, setError] = useState('');

  const loadNews = async (q: string = 'latest') => {
    setLoading(true);
    setError('');
    try {
      const res = await fetchNews(q, 12);
      setArticles(res.data.articles);
    } catch (err: any) {
      setError('Could not load news. Check your NEWS_API_KEY in backend .env file.');
    } finally {
      setLoading(false);
      setSearching(false);
    }
  };

  useEffect(() => {
    loadNews();
  }, []);

  const handleSearch = () => {
    setSearching(true);
    setResults({});
    loadNews(query || 'latest');
  };

  const handleAnalyze = async (article: Article, index: number) => {
    setAnalyzing(index);
    try {
      const res = await analyzeNewsArticle(article.content);
      setResults(prev => ({ ...prev, [index]: res.data }));
    } catch (err) {
      console.error(err);
    } finally {
      setAnalyzing(null);
    }
  };

  if (loading) {
    return (
      <div className="text-center py-12">
        <RefreshCw className="w-8 h-8 animate-spin text-[#1B4F72] mx-auto mb-3" />
        <p className="text-gray-400 text-sm">Fetching latest news...</p>
      </div>
    );
  }

  return (
    <div className="mt-4">
      <div className="flex gap-2 mb-6">
        <input
          value={query}
          onChange={e => setQuery(e.target.value)}
          onKeyDown={e => {
            if (e.key === 'Enter') {
              handleSearch();
            }
          }}
          placeholder="Search news... (e.g. Kenya, AI, sports, health)"
          className="flex-1 bg-white border border-gray-200 rounded-xl px-4 py-2.5 text-sm outline-none"
        />
        <button
          onClick={handleSearch}
          disabled={searching}
          className="bg-[#1B4F72] text-white px-4 py-2.5 rounded-xl flex items-center gap-2 text-sm font-medium"
        >
          <Search className="w-4 h-4" />
          {searching ? 'Searching...' : 'Search'}
        </button>
      </div>

      {error && (
        <div className="bg-red-50 border border-red-200 text-red-700 text-sm rounded-xl px-4 py-3 mb-4">
          {error}
        </div>
      )}

      <div className="space-y-4">
        {articles.map((article, index) => {
          const isAnalyzing = analyzing === index;
          const articleResult = results[index];
          return (
            <div key={index} className="bg-white rounded-2xl shadow-sm p-4">
              <div className="mb-2">
                <div className="flex items-center gap-2 mb-1">
                  <Newspaper className="w-3.5 h-3.5 text-gray-400" />
                  <span className="text-xs text-gray-400">{article.source}</span>
                  <span className="text-xs text-gray-300">·</span>
                  <span className="text-xs text-gray-400">
                    {new Date(article.publishedAt).toLocaleDateString()}
                  </span>
                </div>
                <h4 className="text-sm font-semibold text-gray-800 leading-snug">
                  {article.title}
                </h4>
                <p className="text-xs text-gray-500 mt-1">
                  {article.description}
                </p>
              </div>

              <div className="flex items-center gap-2 mt-3">
                <button
                  onClick={() => handleAnalyze(article, index)}
                  disabled={isAnalyzing}
                  className="flex items-center gap-1.5 text-xs font-medium bg-[#1B4F72] text-white px-3 py-1.5 rounded-lg"
                >
                  {isAnalyzing
                    ? <RefreshCw className="w-3 h-3 animate-spin" />
                    : <Search className="w-3 h-3" />
                  }
                  {isAnalyzing ? 'Analyzing...' : 'Analyze'}
                </button>
                <a href={article.url} target="_blank" rel="noopener noreferrer" className={linkStyle}>
                  <ExternalLink className="w-3 h-3" />
                  Read
                </a>
              </div>

              {articleResult && (
                <ResultCard result={articleResult} />
              )}
            </div>
          );
        })}
      </div>
    </div>
  );
};

export default NewsFeed;