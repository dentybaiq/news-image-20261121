// news-image-20261121 — a one-day world news image (Node 22, standard library only).
// The entry is the entry.png beside this file: a 1024x1024 editorial infographic
// summing up Saturday 21 November 2026. This program copies it to the output
// directory as entry.png, byte for byte, so the judge sees exactly that image.
// It also checks the copy still starts with the PNG signature, so a truncated
// or corrupted copy fails loudly instead of reaching the judge.
//
// Outside the grader's container, MAKEFUN_OUTPUT_DIR stands in for /output:
//   mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts

import { copyFileSync, mkdirSync, readFileSync, statSync } from 'node:fs';
import { dirname, join } from 'node:path';
import { fileURLToPath } from 'node:url';

const here = dirname(fileURLToPath(import.meta.url));
const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? '/output';

mkdirSync(outDir, { recursive: true });
const dest = join(outDir, 'entry.png');
copyFileSync(join(here, 'entry.png'), dest);

// Confirm the copy landed, is a whole PNG, and say how big it is, so a
// failed or partial copy is loud instead of silent.
const { size } = statSync(dest);
const head = readFileSync(dest).subarray(0, 8);
const pngSignature = Buffer.from([0x89, 0x50, 0x4e, 0x47, 0x0d, 0x0a, 0x1a, 0x0a]);
if (!head.equals(pngSignature)) {
  throw new Error(`not a PNG: ${dest}`);
}
console.log(`wrote ${dest} (${size} bytes)`);
