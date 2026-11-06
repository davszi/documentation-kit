"""Generator tooling: SVG figure helpers, verbatim block locks and number ledgers."""
import json
from pathlib import Path
import sys
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tooling"))
import number_ledger  # noqa: E402
import svg_figures  # noqa: E402
import verbatim_blocks  # noqa: E402


def drawing(title="Rates and draws", desc="Two bars."):
    parts = svg_figures.svg_open(100, 40, title, desc)
    parts.append(svg_figures.text(4, 20, "rate 0.1", fill="var(--accent,#39d2c0)"))
    return "\n".join(parts + ["</svg>"])


class SvgFigures(unittest.TestCase):
    def test_figure_numbers_caption_and_labels_once(self):
        out = svg_figures.figure("rates", "R1", drawing(title="Rates' draws"), "Caption with <a href=\"#x\">a link</a>.")
        self.assertIn('<figure class="network-plate" id="rates">', out)
        self.assertIn('aria-label="Rates&#x27; draws"', out)
        self.assertNotIn("&amp;#x27;", out)
        self.assertIn('<figcaption><b>Figure R1.</b> Caption with <a href="#x">a link</a>.</figcaption>', out)
        self.assertNotIn("{id}", out)

    def test_slide_has_no_ids_and_standalone_resolves_variables(self):
        slide = svg_figures.slide_svg(drawing())
        self.assertNotIn(" id=", slide)
        self.assertIn('aria-label="Two bars."', slide)
        image = svg_figures.standalone(drawing())
        self.assertIn('xmlns="http://www.w3.org/2000/svg"', image)
        self.assertNotIn("var(--", image)
        self.assertIn('fill="#39d2c0"', image)


class SvgEdges(unittest.TestCase):
    def test_standalone_after_a_comment_and_slide_after_figure_ids(self):
        header = svg_figures.generated_header("make.py", ["data.json"])
        image = svg_figures.standalone(header + '<svg\n viewBox="0 0 4 4" xmlns="http://www.w3.org/2000/svg"><rect/></svg>')
        self.assertEqual(image.count("xmlns="), 1)
        plain = svg_figures.standalone(header + '<svg viewBox="0 0 4 4"><rect/></svg>')
        self.assertEqual(plain.count('xmlns="http://www.w3.org/2000/svg"'), 1)
        named = drawing(desc='Quote " and <tag>').replace("{id}", "fig")
        slide = svg_figures.slide_svg(named)
        self.assertNotIn("aria-labelledby", slide)
        self.assertIn('aria-label="Quote &quot; and &lt;tag&gt;"', slide)


class VerbatimBlocks(unittest.TestCase):
    SOURCE = "<p>Intro.</p>\n<p>The audit covered 72 settings.</p>\n<p>End.</p>\n"

    def test_lock_passes_then_detects_edits_and_ambiguity(self):
        spans = [("<p>The audit covered", "</p>", True)]
        locks = [(s, e, i, verbatim_blocks.digest(verbatim_blocks.block(self.SOURCE, s, e, i))) for s, e, i in spans]
        self.assertEqual(verbatim_blocks.verify(self.SOURCE, locks), [])
        self.assertEqual(len(verbatim_blocks.verify(self.SOURCE.replace("72", "73"), locks)), 1)
        self.assertIn("occurs 2 times", verbatim_blocks.verify(self.SOURCE * 2, locks)[0])
        self.assertIn("The audit covered", verbatim_blocks.lock_lines(self.SOURCE, spans))


