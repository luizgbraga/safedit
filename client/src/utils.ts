export const API_BASE = import.meta.env.DEV ? 'http://192.168.15.29:8000/api' : '/api';

export const WS_URL = import.meta.env.DEV
  ? 'ws://192.168.15.29:8000'
  : window.location.origin.replace(/^http/, 'ws');
