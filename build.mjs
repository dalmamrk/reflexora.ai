/**
 * build.mjs — Partial inliner for reflexora.ai
 *
 * PURPOSE
 * -------
 * Implements the "Option A" DRY strategy described in for_agents.md §3.4.
 * Reads canonical partial files from partials/ and inlines their content
 * into every HTML page in the project root.
 *
 * HOW IT WORKS
 * ------------
 * Each HTML page may contain idempotent include markers:
 *
 *   <!-- @include: header -->
 *   <!-- @endinclude: header -->
 *
 *   <!-- @include: footer -->
 *   <!-- @endinclude: footer -->
 *
 * On first run:  the opening marker is replaced with the content block.
 * On re-runs:    the entire block (open marker → close marker) is replaced,
 *                so the script is fully idempotent — no duplication.
 *
 * If a page has no markers, it is left untouched.
 * If a partial file is missing, a warning is printed and the script exits 0.
 *
 * USAGE
 * -----
 *   node build.mjs
 *
 * This is a LOCAL build helper only. Nothing here runs at runtime on the
 * server. The site stays 100% static (HTML/CSS/JS vanilla). Node is only
 * needed on the developer machine, never on Aruba hosting.
 *
 * SAFE DIRECTORIES
 * ----------------
 * Only .html files in the project root are processed.
 * Sub-directories (css/, js/, fonts/, images/, partials/, "per testi/", etc.)
 * are intentionally excluded.
 */

import { readFileSync, writeFileSync, readdirSync, existsSync } from 'fs';
import { join, dirname } from 'path';
import { fileURLToPath } from 'url';

// ---------------------------------------------------------------------------
// Config
// ---------------------------------------------------------------------------

const __dirname = dirname(fileURLToPath(import.meta.url));
const ROOT = __dirname;

/** Pages listed in for_agents.md §3.2 + any other .html in root */
const KNOWN_PAGES = [
  'index.html',
  'architecture.html',
  'technology.html',
  'applications.html',
  'research.html',
  'patents.html',
  'company.html',
  'contact.html',
  'privacy.html',
  'cookie-policy.html',
  '404.html',
];

/** Partials to inline, in the order they appear in markup */
const PARTIALS = ['header', 'footer'];

// ---------------------------------------------------------------------------
// Helpers
// ---------------------------------------------------------------------------

/**
 * Build a regex that matches either:
 *   A) A full idempotent block already injected by a previous run:
 *      <!-- @include: NAME --> ... <!-- @endinclude: NAME -->
 *   B) A bare opening marker with no closing tag (first-time insertion):
 *      <!-- @include: NAME -->
 *
 * Returns a regex with a named group `block` covering the full match.
 */
function buildMarkerRegex(name) {
  // Case A: already wrapped  (lazy match so we stop at the first @endinclude)
  const full = `<!-- @include: ${name} -->[\\s\\S]*?<!-- @endinclude: ${name} -->`;
  // Case B: bare marker (no content between open/close)
  const bare = `<!-- @include: ${name} -->`;
  return new RegExp(`(?:${full}|${bare})`, 'g');
}

/**
 * Wrap partial content in idempotent markers so future runs can replace it.
 */
function wrap(name, content) {
  return `<!-- @include: ${name} -->\n${content.trim()}\n<!-- @endinclude: ${name} -->`;
}

/**
 * Collect HTML files to process.
 * Prioritise the known list, then catch any extra .html in root.
 * Never descend into sub-directories.
 */
function collectHtmlFiles() {
  const entries = readdirSync(ROOT, { withFileTypes: true });
  const rootHtmlFiles = entries
    .filter(e => e.isFile() && e.name.endsWith('.html'))
    .map(e => e.name);

  // Union: known pages first, then any unrecognised .html files in root
  const all = new Set([...KNOWN_PAGES, ...rootHtmlFiles]);
  return [...all].filter(name => existsSync(join(ROOT, name)));
}

// ---------------------------------------------------------------------------
// Main
// ---------------------------------------------------------------------------

function main() {
  // 1. Load partials — bail out gracefully if missing
  const partialContent = {};
  let anyMissing = false;

  for (const name of PARTIALS) {
    const partialPath = join(ROOT, 'partials', `${name}.html`);
    if (!existsSync(partialPath)) {
      console.warn(`⚠️  WARNING: partials/${name}.html not found — skipping all @include: ${name} markers.`);
      console.warn(`   (Create the file at ${partialPath} and re-run build.mjs)`);
      anyMissing = true;
      partialContent[name] = null; // signal: skip this partial
    } else {
      partialContent[name] = readFileSync(partialPath, 'utf8');
      console.log(`✔  Loaded  partials/${name}.html`);
    }
  }

  if (anyMissing) {
    console.warn('\n⚠️  One or more partials are missing. Only present partials will be inlined.\n');
  }

  // 2. Process each HTML file
  const pages = collectHtmlFiles();

  if (pages.length === 0) {
    console.log('ℹ  No HTML files found in project root. Nothing to do.');
    process.exit(0);
  }

  let updatedCount = 0;

  for (const filename of pages) {
    const filePath = join(ROOT, filename);
    let source = readFileSync(filePath, 'utf8');
    let changed = false;

    for (const name of PARTIALS) {
      if (partialContent[name] === null) continue; // partial missing — skip

      const regex = buildMarkerRegex(name);
      const replacement = wrap(name, partialContent[name]);

      if (regex.test(source)) {
        // Reset lastIndex after the test() call
        regex.lastIndex = 0;
        const updated = source.replace(regex, replacement);
        if (updated !== source) {
          source = updated;
          changed = true;
        }
      }
      // If no marker found in file, leave file unchanged (don't auto-inject)
    }

    if (changed) {
      writeFileSync(filePath, source, 'utf8');
      console.log(`  ✏️  Updated  ${filename}`);
      updatedCount++;
    } else {
      console.log(`  –  No markers in ${filename}, skipped.`);
    }
  }

  console.log(`\n✅  Done. ${updatedCount} file(s) updated out of ${pages.length} processed.`);
}

main();
