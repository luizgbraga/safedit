export abstract class CRDTOp {
  constructor(public siteId: string) {}

  abstract type: 'insert' | 'delete';

  abstract merge(op: CRDTOp): boolean;
}

export class InsertOp extends CRDTOp {
  type: 'insert' = 'insert';
  constructor(
    public pos: number,
    public value: string,
    siteId: string
  ) {
    super(siteId);
  }

  merge(op: CRDTOp): boolean {
    if (op instanceof InsertOp) {
      if (op.pos === this.pos + this.value.length && op.siteId === this.siteId) {
        this.value += op.value;
        return true;
      }
    }
    if (op instanceof DeleteOp) {
      // Could define merge logic for Insert + Delete if desired
      // Example: no-op merge for now
      return false;
    }
    return false;
  }
}

export class DeleteOp extends CRDTOp {
  type: 'delete' = 'delete';
  constructor(
    public pos: number,
    public length: number,
    siteId: string
  ) {
    super(siteId);
  }

  merge(op: CRDTOp): boolean {
    if (op instanceof DeleteOp) {
      if (op.pos === this.pos && op.siteId === this.siteId) {
        this.length += op.length;
        return true;
      }
    }
    if (op instanceof InsertOp) {
      // Could define merge logic for Delete + Insert if desired
      return false;
    }
    return false;
  }
}

export function reduceOps(ops: CRDTOp[]): CRDTOp[] {
  if (ops.length === 0) return [];

  const reduced: CRDTOp[] = [];
  for (const op of ops) {
    if (reduced.length === 0) {
      reduced.push(op);
      continue;
    }

    const last = reduced[reduced.length - 1];
    if (!last.merge(op)) {
      reduced.push(op);
    }
  }
  return reduced;
}
