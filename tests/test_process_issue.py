import importlib.util
import json
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("process_issue", ROOT / "scripts" / "process_issue.py")
process_issue = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(process_issue)


class UnitTests(unittest.TestCase):
    def test_slugify_removes_accents_and_punctuation(self):
        self.assertEqual(process_issue.slugify("Criptografia & Ontologias"), "criptografia-ontologias")

    def test_slugify_has_safe_fallback(self):
        self.assertEqual(process_issue.slugify("🚀"), "untitled")

    def test_normalize_hierarchical_tag(self):
        self.assertEqual(process_issue.normalize_tag("Cloud/Kubernetes Segurança"), "cloud/kubernetes-seguranca")

    def test_wiki_alias_escapes_link_delimiters(self):
        self.assertEqual(process_issue.wiki_alias("DAB | MCP]"), r"DAB \| MCP\]")

    def test_parse_issue_form(self):
        fields = process_issue.parse_issue_form("### Domínio\n\nObservability\n\n### Tags\n\neBPF")
        self.assertEqual(fields["domain"], "Observability")
        self.assertEqual(fields["tags"], "eBPF")

    def test_markdown_heading_inside_research_is_preserved(self):
        body = (
            "### Pesquisa integral\n\nIntrodução\n\n### Instalação\n\n"
            "Execute o comando.\n\n### Confirmações\n\n- [x] Revisado"
        )
        fields = process_issue.parse_issue_form(body)
        self.assertEqual(
            fields["research"],
            "Introdução\n\n### Instalação\n\nExecute o comando.",
        )

    def test_issue_must_be_ready(self):
        payload = json.loads((ROOT / "tests" / "fixtures" / "issue.json").read_text())
        payload["issue"]["labels"] = []
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            event = root / "event.json"
            event.write_text(json.dumps(payload), encoding="utf-8")
            with self.assertRaises(process_issue.IngestError):
                process_issue.process(event, root)

    def test_empty_form_title_is_rejected(self):
        payload = json.loads((ROOT / "tests" / "fixtures" / "issue.json").read_text())
        payload["issue"]["title"] = "[Research]: "
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            event = root / "event.json"
            event.write_text(json.dumps(payload), encoding="utf-8")
            with self.assertRaises(process_issue.IngestError):
                process_issue.process(event, root)


class IntegrationTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.root = Path(self.temporary.name)
        self.event = ROOT / "tests" / "fixtures" / "issue.json"

    def tearDown(self):
        self.temporary.cleanup()

    def test_ingest_writes_source_manifest_and_moc(self):
        entry = process_issue.process(self.event, self.root)
        note = self.root / entry["path"]
        manifest = self.root / "data" / "manifest.json"
        moc = self.root / "vault" / "30-mocs" / "domain-observability.md"
        self.assertTrue(note.exists())
        self.assertTrue(manifest.exists())
        self.assertTrue(moc.exists())
        content = note.read_text(encoding="utf-8")
        self.assertIn('evidence_status: "unverified"', content)
        self.assertIn("eBPF permite executar", content)
        self.assertIn("Captura bruta da Issue", content)

    def test_ingest_is_idempotent(self):
        process_issue.process(self.event, self.root)
        first = {
            path.relative_to(self.root): path.read_bytes()
            for path in self.root.rglob("*")
            if path.is_file()
        }
        process_issue.process(self.event, self.root)
        second = {
            path.relative_to(self.root): path.read_bytes()
            for path in self.root.rglob("*")
            if path.is_file()
        }
        self.assertEqual(first, second)

    def test_title_change_keeps_existing_path(self):
        first = process_issue.process(self.event, self.root)
        payload = json.loads(self.event.read_text(encoding="utf-8"))
        payload["issue"]["title"] = "[Research]: Novo título"
        changed_event = self.root / "changed.json"
        changed_event.write_text(json.dumps(payload), encoding="utf-8")
        second = process_issue.process(changed_event, self.root)
        self.assertEqual(first["path"], second["path"])
        self.assertIn("# Novo título", (self.root / second["path"]).read_text(encoding="utf-8"))

    def test_domain_change_removes_obsolete_generated_moc(self):
        process_issue.process(self.event, self.root)
        payload = json.loads(self.event.read_text(encoding="utf-8"))
        payload["issue"]["body"] = payload["issue"]["body"].replace("Observability", "Security", 1)
        changed_event = self.root / "changed.json"
        changed_event.write_text(json.dumps(payload), encoding="utf-8")
        process_issue.process(changed_event, self.root)
        self.assertFalse((self.root / "vault" / "30-mocs" / "domain-observability.md").exists())
        self.assertTrue((self.root / "vault" / "30-mocs" / "domain-security.md").exists())

    def test_manifest_rejects_unknown_schema(self):
        manifest = self.root / "data" / "manifest.json"
        manifest.parent.mkdir(parents=True)
        manifest.write_text('{"schema_version": 99, "sources": []}', encoding="utf-8")
        with self.assertRaises(process_issue.IngestError):
            process_issue.process(self.event, self.root)

    def test_manifest_cannot_redirect_source_outside_vault(self):
        manifest = self.root / "data" / "manifest.json"
        manifest.parent.mkdir(parents=True)
        manifest.write_text(
            json.dumps(
                {
                    "schema_version": 1,
                    "sources": [
                        {"id": "gh-issue-123", "path": "../../escaped.md", "source_issue": 123}
                    ],
                }
            ),
            encoding="utf-8",
        )
        with self.assertRaises(process_issue.IngestError):
            process_issue.process(self.event, self.root)
        self.assertFalse((self.root.parent / "escaped.md").exists())


class CommentIntegrationTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.root = Path(self.temporary.name)
        self.issue_event = ROOT / "tests" / "fixtures" / "issue.json"
        self.comment_event = ROOT / "tests" / "fixtures" / "comment.json"

    def tearDown(self):
        self.temporary.cleanup()

    def ingest_parent(self):
        return process_issue.process(self.issue_event, self.root)

    def test_comment_creates_linked_note_and_inherits_metadata(self):
        parent = self.ingest_parent()
        entry = process_issue.process_comment(self.comment_event, self.root)
        note = self.root / entry["path"]
        content = note.read_text(encoding="utf-8")
        manifest = json.loads((self.root / "data" / "manifest.json").read_text(encoding="utf-8"))
        moc = (self.root / "vault" / "30-mocs" / "domain-observability.md").read_text(encoding="utf-8")

        self.assertEqual(entry["domain"], parent["domain"])
        self.assertEqual(entry["title"], "Complemento à Issue #123: Observabilidade com eBPF")
        self.assertIn("source/github-comment", entry["tags"])
        self.assertEqual(len(manifest["sources"]), 2)
        self.assertIn("OpenTelemetry também pode receber", content)
        self.assertIn("[[../gh-issue-123-observabilidade-com-ebpf", content)
        self.assertIn("../10-sources/github/comments/gh-comment-987654321", moc)
        self.assertIn("Comentário #987654321 · Issue #123", moc)

    def test_edited_comment_updates_same_note_idempotently(self):
        self.ingest_parent()
        first = process_issue.process_comment(self.comment_event, self.root)
        payload = json.loads(self.comment_event.read_text(encoding="utf-8"))
        payload["action"] = "edited"
        payload["comment"]["body"] = "/knowledge\n\nConteúdo revisado."
        payload["comment"]["updated_at"] = "2026-11-07T10:00:00Z"
        edited_event = self.root / "edited-comment.json"
        edited_event.write_text(json.dumps(payload), encoding="utf-8")

        second = process_issue.process_comment(edited_event, self.root)
        manifest = json.loads((self.root / "data" / "manifest.json").read_text(encoding="utf-8"))
        matching = [item for item in manifest["sources"] if item["id"] == first["id"]]
        self.assertEqual(first["path"], second["path"])
        self.assertEqual(len(matching), 1)
        self.assertIn("Conteúdo revisado.", (self.root / second["path"]).read_text(encoding="utf-8"))

    def test_comment_without_command_is_rejected(self):
        self.ingest_parent()
        payload = json.loads(self.comment_event.read_text(encoding="utf-8"))
        payload["comment"]["body"] = "Comentário comum."
        event = self.root / "ordinary-comment.json"
        event.write_text(json.dumps(payload), encoding="utf-8")
        with self.assertRaises(process_issue.IngestError):
            process_issue.process_comment(event, self.root)

    def test_comment_requires_ingested_parent(self):
        with self.assertRaises(process_issue.IngestError):
            process_issue.process_comment(self.comment_event, self.root)

    def test_pull_request_comment_is_rejected(self):
        self.ingest_parent()
        payload = json.loads(self.comment_event.read_text(encoding="utf-8"))
        payload["issue"]["pull_request"] = {"url": "https://api.github.com/pulls/123"}
        event = self.root / "pr-comment.json"
        event.write_text(json.dumps(payload), encoding="utf-8")
        with self.assertRaises(process_issue.IngestError):
            process_issue.process_comment(event, self.root)


if __name__ == "__main__":
    unittest.main()
