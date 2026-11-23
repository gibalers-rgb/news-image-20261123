// news-image-20261123 — the program that ships the entry.
//
// The entry itself is a single picture: a newspaper front page for
// Monday 23 November 2026, stored next to this file as entry.png.
// All this program does is hand that picture over to the grader,
// unchanged, and prove it did. It reads the PNG, makes sure it is
// really the picture the competition expects — a genuine 1024 by 1024
// PNG, no bigger than a mebibyte — writes it to the output folder
// under the same name, and reads it back to confirm every byte
// arrived. Run it twice and the output is identical both times,
// because the input never changes.
//
// Try it locally with:
//   mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts

import { createHash } from 'node:crypto';
import { mkdirSync, readFileSync, statSync, writeFileSync } from 'node:fs';
import { dirname, join } from 'node:path';
import { fileURLToPath } from 'node:url';

const PNG_SIGNATURE = Buffer.from([
  0x89, 0x50, 0x4e, 0x47, 0x0d, 0x0a, 0x1a, 0x0a,
]);
const MAX_SIZE_BYTES = 1024 * 1024;
const WANT_WIDTH = 1024;
const WANT_HEIGHT = 1024;

const repoDir = dirname(fileURLToPath(import.meta.url));
const sourceFile = join(repoDir, 'entry.png');
// An empty MAKEFUN_OUTPUT_DIR counts as unset, so a stray empty
// variable cannot make the program write into the current folder.
const outDir = process.env.MAKEFUN_OUTPUT_DIR?.trim()
  ? process.env.MAKEFUN_OUTPUT_DIR
  : '/output';

function fail(message: string): never {
  throw new Error(`entry.png rejected: ${message}`);
}

function readSource(): Buffer {
  let data: Buffer;
  try {
    data = readFileSync(sourceFile);
  } catch {
    fail(`cannot read ${sourceFile}`);
  }
  return data!;
}

function checkPng(data: Buffer): void {
  if (data.length < 24) {
    fail(`only ${data.length} bytes, too short to be a PNG`);
  }
  if (!data.subarray(0, 8).equals(PNG_SIGNATURE)) {
    fail('does not start with the PNG signature');
  }
  if (data.length > MAX_SIZE_BYTES) {
    fail(`${data.length} bytes, over the 1 MiB limit`);
  }
  // Inside the file, the first chunk is IHDR: four bytes of length,
  // the four letters "IHDR", then width and height as big-endian
  // 32-bit numbers.
  if (data.subarray(12, 16).toString('ascii') !== 'IHDR') {
    fail('first chunk is not IHDR');
  }
  const width = data.readUInt32BE(16);
  const height = data.readUInt32BE(20);
  if (width !== WANT_WIDTH || height !== WANT_HEIGHT) {
    fail(`is ${width}x${height}, expected ${WANT_WIDTH}x${WANT_HEIGHT}`);
  }
}

function main(): void {
  const data = readSource();
  checkPng(data);

  try {
    mkdirSync(outDir, { recursive: true });
  } catch {
    fail(`cannot create the output directory ${outDir}`);
  }
  const target = join(outDir, 'entry.png');
  writeFileSync(target, data);

  const written = readFileSync(target);
  if (!written.equals(data)) {
    fail(`what came back from ${target} differs from the source`);
  }
  const digest = createHash('sha256').update(written).digest('hex');
  const size = statSync(target).size;
  console.log(`entry.png -> ${target} (${size} bytes, sha256=${digest})`);
}

main();
