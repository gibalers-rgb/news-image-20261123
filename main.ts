// news-image-20261123 — entrypoint (Node 22, standard library only).
//
// The entry is the newspaper front page shipped beside this file:
// read it in, check it is the whole PNG the kit gate expects, and write
// it out byte for byte as entry.png, so both grader runs produce the
// exact same bytes. The image sums up the world news of Monday
// 23 November 2026 — the Hormuz/Bahrain escalation, the COP31 collapse,
// the Kyiv-region drone strike, the Seoul minister's resignation, the
// Lisbon cost-of-living march and the Indonesian factory fire.
//
// Local check:  mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts

import { mkdirSync, readFileSync, statSync, writeFileSync } from 'node:fs';
import { join } from 'node:path';
import { createHash } from 'node:crypto';

const PNG_MAGIC = Buffer.from([0x89, 0x50, 0x4e, 0x47, 0x0d, 0x0a, 0x1a, 0x0a]);
const MAX_BYTES = 1_048_576;
const EXPECTED_WIDTH = 1024;
const EXPECTED_HEIGHT = 1024;

const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? '/output';
const sourcePath = new URL('./entry.png', import.meta.url);

const image = readFileSync(sourcePath);
if (!image.subarray(0, PNG_MAGIC.length).equals(PNG_MAGIC)) {
  throw new Error('entry.png is not a PNG file');
}
if (image.length > MAX_BYTES) {
  throw new Error(`entry.png is ${image.length} bytes, over the 1 MiB gate`);
}
// The IHDR chunk follows the 8-byte signature: 4-byte length, 4-byte
// "IHDR", then width and height as 4-byte big-endian integers.
if (image.subarray(12, 16).toString('latin1') !== 'IHDR') {
  throw new Error('entry.png has no IHDR chunk');
}
const width = image.readUInt32BE(16);
const height = image.readUInt32BE(20);
if (width !== EXPECTED_WIDTH || height !== EXPECTED_HEIGHT) {
  throw new Error(`entry.png is ${width}x${height}, expected 1024x1024`);
}

mkdirSync(outDir, { recursive: true });
const target = join(outDir, 'entry.png');
writeFileSync(target, image);

const written = readFileSync(target);
if (!written.equals(image)) {
  throw new Error('entry.png written to /output does not match the source');
}
const sha = createHash('sha256').update(written).digest('hex');
console.log(`wrote ${target} (${statSync(target).size} bytes, sha256=${sha})`);
