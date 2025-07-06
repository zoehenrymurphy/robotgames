onmessage = function (e) {
    const { robotPos, totalKeys, gridData, itemMap, ROWS, COLS } = e.data;
    const result = aStarPathfinding(robotPos, totalKeys, gridData, itemMap, ROWS, COLS);
    postMessage(result);
};
function heuristic(r, c, targets) {
    let min = Infinity;
    for (const [tr, tc] of targets) {
        const d = Math.abs(r - tr) + Math.abs(c - tc);
        if (d < min) min = d;
    }
    return min === Infinity ? 0 : min;
}
function aStarPathfinding(start, totalKeys, grid, itemMap, ROWS, COLS) {
    const dirMap = ['up', 'down', 'left', 'right'];
    const deltas = [
        [-1, 0], [1, 0], [0, -1], [0, 1]
    ];
    const toIndex = (r, c) => r * COLS + c;
    const getBit = (mask, bit) => (mask >> bit) & 1;
    const setBit = (mask, bit) => mask | (1 << bit);
    const visited = new Set();
    const pq = new MinHeap((a, b) => a.f - b.f);
    // Pre-collect positions of all keys and door(s)
    const keyTargets = [];
    const doorTargets = [];
    for (let i = 0; i < grid.length; i++) {
        if (grid[i] === 1) keyTargets.push([Math.floor(i / COLS), i % COLS]);
        if (grid[i] === 4) doorTargets.push([Math.floor(i / COLS), i % COLS]);
    }
    pq.push({
        r: start.row,
        c: start.col,
        keys: 0,
        hammers: 0,
        collected: 0,
        g: 0,
        f: 0,
        path: []
    });
    while (!pq.isEmpty()) {
        const node = pq.pop();
        const { r, c, keys, hammers, collected, g, path } = node;
        const index = toIndex(r, c);
        const hash = `${r},${c},${keys},${hammers},${collected}`;
        if (visited.has(hash)) continue;
        visited.add(hash);
        const cell = grid[index];
        const id = itemMap[index];
        let newKeys = keys;
        let newHammers = hammers;
        let newCollected = collected;
        if (id >= 0 && getBit(collected, id) === 0) {
            if (cell === 1) {
                newKeys += 1;
                newCollected = setBit(collected, id);
            } else if (cell === 2) {
                newHammers += 1;
                newCollected = setBit(collected, id);
            } else if (cell === 3) {
                if (hammers > 0) {
                    newHammers -= 1;
                    newCollected = setBit(collected, id);
                } else {
                    continue;
                }
            }
        } else if (cell === 3 && (id === -1 || getBit(collected, id) === 0)) {
            continue;
        }
        // Check win condition
        if (cell === 4 && newKeys >= totalKeys) {
            return path;
        }
        for (let d = 0; d < 4; d++) {
            const [dr, dc] = deltas[d];
            const nr = r + dr;
            const nc = c + dc;
            if (nr < 0 || nr >= ROWS || nc < 0 || nc >= COLS) continue;
            const nextPath = [...path, dirMap[d]];
            const h = heuristic(nr, nc,
                newKeys < totalKeys
                    ? keyTargets.filter(([kr, kc], i) => {
                            const idx = toIndex(kr, kc);
                            const kid = itemMap[idx];
                            return kid >= 0 && getBit(newCollected, kid) === 0;
                        })
                    : doorTargets
            );
            pq.push({
                r: nr,
                c: nc,
                keys: newKeys,
                hammers: newHammers,
                collected: newCollected,
                g: g + 1,
                f: g + 1 + h,
                path: nextPath
            });
        }
    }
    return null; // no solution
}
// MinHeap implementation
class MinHeap {
    constructor(compare) {
        this.compare = compare;
        this.items = [];
    }
    push(item) {
        this.items.push(item);
        this.bubbleUp();
    }
    pop() {
        const top = this.items[0];
        const bottom = this.items.pop();
        if (this.items.length > 0) {
            this.items[0] = bottom;
            this.bubbleDown();
        }
        return top;
    }
    bubbleUp() {
        let index = this.items.length - 1;
        while (index > 0) {
            const parent = Math.floor((index - 1) / 2);
            if (this.compare(this.items[index], this.items[parent]) >= 0) break;
            [this.items[index], this.items[parent]] = [this.items[parent], this.items[index]];
            index = parent;
        }
    }
    bubbleDown() {
        let index = 0;
        const length = this.items.length;
        while (true) {
            let left = 2 * index + 1;
            let right = 2 * index + 2;
            let smallest = index;
            if (left < length && this.compare(this.items[left], this.items[smallest]) < 0) {
                smallest = left;
            }
            if (right < length && this.compare(this.items[right], this.items[smallest]) < 0) {
                smallest = right;
            }
            if (smallest === index) break;
            [this.items[index], this.items[smallest]] = [this.items[smallest], this.items[index]];
            index = smallest;
        }
    }
    isEmpty() {
        return this.items.length === 0;
    }
}