import React from 'react';
import { AnalysisResult } from '../api';
import { ShieldCheck, ShieldAlert, AlertTriangle } from 'lucide-react';

interface Props {
  result: AnalysisResult;
}

const ResultCard: React.FC<Props> = ({ result }) => {
  const isReal = result.prediction === 'REAL';
  const isBorderline = result.confidence < 70;

  const bgColor  = isBorderline ? 'bg-yellow-50 border-yellow-400'
                 : isReal       ? 'bg-green-50 border-green-500'
                 :                'bg-red-50 border-red-500';

  const textColor = isBorderline ? 'text-yellow-700'
                  : isReal       ? 'text-green-700'
                  :                'text-red-700';

  const Icon = isBorderline ? AlertTriangle
             : isReal       ? ShieldCheck
             :                ShieldAlert;

  const label = isBorderline ? 'UNCERTAIN'
              : result.prediction;

  return (
    <div className={`border-2 rounded-2xl p-6 mt-6 ${bgColor} shadow-md`}>

      {/* Header */}
      <div className="flex items-center gap-3 mb-4">
        <Icon className={`w-10 h-10 ${textColor}`} />
        <div>
          <p className="text-sm text-gray-500 font-medium">Verdict</p>
          <h2 className={`text-3xl font-bold ${textColor}`}>{label}</h2>
        </div>
      </div>

      {/* Score bars */}
      <div className="mb-4">
        <div className="flex justify-between text-sm font-medium mb-1">
          <span className="text-green-700">Real</span>
          <span className="text-green-700">{result.real_score}%</span>
        </div>
        <div className="w-full bg-gray-200 rounded-full h-3 mb-3">
          <div
            className="bg-green-500 h-3 rounded-full transition-all duration-700"
            style={{ width: `${result.real_score}%` }}
          />
        </div>

        <div className="flex justify-between text-sm font-medium mb-1">
          <span className="text-red-700">Fake</span>
          <span className="text-red-700">{result.fake_score}%</span>
        </div>
        <div className="w-full bg-gray-200 rounded-full h-3">
          <div
            className="bg-red-500 h-3 rounded-full transition-all duration-700"
            style={{ width: `${result.fake_score}%` }}
          />
        </div>
      </div>

      {/* Confidence */}
      <div className="flex items-center justify-between bg-white rounded-xl px-4 py-3 mt-4 shadow-sm">
        <span className="text-gray-600 font-medium">Confidence</span>
        <span className={`text-2xl font-bold ${textColor}`}>
          {result.confidence}%
        </span>
      </div>

      {/* Content preview */}
      {result.content_preview && (
        <div className="mt-4 bg-white rounded-xl px-4 py-3 shadow-sm">
          <p className="text-xs text-gray-400 font-medium mb-1">Content analyzed</p>
          <p className="text-sm text-gray-600 leading-relaxed line-clamp-3">
            {result.content_preview}
          </p>
        </div>
      )}

      {result.title && (
        <div className="mt-3 bg-white rounded-xl px-4 py-3 shadow-sm">
          <p className="text-xs text-gray-400 font-medium mb-1">Article title</p>
          <p className="text-sm text-gray-700 font-semibold">{result.title}</p>
        </div>
      )}
    </div>
  );
};

export default ResultCard;