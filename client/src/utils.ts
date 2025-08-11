export const API_BASE = import.meta.env.DEV ? 'http://localhost:8000/api' : '/api';

export const WS_URL = import.meta.env.DEV
  ? 'ws://localhost:8000'
  : window.location.origin.replace(/^http/, 'ws');

export class Semaphore {
  private _locked = false;
  lock() {
    this._locked = true;
  }
  unlock() {
    this._locked = false;
  }
  isLocked() {
    return this._locked;
  }
}
