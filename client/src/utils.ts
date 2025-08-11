export const API_BASE = import.meta.env.DEV ? 'http://localhost:8000/api' : '/api';

export const WS_URL = import.meta.env.DEV
  ? 'ws://localhost:8000'
  : window.location.origin.replace(/^http/, 'ws');
