import React from 'react';

export default function SimpleApp() {
  return (
    <div className="min-h-screen bg-gray-950 text-white flex items-center justify-center">
      <div className="text-center space-y-6">
        <h1 className="text-4xl font-bold text-blue-400">🚀 HybridBot</h1>
        <p className="text-xl text-gray-300">Client Portal Test</p>
        <div className="bg-gray-800 rounded-lg p-6 max-w-md mx-auto">
          <h2 className="text-lg font-semibold mb-4">✅ React App Working!</h2>
          <p className="text-gray-400 mb-4">
            If you can see this, your React setup is working correctly.
          </p>
          <div className="space-y-2">
            <div className="flex items-center justify-between">
              <span>Frontend:</span>
              <span className="text-green-400">✅ Working</span>
            </div>
            <div className="flex items-center justify-between">
              <span>TypeScript:</span>
              <span className="text-green-400">✅ Working</span>
            </div>
            <div className="flex items-center justify-between">
              <span>Tailwind CSS:</span>
              <span className="text-green-400">✅ Working</span>
            </div>
          </div>
          <button 
            onClick={() => alert('Button works!')}
            className="mt-4 w-full bg-blue-600 hover:bg-blue-700 text-white font-medium py-2 px-4 rounded-lg transition-colors"
          >
            Test Button
          </button>
        </div>
        
        <div className="text-sm text-gray-500">
          <p>Next: Start your Python backend and enable authentication</p>
          <p className="mt-2">
            <span className="bg-gray-800 px-2 py-1 rounded">python test-app.py</span>
          </p>
        </div>
      </div>
    </div>
  );
}