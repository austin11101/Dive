import { defineConfig } from 'vite';
import { resolve } from 'path';

export default defineConfig({
  server: {
    port: 4200,
    host: '0.0.0.0',
    watch: {
      usePolling: true,
      interval: 1000,
    },
    hmr: {
      overlay: true,
    },
    cors: true,
  },
  build: {
    target: 'es2020',
    outDir: 'dist',
    sourcemap: true,
    rollupOptions: {
      input: {
        main: resolve(__dirname, 'src/main.ts'),
      },
      output: {
        manualChunks: {
          vendor: ['@angular/core', '@angular/common', '@angular/platform-browser'],
          rxjs: ['rxjs'],
        },
      },
    },
  },
  resolve: {
    alias: {
      '@': resolve(__dirname, 'src'),
    },
  },
  optimizeDeps: {
    include: [
      'bootstrap',
      '@angular/core',
      '@angular/common',
      '@angular/platform-browser',
      'rxjs',
    ],
    exclude: ['@angular/platform-browser-dynamic'],
  },
  plugins: [],
}); 