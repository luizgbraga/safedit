import { io, Socket } from 'socket.io-client';
import { WS_URL } from './utils';
import { CRDTOp } from './crdt';

type FileChangeListener = (content: string) => void;

export class SocketHandler {
  socket: Socket | null = null;
  listeners: FileChangeListener[] = [];

  constructor() {
    this.initSocket();
  }

  get id() {
    return this.socket?.id || 'undefined';
  }

  private initSocket() {
    this.socket = io(WS_URL);
    this.socket.on('file_changed', (payload: { content: string }) => {
      if (!payload.content) return;
      this.listeners.forEach((fn) => fn(payload.content));
    });
  }

  public sendCRDTOp(op: Omit<CRDTOp, 'siteId'>) {
    if (this.socket && this.socket.id) {
      const opWithSite = { ...op, siteId: this.socket.id };
      this.socket.emit('crdt_op', opWithSite);
    }
  }

  public subscribeToFileChanges(cb: (content: string) => void) {
    this.listeners.push(cb);

    return () => {
      const idx = this.listeners.indexOf(cb);
      if (idx !== -1) this.listeners.splice(idx, 1);
    };
  }
}

export const ws = new SocketHandler();
