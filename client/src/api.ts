import { API_BASE } from './utils';

export class Api {
  baseUrl: string;

  constructor(baseUrl: string) {
    this.baseUrl = baseUrl;
  }

  async getContent(): Promise<string> {
    try {
      const res = await fetch(`${this.baseUrl}/file`);
      if (!res.ok) return '';
      const data = await res.json();
      return data.content || '';
    } catch (e) {
      console.error('Error fetching initial content:', e);
      return '';
    }
  }
}

export const api = new Api(API_BASE);
