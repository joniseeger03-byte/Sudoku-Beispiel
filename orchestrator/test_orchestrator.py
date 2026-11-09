import io
import json
import os
import pathlib
import sys
import unittest
import urllib.error
from unittest.mock import patch

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "orchestrator"))

import agents  # noqa: E402
import graph  # noqa: E402
import run  # noqa: E402


class GraphTest(unittest.TestCase):
    def test_kanten_verbinden_bekannte_knoten(self):
        for von, nach, art, _ in graph.KANTEN:
            self.assertIn(von, graph.KNOTEN)
            self.assertIn(nach, graph.KNOTEN)
            self.assertIn(art, ("", "bedingt", "schleife"))

    def test_jeder_knoten_hat_eine_bekannte_phase(self):
        phasen = {p for p, _ in graph.PHASEN}
        for k in graph.KNOTEN.values():
            self.assertIn(k["phase"], phasen)

    def test_modellknoten_haben_prompt_rolle_und_demo_antwort(self):
        cfg = json.loads((ROOT / "config.json").read_text(encoding="utf-8"))
        for name, k in graph.KNOTEN.items():
            if k["art"] not in ("modell", "agent"):
                continue
            self.assertTrue((ROOT / "prompts" / k["prompt"]).is_file(), k["prompt"])
            self.assertIn(name, cfg["rollen"], f"Rolle {name} fehlt in config.json")
            demo = (run.DEMO / "texte" / f"{name}.md").exists() or name in run.DEMO_CODE
            self.assertTrue(demo, f"Demo-Antwort für {name} fehlt")

    def test_positionen_sind_eindeutig(self):
        pos = [tuple(k["pos"]) for k in graph.KNOTEN.values()]
        self.assertEqual(len(pos), len(set(pos)))


class HarnessTest(unittest.TestCase):
    def test_codebloecke_nach_sprache(self):
        text = "Hier:\n```html\n<p>x</p>\n```\n\n```javascript\nlet a = 1\n```\n```css\np{}\n```"
        self.assertEqual(run.codebloecke(text), [("html", "<p>x</p>"), ("javascript", "let a = 1"), ("css", "p{}")])

    def test_zaun_im_fliesstext_ist_kein_block(self):
        text = "Die Datei enthält Fences (```python```) und ist kaputt.\n\n**URTEIL:** test\n\n```python\nimport engine\n```"
        self.assertEqual(run.codebloecke(text), [("python", "import engine")])

    def test_abgeschnittener_block_zaehlt_bis_zum_ende(self):
        self.assertEqual(run.codebloecke("```python\nfor x in y:\n    for"), [("python", "for x in y:\n    for")])

    def test_urteil(self):
        self.assertEqual(run.urteil("bla\nURTEIL: ok", ["ok", "nacharbeiten"]), "ok")
        self.assertEqual(run.urteil("**URTEIL:** nacharbeiten", ["ok", "nacharbeiten"]), "nacharbeiten")
        self.assertIsNone(run.urteil("alles gut", ["ok", "nacharbeiten"]))


class AgentsTest(unittest.TestCase):
    cfg = {"anbieter": {
        "groq": {"url": "https://api.groq.com/openai/v1", "key": "GROQ_API_KEY", "modell": "a"},
        "openrouter": {"url": "https://openrouter.ai/api/v1", "key": "OPENROUTER_API_KEY", "modell": "b"},
    }}

    def fehler(self, code):
        def fake(req, timeout=300):
            raise urllib.error.HTTPError(req.full_url, code, "x", hdrs=None, fp=io.BytesIO(b"nope"))
        return fake

    def test_401_weicht_nicht_aus(self):
        with patch.dict(os.environ, {"GROQ_API_KEY": "g", "OPENROUTER_API_KEY": "o"}), \
                patch("agents.urllib.request.urlopen", side_effect=self.fehler(401)) as m:
            with self.assertRaises(agents.ApiFehler):
                agents.api_call(self.cfg, "groq", "Hallo")
            self.assertEqual(m.call_count, 1)

    def test_check_weicht_nie_aus(self):
        with patch.dict(os.environ, {"GROQ_API_KEY": "g", "OPENROUTER_API_KEY": "o"}), \
                patch("agents.urllib.request.urlopen", side_effect=self.fehler(403)) as m:
            with self.assertRaises(agents.ApiFehler):
                agents.api_call(self.cfg, "groq", "Hallo", ausweichen=False)
            self.assertEqual(m.call_count, 1)

    def test_claude_ist_kein_ausweichziel(self):
        cfg = {"anbieter": {**self.cfg["anbieter"], "claude": {"typ": "claude-code", "modell": "sonnet"}}}
        with patch.dict(os.environ, {"GROQ_API_KEY": "g", "OPENROUTER_API_KEY": "o"}), \
                patch("agents.urllib.request.urlopen", side_effect=self.fehler(503)) as m:
            with self.assertRaises(agents.ApiFehler):
                agents.api_call(cfg, "groq", "Hallo")
            self.assertEqual(m.call_count, 2)

    def test_agent_bekommt_werkzeuge_urteiler_nicht(self):
        a = {"typ": "claude-code", "modell": "sonnet"}
        self.assertIn("--allowedTools", agents.claude_befehl(a, True))
        self.assertNotIn("--allowedTools", agents.claude_befehl(a, False))

    def test_wechsel_wird_gemeldet(self):
        gemeldet = []
        with patch.dict(os.environ, {"GROQ_API_KEY": "", "OPENROUTER_API_KEY": "o"}), \
                patch("agents.urllib.request.urlopen", side_effect=self.fehler(503)):
            with self.assertRaises(agents.ApiFehler):
                agents.api_call(self.cfg, "groq", "Hallo", wechsel=lambda *a: gemeldet.append(a[:2]))
        self.assertEqual(gemeldet, [("groq", "openrouter")])


if __name__ == "__main__":
    unittest.main()
