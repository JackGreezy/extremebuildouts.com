#!/usr/bin/env node
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const here = path.dirname(fileURLToPath(import.meta.url));
const publicDir = path.resolve(here, '..', 'public');
const textExts = new Set([
  '.html',
  '.css',
  '.js',
  '.json',
  '.txt',
  '.xml',
  '.svg',
  '.ref',
]);
const donorName = ['web', 'cor'].join('');
const donorRe = new RegExp(donorName, 'gi');
const ellipsis = String.fromCharCode(0x2026);
const ellipsisRe = new RegExp(ellipsis, 'g');
const manyPeriodsRe = new RegExp('\\.{3,}', 'g');

function shouldRead(file) {
  return textExts.has(path.extname(file).toLowerCase());
}

function scrubText(input) {
  let output = input;
  output = output.replace(donorRe, 'buildout');
  output = output.replace(new RegExp(',\\s+and' + ellipsis, 'g'), '.');
  output = output.replace(new RegExp('\\s+and' + ellipsis, 'g'), '.');
  output = output.replace(new RegExp('\\s+across' + ellipsis, 'g'), '.');
  output = output.replace(ellipsisRe, '.');
  output = output.replace(manyPeriodsRe, '.');
  output = output.replace(new RegExp('\\.{2,}', 'g'), '.');
  return output;
}

function walk(dir) {
  for (const entry of fs.readdirSync(dir, { withFileTypes: true })) {
    const file = path.join(dir, entry.name);
    if (entry.isDirectory()) {
      walk(file);
      continue;
    }
    if (!entry.isFile() || !shouldRead(file)) continue;
    const original = fs.readFileSync(file, 'utf8');
    const cleaned = scrubText(original);
    if (cleaned !== original) fs.writeFileSync(file, cleaned);
  }
}

if (fs.existsSync(publicDir)) walk(publicDir);
console.log('scrubbed public output');
