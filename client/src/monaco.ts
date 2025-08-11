import * as monaco from 'monaco-editor';

import { api } from './api';
import { ws } from './socket';
import { CRDTOp, DeleteOp, InsertOp, reduceOps } from './crdt';
import debounce from 'lodash.debounce';
import { Semaphore } from './utils';

let editor: monaco.editor.IStandaloneCodeEditor | undefined;

const remoteUpdateSemaphore = new Semaphore();

let crdtOpBuffer: CRDTOp[] = [];

const flushCRDTOps = debounce(() => {
  if (crdtOpBuffer.length === 0) return;
  const reduced = reduceOps(crdtOpBuffer);
  reduced.forEach((op) => ws.sendCRDTOp(op));
  crdtOpBuffer = [];
}, 1000);

const getChangeType = (change: monaco.editor.IModelContentChangedEvent['changes'][0]) => {
  if (change.text.length > 0 && change.rangeLength === 0) {
    return 'insert';
  } else if (change.text.length === 0 && change.rangeLength > 0) {
    return 'delete';
  } else {
    return 'replace';
  }
};

export async function setupMonacoEditor() {
  const initialContent = await api.getContent();
  editor = monaco.editor.create(document.getElementById('editor') as HTMLElement, {
    value: initialContent,
    language: 'plaintext',
    theme: 'vs-dark',
    fontSize: 15,
    minimap: { enabled: false },
    automaticLayout: true,
    scrollbar: { vertical: 'hidden', horizontal: 'hidden' },
  });

  if (editor) {
    editor.onDidChangeModelContent((event) => {
      if (remoteUpdateSemaphore.isLocked()) {
        return;
      }
      event.changes.forEach((change) => {
        const changeType = getChangeType(change);
        if (changeType === 'insert') {
          const op = new InsertOp(change.rangeOffset, change.text, ws.id);
          crdtOpBuffer.push(op);
        } else if (changeType === 'delete') {
          const op = new DeleteOp(change.rangeOffset, change.rangeLength, ws.id);
          crdtOpBuffer.push(op);
        } else {
          const delOp = new DeleteOp(change.rangeOffset, change.rangeLength, ws.id);
          crdtOpBuffer.push(delOp);
          const insOp = new InsertOp(change.rangeOffset, change.text, ws.id);
          crdtOpBuffer.push(insOp);
        }
        flushCRDTOps();
      });
    });
  }

  ws.subscribeToFileChanges(async (newContent) => {
    if (editor && newContent !== editor.getValue()) {
      const pos = editor.getPosition();
      remoteUpdateSemaphore.lock();
      const model = editor.getModel();
      if (model && crdtOpBuffer.length === 0) {
        editor.executeEdits('remote-update', [
          {
            range: model.getFullModelRange(),
            text: newContent,
            forceMoveMarkers: true,
          },
        ]);
      }
      if (pos) editor.setPosition(pos);
      remoteUpdateSemaphore.unlock();
    }
  });
}
