import React, { StrictMode } from 'react';
import { createRoot } from 'react-dom/client';
import SimpleApp from './SimpleApp';
import './index.css';

createRoot(document.getElementById('root')!).render(
  <React.StrictMode>
    <SimpleApp />
  </React.StrictMode>
);
