#!/usr/bin/env python3
"""Turn a GitHub Issue event into a source note and deterministic MOCs.

Only the Python standard library is used. Issue content is treated as data: it
is never evaluated, rendered as a template, or passed to a shell.
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import re
import sys
import tempfile
import unicodedata
from pathlib import Path
from typing import Any

READY_LABEL = "knowledge/ready"
SCHEMA_VERSION = 1
FIELD_ALIASES = {
    "domain": ("domain", "domínio", "dominio"),
    "provider": ("ai provider", "provedor de ia", "provider", "provedor"),
    "tags": ("tags", "etiquetas"),
    "references": ("references", "referências", "referencias"),
    "research": (
        "pesquisa integral",
        "full research",
        "research",
        "pesquisa",
        "conteúdo",
        "conteudo",
    ),
}
FIELD_BY_HEADING = {
    alias.casefold(): field
    for field, aliases in FIELD_ALIASES.items()
    for alias in aliases
}
FORM_STOP_HEADINGS = {
    "confirmações",
    "confirmacoes",
    "confirmations",
    "safety",
}
EMPTY_VALUES = {"", "_no response_", "_nenhuma resposta_", "n/a", "none"}


class IngestError(ValueError):
    """Raised when an event cannot safely be ingested."""


def slugify(value: str, *, fallback: str = "untitled", limit: int = 80) -> str:
    normalized = unicodedata.normalize("NFKD", value)
    ascii_value = normalized.encode("ascii", "ignore").decode("ascii").lower()
    slug = re.sub(r"[^a-z0-9]+", "-", ascii_value).strip("-")
    return (slug[:limit].rstrip("-") or fallback)


def normalize_tag(value: str) -> str:
    parts = [slugify(part, fallback="tag", limit=40) for part in value.split("/")]
    return "/".join(part for part in parts if part)


def parse_issue_form(body: str) -> dict[str, str]:
    """Parse GitHub Issue Form output (`### heading` followed by its value)."""
    sections: dict[str, list[str]] = {}
    current: str | None = None
    for line in body.splitlines():
        match = re.match(r"^###\s+(.+?)\s*$", line)
        if match:
            heading = match.group(1).strip().casefold()
            if heading in FIELD_BY_HEADING:
                current = FIELD_BY_HEADING[heading]
                sections.setdefault(current, [])
            elif heading in FORM_STOP_HEADINGS:
                current = None
            elif current is not None:
                # Markdown headings inside a field are content, not form keys.
                sections[current].append(line)
        elif current is not None:
            sections[current].append(line)

    result: dict[str, str] = {}
    for field, lines in sections.items():
        value = "\n".join(lines).strip()
        if value.casefold() not in EMPTY_VALUES:
            result[field] = value
    return result


def label_names(issue: dict[str, Any]) -> set[str]:
    names: set[str] = set()
    for label in issue.get("labels") or []:
        if isinstance(label, str):
            names.add(label)
        elif isinstance(label, dict) and isinstance(label.get("name"), str):
            names.add(label["name"])
    return names


def issue_from_payload(payload: Any) -> dict[str, Any]:
    if not isinstance(payload, dict):
        raise IngestError("event payload must be a JSON object")
    issue = payload.get("issue", payload)
    if not isinstance(issue, dict):
        raise IngestError("event does not contain an issue object")
    if not isinstance(issue.get("number"), int) or issue["number"] <= 0:
        raise IngestError("issue.number must be a positive integer")
    if not isinstance(issue.get("title"), str) or not issue["title"].strip():
        raise IngestError("issue.title must be a non-empty string")
    if not isinstance(issue.get("body"), str) or not issue["body"].strip():
        raise IngestError("issue.body must be a non-empty string")
    return issue


def parse_date(value: Any) -> str:
    if isinstance(value, str):
        try:
            return dt.datetime.fromisoformat(value.replace("Z", "+00:00")).date().isoformat()
        except ValueError:
            pass
    return dt.datetime.now(dt.timezone.utc).date().isoformat()


def yaml_string(value: str) -> str:
    """JSON strings are valid YAML double-quoted scalars."""
    return json.dumps(value, ensure_ascii=False)


def parse_tags(raw: str, domain: str) -> list[str]:
    candidates = re.split(r"[,;\n]+", raw)
    tags = [f"domain/{domain}", "source/ai"]
    tags.extend(normalize_tag(item.strip().lstrip("#")) for item in candidates if item.strip())
    return sorted(set(tag for tag in tags if tag))


def validate_source_path(value: str) -> str:
    """Allow only source-note paths in the canonical GitHub source folder."""
    path = Path(value)
    expected = Path("vault/10-sources/github")
    if path.is_absolute() or ".." in path.parts or path.parent != expected or path.suffix != ".md":
        raise IngestError("manifest contains an unsafe source path")
    return path.as_posix()


def render_source(entry: dict[str, Any], body: str, research: str, references: str) -> str:
    tags = "\n".join(f"  - {yaml_string(tag)}" for tag in entry["tags"])
    moc_link = f"[[../../30-mocs/domain-{entry['domain']}|{entry['domain']}]]"
    reference_block = references.strip() or "Nenhuma referência informada."
    return (
        "---\n"
        f"id: {yaml_string(entry['id'])}\n"
        f"title: {yaml_string(entry['title'])}\n"
        "kind: \"research-source\"\n"
        f"domain: {yaml_string(entry['domain'])}\n"
        "tags:\n"
        f"{tags}\n"
        f"ai_provider: {yaml_string(entry['ai_provider'])}\n"
        f"source_issue: {entry['source_issue']}\n"
        f"source_url: {yaml_string(entry['source_url'])}\n"
        f"created: {yaml_string(entry['created'])}\n"
        "status: \"captured\"\n"
        "evidence_status: \"unverified\"\n"
        "---\n\n"
        f"# {entry['title']}\n\n"
        f"> [!info] Proveniência\n"
        f"> Captura integral da Issue [#{entry['source_issue']}]({entry['source_url']}). "
        "O conteúdo e as referências ainda não foram verificados.\n\n"
        f"**Domínio:** {moc_link}\n\n"
        "## Pesquisa original\n\n"
        f"{research.strip()}\n\n"
        "## Referências informadas\n\n"
        f"{reference_block}\n\n"
        "## Captura bruta da Issue\n\n"
        "<details>\n<summary>Exibir corpo original</summary>\n\n"
        f"{body.rstrip()}\n\n"
        "</details>\n"
    )


def load_manifest(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {"schema_version": SCHEMA_VERSION, "sources": []}
    try:
        manifest = json.loads(path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError) as exc:
        raise IngestError(f"cannot read manifest: {exc}") from exc
    if manifest.get("schema_version") != SCHEMA_VERSION or not isinstance(manifest.get("sources"), list):
        raise IngestError("unsupported or invalid manifest schema")
    return manifest


def atomic_write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    descriptor, temporary = tempfile.mkstemp(prefix=f".{path.name}.", dir=path.parent)
    try:
        with os.fdopen(descriptor, "w", encoding="utf-8", newline="\n") as handle:
            handle.write(content)
        os.replace(temporary, path)
    except BaseException:
        try:
            os.unlink(temporary)
        except FileNotFoundError:
            pass
        raise


def write_manifest(path: Path, manifest: dict[str, Any]) -> None:
    manifest["sources"] = sorted(manifest["sources"], key=lambda item: item["source_issue"])
    atomic_write(path, json.dumps(manifest, ensure_ascii=False, indent=2, sort_keys=True) + "\n")


def rebuild_mocs(root: Path, sources: list[dict[str, Any]]) -> None:
    moc_dir = root / "vault" / "30-mocs"
    grouped: dict[str, list[dict[str, Any]]] = {}
    for source in sources:
        grouped.setdefault(source["domain"], []).append(source)

    expected: set[Path] = set()
    for domain, entries in sorted(grouped.items()):
        path = moc_dir / f"domain-{domain}.md"
        expected.add(path)
        lines = [
            "---",
            f"title: {yaml_string('MOC: ' + domain)}",
            'kind: "moc"',
            f"domain: {yaml_string(domain)}",
            "tags:",
            f"  - {yaml_string('moc/' + domain)}",
            "generated: true",
            "---",
            "",
            f"# {domain}",
            "",
            "> [!warning] Gerado automaticamente",
            "> Este índice é reconstruído a partir de `data/manifest.json`.",
            "",
            "## Pesquisas",
            "",
        ]
        for entry in sorted(entries, key=lambda item: (item["created"], item["title"].casefold()), reverse=True):
            note_name = Path(entry["path"]).stem
            lines.append(
                f"- [[../10-sources/github/{note_name}|{entry['title']}]] "
                f"— {entry['created']} · Issue #{entry['source_issue']}"
            )
        lines.append("")
        atomic_write(path, "\n".join(lines))

    if moc_dir.exists():
        for path in moc_dir.glob("domain-*.md"):
            if path not in expected:
                path.unlink()


def process(event_path: Path, root: Path, *, allow_unready: bool = False) -> dict[str, Any]:
    try:
        payload = json.loads(event_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise IngestError(f"cannot read event JSON: {exc}") from exc

    issue = issue_from_payload(payload)
    if not allow_unready and READY_LABEL not in label_names(issue):
        raise IngestError(f"issue must have the {READY_LABEL!r} label")

    fields = parse_issue_form(issue["body"])
    domain = slugify(fields.get("domain", "uncategorized"), fallback="uncategorized", limit=50)
    title = re.sub(r"^\[research\]:\s*", "", issue["title"].strip(), flags=re.IGNORECASE).strip()
    if not title:
        raise IngestError("issue title is empty after removing the form prefix")
    provider = fields.get("provider", "Unknown").splitlines()[0].strip()
    research = fields.get("research", issue["body"])
    references = fields.get("references", "")
    tags = parse_tags(fields.get("tags", ""), domain)
    issue_number = issue["number"]
    source_id = f"gh-issue-{issue_number}"

    manifest_path = root / "data" / "manifest.json"
    manifest = load_manifest(manifest_path)
    previous = next((item for item in manifest["sources"] if item.get("id") == source_id), None)
    relative_path = (
        validate_source_path(previous["path"])
        if previous and isinstance(previous.get("path"), str)
        else f"vault/10-sources/github/{source_id}-{slugify(title)}.md"
    )
    entry = {
        "ai_provider": provider,
        "created": parse_date(issue.get("created_at")),
        "domain": domain,
        "id": source_id,
        "path": relative_path,
        "source_issue": issue_number,
        "source_url": str(issue.get("html_url") or f"https://github.com/issues/{issue_number}"),
        "status": "captured",
        "tags": tags,
        "title": title,
    }

    source_path = root / relative_path
    atomic_write(source_path, render_source(entry, issue["body"], research, references))
    manifest["sources"] = [item for item in manifest["sources"] if item.get("id") != source_id]
    manifest["sources"].append(entry)
    write_manifest(manifest_path, manifest)
    rebuild_mocs(root, manifest["sources"])
    return entry


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--event", required=True, type=Path, help="GitHub event or issue JSON")
    parser.add_argument("--root", default=Path.cwd(), type=Path, help="repository root")
    parser.add_argument(
        "--allow-unready",
        action="store_true",
        help=f"allow issues without {READY_LABEL!r}; intended for local development",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        entry = process(args.event.resolve(), args.root.resolve(), allow_unready=args.allow_unready)
    except IngestError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2
    print(json.dumps(entry, ensure_ascii=False, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
