#!/usr/bin/env node
// Pastes the shared blocks from plugins/samatva/skills/_shared/ into every SKILL.md, between
// markers, and keeps the repo-level copies of shipped files in step.
//
//   node scripts/sync-shared.mjs              rewrite every SKILL.md and copy
//   node scripts/sync-shared.mjs --check      exit 1 if anything is stale (CI)
//   node scripts/sync-shared.mjs <SKILL.md>   only these files (no copies)
//
// A SKILL.md holds each block between a start and an end marker on their own lines:
//
//   <!-- samatva:shared:risk-handoff:start -->
//   <!-- samatva:shared:risk-handoff:end -->
//
// Everything between the two is replaced by _shared/<name>.md, minus that file's leading
// <!-- ... --> comment. Every SKILL.md must carry every block in REQUIRED; a block in OPTIONAL
// is pasted only where its markers are. A missing required marker, or an unbalanced or doubled
// marker of any block, is an error in both modes. Exit codes: 0 clean, 1 stale under --check,
// 2 usage or marker error.

import { readFileSync, writeFileSync, readdirSync, existsSync, statSync } from 'node:fs';
import { dirname, join, relative, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';

const ROOT = resolve(dirname(fileURLToPath(import.meta.url)), '..');
const SKILLS = join(ROOT, 'plugins', 'samatva', 'skills');
const SHARED = join(SKILLS, '_shared');
const REQUIRED = ['risk-handoff', 'no-memory'];
// Pasted only into the SKILL.md files that carry their markers; required in the skills listed.
const OPTIONAL = ['arousal-check'];
const REQUIRED_IN = { 'arousal-check': ['samatva', 'vent', 'think-it-through', 'before-you-send', 'cool-down-close'] };
// [source, copy]: the copy must match the source byte for byte (after line-ending normalisation).
const COPIES = [
  ['plugins/samatva/skills/voice-setup/references/example-profile.md', 'examples/voice.md'],
];

const args = process.argv.slice(2);
const check = args.includes('--check');
const only = args.filter((a) => a !== '--check');
const rel = (p) => relative(ROOT, p).split('\\').join('/');
const lf = (s) => s.replace(/\r\n?/g, '\n');

function loadBlock(name) {
  const file = join(SHARED, `${name}.md`);
  if (!existsSync(file)) fail(`missing shared block ${rel(file)}`);
  let text = lf(readFileSync(file, 'utf8'));
  text = text.replace(/^<!--[\s\S]*?-->\n/, '');
  return text.replace(/\n+$/, '') + '\n';
}

function fail(msg) {
  console.error(`error: ${msg}`);
  process.exit(2);
}

function skillFiles() {
  if (only.length) return only.map((p) => resolve(p));
  return readdirSync(SKILLS)
    .filter((d) => !d.startsWith('_') && statSync(join(SKILLS, d)).isDirectory())
    .map((d) => join(SKILLS, d, 'SKILL.md'))
    .filter((f) => existsSync(f));
}

const blocks = Object.fromEntries([...REQUIRED, ...OPTIONAL].map((n) => [n, loadBlock(n)]));
const stale = [];
let errors = 0;

for (const file of skillFiles()) {
  if (!existsSync(file)) {
    console.error(`error: ${rel(file)} does not exist`);
    errors++;
    continue;
  }
  const before = lf(readFileSync(file, 'utf8'));
  let after = before;
  const errorsBefore = errors;
  for (const name of [...REQUIRED, ...OPTIONAL]) {
    const start = `<!-- samatva:shared:${name}:start -->`;
    const end = `<!-- samatva:shared:${name}:end -->`;
    const s = after.indexOf(start);
    const e = after.indexOf(end);
    const skill = file.split(/[\\/]/).slice(-2, -1)[0];
    const needed = !OPTIONAL.includes(name) || (REQUIRED_IN[name] || []).includes(skill);
    if (!needed && s === -1 && e === -1) continue;
    const dup = after.indexOf(start, s + 1) !== -1 || after.indexOf(end, e + 1) !== -1;
    if (s === -1 || e === -1 || e < s || dup) {
      console.error(`error: ${rel(file)} needs exactly one ${start} ... ${end} pair`);
      errors++;
      continue;
    }
    after = after.slice(0, s + start.length) + '\n' + blocks[name] + after.slice(e);
  }
  if (errors > errorsBefore) continue;
  if (after !== before) {
    stale.push(rel(file));
    if (!check) writeFileSync(file, after);
  }
}

if (!only.length) {
  for (const [src, copy] of COPIES) {
    const srcPath = join(ROOT, src);
    const copyPath = join(ROOT, copy);
    if (!existsSync(srcPath)) continue;
    const want = lf(readFileSync(srcPath, 'utf8'));
    const have = existsSync(copyPath) ? lf(readFileSync(copyPath, 'utf8')) : null;
    if (have !== want) {
      stale.push(copy);
      if (!check) writeFileSync(copyPath, want);
    }
  }
}

if (errors) process.exit(2);
if (check && stale.length) {
  console.error(`stale (run node scripts/sync-shared.mjs):\n  ${stale.join('\n  ')}`);
  process.exit(1);
}
console.log(stale.length ? `${check ? 'would update' : 'updated'}: ${stale.join(', ')}` : 'shared blocks in sync');
