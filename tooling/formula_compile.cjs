// Compile formulas with the KaTeX the kit ships, for lint's formula check
// (tooling/formula_checks.py). Reads [{tex, display}] as JSON on stdin and
// writes {katex, results}: per formula null, or KaTeX's error message.
'use strict';
const path = require('path');
const katex = require(path.join(__dirname, '..', 'theme', 'assets', 'vendor', 'katex', 'katex.min.js'));

let input = '';
process.stdin.setEncoding('utf8');
process.stdin.on('data', chunk => { input += chunk; });
process.stdin.on('end', () => {
  const formulas = JSON.parse(input);
  const results = formulas.map(({tex, display}) => {
    try {
      // Strictness changes warnings only; a formula renders or throws as in the browser.
      katex.renderToString(String(tex), {displayMode: Boolean(display), throwOnError: true, strict: 'ignore'});
      return null;
    } catch (problem) {
      return String(problem && problem.message || problem);
    }
  });
  process.stdout.write(JSON.stringify({katex: katex.version, results}));
});