class NumberLedger(unittest.TestCase):
    def setUp(self):
        self.folder = tempfile.TemporaryDirectory()
        self.addCleanup(self.folder.cleanup)
        self.root = Path(self.folder.name)
        (self.root / "config.json").write_text(json.dumps({"axes": {"support": [4, 16, 64]}, "rule": "levels 20/60/180"}))
        (self.root / "record.json").write_text(json.dumps({"mean": 0.0314525}))
        (self.root / "pinned.html").write_text("<p>Pinned 999.</p>")
        self.evidence = {"data": {"lower": 139, "total": 144, "ratios": ["0.61", "0.51"]}}

    def ledger(self, facts):
        return {"chapter": "results", "config": "config.json", "facts": facts}

    def test_every_kind_checks_its_value(self):
        markup = ("<section><p>139 of 144 settings; K 16; levels 20 and 60; mean 0.0314525; ratios 0.61 and 0.51;"
                  " tick 10; 1,000 cursors.</p><p>Pinned 999.</p><p>Kept 555.</p><script>var x = 77;</script></section>")
        facts = [{"value": "139", "kind": "extract", "expr": "data['lower']"},
                 {"value": "144", "kind": "extract", "expr": "data['total']"},
                 {"value": "16", "kind": "config", "pointer": "/axes/support/1"},
                 {"value": "20", "kind": "config_text", "pointer": "/rule"},
                 {"value": "60", "kind": "arithmetic", "expr": "cfg['axes']['support'][0] * 15"},
                 {"value": "0.0314525", "kind": "record", "file": "record.json", "pointer": "/mean"},
                 {"kind": "extract_set", "expr": "data['ratios']", "note": "ratios"},
                 {"value": "10", "kind": "teaching", "note": "axis tick"},
                 {"value": "1000", "kind": "arithmetic", "expr": "10 ** 3"},
                 {"kind": "pinned_fragment", "file": "pinned.html"},
                 {"kind": "kept_block", "start": "<p>Kept", "end": "</p>"}]
        problems = number_ledger.check(markup, self.ledger(facts), root=self.root, evidence=self.evidence,
                                       pinned={"pinned.html"}, kept={("<p>Kept", "</p>")})
        self.assertEqual(problems, [])

    def test_unlisted_wrong_and_stale_values_are_reported(self):
        markup = "<p>139 of 145 settings.</p>"
        facts = [{"value": "139", "kind": "extract", "expr": "data['total']"},
                 {"value": "7", "kind": "teaching", "note": "gone"},
                 {"value": "1", "kind": "teaching"}]
        problems = number_ledger.check(markup, self.ledger(facts), root=self.root, evidence=self.evidence)
        joined = "\n".join(problems)
        self.assertIn("139: extract source does not give this value", joined)
        self.assertIn("145: shown without a ledger source", joined)
        self.assertIn("7: in the ledger but no longer shown", joined)
        self.assertIn("1: teaching source does not give this value", joined)

    def test_expressions_get_no_builtins_but_are_not_a_sandbox(self):
        # Builtins are absent by convenience only; ledger expressions are reviewed project code.
        facts = [{"value": "1", "kind": "extract", "expr": "__import__('os').getpid()"}]
        problems = number_ledger.check("<p>1</p>", self.ledger(facts), root=self.root, evidence=self.evidence)
        self.assertIn("NameError", problems[0])
        self.assertIn("not a sandbox", number_ledger.__doc__)

    def test_distinct_unsigned_values_and_comma_forms(self):
        markup = "<p>3 seeds, 3 failures; change −0.5; 1,036 cursors.</p>"
        facts = [{"value": "3", "kind": "teaching", "note": "count"},
                 {"value": "0.5", "kind": "teaching", "note": "unsigned"},
                 {"value": "1,036", "kind": "arithmetic", "expr": "1036"}]
        self.assertEqual(number_ledger.check(markup, self.ledger(facts), root=self.root), [])
        twice = number_ledger.check(markup, self.ledger(facts + [{"value": "3", "kind": "teaching", "note": "again"}]),
                                    root=self.root)
        self.assertIn("3: listed twice", twice)

    def test_kept_block_edges_are_reported_not_raised(self):
        kept = {("<p>Kept", "</p>"), ("<p>Keep", "<b>")}
        missing_end = [{"kind": "kept_block", "start": "<p>Kept", "end": "</p>"}]
        problems = number_ledger.check("<p>Kept 5", self.ledger(missing_end), root=self.root, kept=kept)
        self.assertIn("no longer follows the start", problems[0])
        exclusive = [{"kind": "kept_block", "start": "<p>Keep", "end": "<b>", "inclusive": False}]
        problems = number_ledger.check("<p>Keep 8 <b>9</b></p>", self.ledger(exclusive), root=self.root, kept=kept)
        self.assertEqual(problems, ["9: shown without a ledger source"])

    def test_unlocked_fragment_cannot_be_removed(self):
        facts = [{"kind": "pinned_fragment", "file": "pinned.html"}]
        problems = number_ledger.check("<p>Pinned 999.</p>", self.ledger(facts), root=self.root)
        self.assertIn("not a locked fragment", problems[0])
        self.assertIn("999: shown without a ledger source", problems[-1])


if __name__ == "__main__":
    unittest.main()
