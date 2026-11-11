// Logic checks for theme/components/panel-switcher.js without a browser: two
// independent switchers on a synthetic page, buttons, print, hash deep links
// and malformed hashes. Real-browser behaviour stays in test_panel_switcher.cjs.
// Ported from ADP's experiments/track_geometry/test_width_examples_ui.cjs
// (lines 30-59) at commit e21c2e84. READER_LOGIC_COMPONENTS points the check
// at another copy of theme/components, which is how mutation checks run.
const fs = require('node:fs');
const path = require('node:path');
const vm = require('node:vm');
const assert = require('node:assert/strict');

const components = process.env.READER_LOGIC_COMPONENTS
  ? path.resolve(process.env.READER_LOGIC_COMPONENTS)
  : path.resolve(__dirname, '../theme/components');
const script = fs.readFileSync(path.join(components, 'panel-switcher.js'), 'utf8');

class Panel {
  constructor(value, id) { Object.assign(this, {dataset: {panel: value}, id, hidden: false}); }
  // Each panel holds one inner anchor, `<panel id>-anchor`.
  contains(target) { return target === this || target?.parent === this; }
}
class ChoiceButton {
  constructor(value) { Object.assign(this, {dataset: {panelChoice: value}, attrs: {}, listeners: {}}); }
  setAttribute(key, value) { this.attrs[key] = String(value); }
  addEventListener(type, listener) { this.listeners[type] = listener; }
  click() { this.listeners.click(); }
}

// Two switchers: the first defaults to its first panel, the second has three.
const SWITCHERS = [['coarse', 'dense'], ['narrowing', 'dip', 'bend']];

function boot(hash = '') {
  const roots = SWITCHERS.map((values, index) => {
    const panels = values.map(value => new Panel(value, `panel-${index}-${value}`));
    const buttons = values.map(value => new ChoiceButton(value));
    return {
      dataset: {panelDefault: values[0]}, panels, buttons,
      querySelectorAll: selector => {
        if (selector === '[data-panel-choice]') return buttons;
        assert.equal(selector, '[data-panel]', 'The switcher looks up panels by data-panel');
        return panels;
      },
    };
  });
  const document = {
    querySelectorAll: selector => {
      assert.equal(selector, '[data-panel-switcher]', 'The switcher finds its roots by data-panel-switcher');
      return roots;
    },
    getElementById(id) {
      for (const panel of roots.flatMap(root => root.panels)) {
        if (panel.id === id) return panel;
        if (id === panel.id + '-anchor') return {parent: panel};
      }
      return null;
    },
  };
  const listeners = {};
  const window = {addEventListener: (type, listener) => (listeners[type] ??= []).push(listener)};
  const location = {hash};
  vm.runInNewContext(script, {document, window, location});
  const fire = type => (listeners[type] || []).forEach(listener => listener());
  const shown = () => roots.map(root => root.panels.find(panel => !panel.hidden)?.dataset.panel);
  return {roots, location, fire, shown};
}

const page = boot();
assert.deepEqual(page.shown(), ['coarse', 'narrowing'], 'Each switcher starts on its default panel');
for (const root of page.roots) {
  assert.equal(root.dataset.panelReady, 'true', 'A switcher marks itself ready');
  for (const button of root.buttons) {
    button.click();
    for (const panel of root.panels) {
      assert.equal(panel.hidden, panel.dataset.panel !== button.dataset.panelChoice, 'A choice shows only its own panel');
    }
    for (const other of root.buttons) {
      assert.equal(other.attrs['aria-pressed'], String(other === button), 'Only the chosen button is pressed');
    }
  }
}
assert.equal(page.shown()[0], 'dense', 'Choosing in one switcher leaves the other switcher alone');

const beforePrint = page.roots.map(root => root.panels.map(panel => panel.hidden));
page.fire('beforeprint');
assert.ok(page.roots.every(root => root.panels.every(panel => !panel.hidden)), 'Print shows every panel');
page.fire('afterprint');
assert.deepEqual(page.roots.map(root => root.panels.map(panel => panel.hidden)), beforePrint,
  'After print each switcher returns to its choice');

const linked = boot('#panel-1-dip-anchor');
assert.deepEqual(linked.shown(), ['coarse', 'dip'], 'A hash naming an anchor inside a panel selects that panel at load');
linked.location.hash = '#panel-0-dense';
linked.fire('hashchange');
assert.deepEqual(linked.shown(), ['dense', 'dip'], 'A hash change naming a panel selects it');
linked.location.hash = '#%';
assert.doesNotThrow(() => linked.fire('hashchange'), 'A malformed hash must not throw');
assert.deepEqual(linked.shown(), ['dense', 'dip'], 'A malformed hash changes nothing and does not throw');

assert.ok(!/\b(?:fetch|XMLHttpRequest|WebSocket)\s*\(/.test(script), 'panel-switcher.js makes no network request');
console.log('Panel switcher logic checks pass: defaults, independent switchers, pressed state, print show and restore, '
  + 'hash deep links at load and on change, malformed hashes, no network requests.');
