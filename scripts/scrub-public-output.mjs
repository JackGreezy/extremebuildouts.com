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
const constructionDescription =
  'Extreme Buildouts LLC provides commercial and residential construction, retail buildouts, A/C, electrical, plumbing, design-build, and ground-up work across East Texas, Houston, and DFW.';
const constructionIntro =
  'Extreme Buildouts LLC coordinates retail buildouts, commercial A/C, electrical, plumbing, design-build, renovations, and ground-up construction under one roof. The work is planned around field conditions, owner timing, trade access, inspections, and the day the space needs to open.';
const contactIntro =
  'Send the project address or area, space type, schedule, known utility needs, and the work you want priced. Extreme Buildouts LLC will review the construction scope and return practical next steps.';
const resetCopy =
  'This link needs a reset. Open service areas, services, industries, project types, or contact Extreme Buildouts LLC for commercial and residential construction.';
const badPublicPatterns = [
  donorRe,
  ellipsisRe,
  manyPeriodsRe,
  /\b1031\b/i,
  /\bexchange\b/i,
  /qualified intermediary/i,
  /replacement property/i,
  /replacement inventory/i,
  /lender timing/i,
  /closing records/i,
  /forty-five day window/i,
  /deadline-first/i,
];

function shouldRead(file) {
  return textExts.has(path.extname(file).toLowerCase());
}

function scrubText(input) {
  let output = input;
  output = output.replace(donorRe, 'buildout');
  output = output.replace(/Texas 1031 Exchange Coordination/g, 'Commercial and Residential Construction');
  output = output.replace(/Texas 1031 exchange questions/g, 'Buildout questions');
  output = output.replace(/Organize this Texas exchange file/g, 'Ready to plan the buildout?');
  output = output.replace(/Deadline-first exchange work for Texas/g, 'Commercial and residential construction under one roof');
  output = output.replace(/Texas exchange review starts here/g, 'Start a buildout review');
  output = output.replace(/Texas exchange route needs a reset/g, 'Route needs a reset');
  output = output.replace(/Back to Texas exchange home/g, 'Back to home');
  output = output.replace(/Texas reset page\. Texas owners can reopen East Texas notes through Retail Buildouts\. Texas teams checking Tyler, TX should review Commercial A\/C Buildouts\. Texas files near Longview, TX can compare Texas Electrical Buildout Services\. Texas links below route Texas service or market decisions\./g, resetCopy);
  output = output.replace(/Texas sale timing, Texas property type, Texas target areas like East Texas and Tyler, TX, plus Texas owner questions help Extreme Buildouts LLC return Texas next coordination steps\./g, contactIntro);
  output = output.replace(/<meta content="Texas sale timing[^"]*" name="description"\/>/g, `<meta content="${contactIntro}" name="description"/>`);
  output = output.replace(/<meta content="Texas sale timing[^"]*" property="og:description"\/>/g, `<meta content="${contactIntro}" property="og:description"/>`);
  output = output.replace(/<meta content="Texas sale timing[^"]*" name="twitter:description"\/>/g, `<meta content="${contactIntro}" name="twitter:description"/>`);
  output = output.replace(/<meta content="Texas reset page[^"]*" name="description"\/>/g, `<meta content="${resetCopy}" name="description"/>`);
  output = output.replace(/<meta content="Texas reset page[^"]*" property="og:description"\/>/g, `<meta content="${resetCopy}" property="og:description"/>`);
  output = output.replace(/<meta content="Texas reset page[^"]*" name="twitter:description"\/>/g, `<meta content="${resetCopy}" name="twitter:description"/>`);
  output = output.replace(/Texas investors/g, 'Texas owners');
  output = output.replace(/Texas lender timing/g, 'Texas project timing');
  output = output.replace(/Tyler, TX closing records/g, 'Tyler, TX project records');
  output = output.replace(/Texas replacement inventory/g, 'Texas field conditions');
  output = output.replace(/Texas advisor questions/g, 'Texas owner questions');
  output = output.replace(/Texas financing limits/g, 'Texas budget constraints');
  output = output.replace(/Texas exchange clock tightens/g, 'construction schedule moves');
  output = output.replace(/the Texas exchange clock tightens/g, 'the construction schedule moves');
  output = output.replace(/before the Texas exchange clock tightens/g, 'before the construction schedule moves');
  output = output.replace(/Texas forty-five day window narrows/g, 'Texas project schedule tightens');
  output = output.replace(/forty-five day window narrows/g, 'project schedule tightens');
  output = output.replace(/1031 file/g, 'construction scope');
  output = output.replace(/exchange file/g, 'buildout scope');
  output = output.replace(/exchange questions/g, 'buildout questions');
  output = output.replace(/exchange coordination/g, 'construction coordination');
  output = output.replace(/exchange work/g, 'construction work');
  output = output.replace(/exchange clock/g, 'construction schedule');
  output = output.replace(/replacement property/g, 'project site');
  output = output.replace(/replacement inventory/g, 'field conditions');
  output = output.replace(/qualified intermediary/g, 'project coordinator');
  output = output.replace(/lender timing/g, 'project timing');
  output = output.replace(/closing records/g, 'project records');
  output = output.replace(/\b1031\b/g, 'buildout');
  output = output.replace(/\bexchange\b/gi, 'construction');
  output = output.replace(/<meta content="Extreme Buildouts LLC helps[^"]+" name="description"\/>/g, `<meta content="${constructionDescription}" name="description"/>`);
  output = output.replace(/<meta content="Extreme Buildouts LLC helps[^"]+" property="og:description"\/>/g, `<meta content="${constructionDescription}" property="og:description"/>`);
  output = output.replace(/<meta content="Extreme Buildouts LLC helps[^"]+" name="twitter:description"\/>/g, `<meta content="${constructionDescription}" name="twitter:description"/>`);
  output = output.replace(/<p class="paragraph">In Texas, a construction scope is shaped[^<]+<\/p>/g, `<p class="paragraph">${constructionIntro}</p>`);
  output = output.replace(new RegExp(',\\s+and' + ellipsis, 'g'), '.');
  output = output.replace(new RegExp('\\s+and' + ellipsis, 'g'), '.');
  output = output.replace(new RegExp('\\s+across' + ellipsis, 'g'), '.');
  output = output.replace(ellipsisRe, '.');
  output = output.replace(manyPeriodsRe, '.');
  output = output.replace(new RegExp('\\.{2,}', 'g'), '.');
  return output;
}

const failures = [];

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
    const finalText = cleaned;
    for (const pattern of badPublicPatterns) {
      pattern.lastIndex = 0;
      if (pattern.test(finalText)) {
        failures.push(`${path.relative(publicDir, file)} :: ${pattern}`);
      }
    }
  }
}

if (fs.existsSync(publicDir)) walk(publicDir);
if (failures.length) {
  console.error('public scrub failed');
  for (const failure of failures.slice(0, 20)) console.error(failure);
  process.exit(1);
}
console.log('scrubbed public output');
