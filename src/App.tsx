    import { defineConfig } from 'vite';
    import react from '@vitejs/plugin-react';

    // https://vitejs.dev/config/
    export default defineConfig({
      plugins: [react()],
      optimizeDeps: {
        // This explicitly tells Vite to not pre-bundle 'reconnecting-websocket'
        // which can sometimes help with CommonJS compatibility.
        include: ['reconnecting-websocket'],
      },
      server: {
        proxy: {
          '/api': {
            target: 'https://hybridbot-backend-273820287691.us-central1.run.app', // Your backend Cloud Run URL
            changeOrigin: true,
            secure: false,
            rewrite: (path) => path.replace(/^\/api/, '/api'),
          },
          '/ws': {
            target: 'wss://hybridbot-backend-273820287691.us-central1.run.app', // Your backend Cloud Run WebSocket URL
            changeOrigin: true,
            ws: true,
            secure: false,
          },
        },
      },
    });
    