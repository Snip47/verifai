import React, { useEffect, useState } from 'react';
import { getHistory } from '../api';
import { ShieldCheck, ShieldAlert } from 'lucide-react';

const HistoryList: React.FC = () => {
  const [history, setHistory] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    getHistory()
      .then(res => setHistory(res.data))
      .catch(err => console.error(err))
      .finally(() => setLoading(false));
  }, []);

  if (loading) return <p className="text-gray-400 text-center py-8">Loading history...</p>;
  if (history.length === 0) return <p className="text-gray-400 text-center py-8">No analyses yet.</p>;

  return (
    <div className="mt-6 space-y-3">
      <h3 className="text-lg font-bold text-gray-700">Recent Analyses</h3>
      {history.map((item: any) => {
        const isReal = item.prediction === 'REAL';
        return (
          <div key={item.id} className="bg-white rounded-xl px-4 py-3 shadow-sm flex items-center gap-4">
            {isReal
              ? <ShieldCheck className="w-6 h-6 text-green-500 shrink-0" />
              : <ShieldAlert className="w-6 h-6 text-red-500 shrink-0" />
            }
            <div className="flex-1 min-w-0">
              <p className="text-sm text-gray-700 truncate">{item.content?.slice(0, 80)}...</p>
              <p className="text-xs text-gray-400 mt-0.5">{item.input_type?.toUpperCase()} · {new Date(item.created_at).toLocaleString()}</p>
            </div>
            <span className={`text-sm font-bold shrink-0 ${isReal ? 'text-green-600' : 'text-red-600'}`}>
              {item.prediction}
            </span>
          </div>
        );
      })}
    </div>
  );
};

export default HistoryList;