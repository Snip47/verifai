import React, { useEffect, useState } from 'react';
import { getHistory, clearHistory, deleteHistoryItem } from '../api';
import { ShieldCheck, ShieldAlert, Trash2, X } from 'lucide-react';

const HistoryList: React.FC = () => {
  const [history, setHistory]   = useState<any[]>([]);
  const [loading, setLoading]   = useState(true);
  const [clearing, setClearing] = useState(false);

  const fetchHistory = () => {
    setLoading(true);
    getHistory()
      .then(res => setHistory(res.data))
      .catch(err => console.error(err))
      .finally(() => setLoading(false));
  };

  useEffect(() => { fetchHistory(); }, []);

  const handleClear = async () => {
    if (!window.confirm('Clear all history? This cannot be undone.')) return;
    setClearing(true);
    try {
      await clearHistory();
      setHistory([]);
    } catch (err) {
      console.error(err);
    } finally {
      setClearing(false);
    }
  };

  const handleDelete = async (id: number) => {
    try {
      await deleteHistoryItem(id);
      setHistory(prev => prev.filter(item => item.id !== id));
    } catch (err) {
      console.error(err);
    }
  };

  if (loading) return (
    <p className="text-gray-400 text-center py-8">Loading history...</p>
  );

  return (
    <div className="mt-6">
      <div className="flex items-center justify-between mb-4">
        <h3 className="text-lg font-bold text-gray-700">
          Recent Analyses ({history.length})
        </h3>
        {history.length > 0 && (
          <button
            onClick={handleClear}
            disabled={clearing}
            className="flex items-center gap-1.5 text-sm text-red-600 bg-red-50 hover:bg-red-100 px-3 py-1.5 rounded-lg transition"
          >
            <Trash2 className="w-4 h-4" />
            {clearing ? 'Clearing...' : 'Clear All'}
          </button>
        )}
      </div>

      {history.length === 0 ? (
        <p className="text-gray-400 text-center py-8">No analyses yet.</p>
      ) : (
        <div className="space-y-3">
          {history.map((item: any) => {
            const isReal = item.prediction === 'REAL';
            return (
              <div key={item.id} className="bg-white rounded-xl px-4 py-3 shadow-sm flex items-center gap-4">
                {isReal
                  ? <ShieldCheck className="w-6 h-6 text-green-500 shrink-0" />
                  : <ShieldAlert className="w-6 h-6 text-red-500 shrink-0" />
                }
                <div className="flex-1 min-w-0">
                  <p className="text-sm text-gray-700 truncate">
                    {item.content?.slice(0, 80)}...
                  </p>
                  <p className="text-xs text-gray-400 mt-0.5">
                    {item.input_type?.toUpperCase()} · {item.confidence?.toFixed(1)}% · {new Date(item.created_at).toLocaleString()}
                  </p>
                </div>
                <span className={`text-sm font-bold shrink-0 ${isReal ? 'text-green-600' : 'text-red-600'}`}>
                  {item.prediction}
                </span>
                <button
                  onClick={() => handleDelete(item.id)}
                  className="text-gray-300 hover:text-red-500 transition shrink-0"
                  title="Delete"
                >
                  <X className="w-4 h-4" />
                </button>
              </div>
            );
          })}
        </div>
      )}
    </div>
  );
};

export default HistoryList;