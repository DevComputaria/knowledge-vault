#!/usr/bin/env python3
"""Turn a GitHub Issue or opted-in comment into notes and deterministic MOCs.

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
KNOWLEDGE_COMMAND = "/knowledge"
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


def wiki_alias(value: str) -> str:
    """Escape characters with structural meaning in an Obsidian wikilink alias."""
    return value.replace("\\", "\\\\").replace("|", "\\|").replace("]", "\\]")


def validate_domain(value: Any) -> str:
    if not isinstance(value, str) or value != slugify(value, fallback="uncategorized", limit=50):
        raise IngestError("manifest contains an unsafe domain")
    return value


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


def validate_comment_path(value: str) -> str:
    """Allow only comment-note paths in the canonical comments folder."""
    path = Path(value)
    expected = Path("vault/10-sources/github/comments")
    if path.is_absolute() or ".." in path.parts or path.parent != expected or path.suffix != ".md":
        raise IngestError("manifest contains an unsafe comment path")
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


def extract_comment_content(body: Any) -> str:
    if not isinstance(body, str):
        raise IngestError("comment.body must be a string")
    match = re.match(r"^/knowledge(?:[ \t]*(?:\r?\n|$))", body, flags=re.IGNORECASE)
    if not match:
        raise IngestError(f"comment must start with {KNOWLEDGE_COMMAND!r} on its own line")
    content = body[match.end():].strip()
    if not content:
        raise IngestError("comment does not contain knowledge after the command")
    return content


def render_comment(entry: dict[str, Any], raw_body: str, content: str, parent: dict[str, Any]) -> str:
    tags = "\n".join(f"  - {yaml_string(tag)}" for tag in entry["tags"])
    parent_name = Path(parent["path"]).stem
    parent_link = f"[[../{parent_name}|{wiki_alias(parent['title'])}]]"
    moc_link = f"[[../../../30-mocs/domain-{entry['domain']}|{entry['domain']}]]"
    return (
        "---\n"
        f"id: {yaml_string(entry['id'])}\n"
        f"title: {yaml_string(entry['title'])}\n"
        "kind: \"research-comment\"\n"
        f"domain: {yaml_string(entry['domain'])}\n"
        "tags:\n"
        f"{tags}\n"
        f"source_issue: {entry['source_issue']}\n"
        f"source_comment: {entry['source_comment']}\n"
        f"parent_id: {yaml_string(entry['parent_id'])}\n"
        f"author: {yaml_string(entry['author'])}\n"
        f"source_url: {yaml_string(entry['source_url'])}\n"
        f"created: {yaml_string(entry['created'])}\n"
        f"updated: {yaml_string(entry['updated'])}\n"
        "status: \"captured\"\n"
        "evidence_status: \"unverified\"\n"
        "---\n\n"
        f"# {entry['title']}\n\n"
        "> [!info] Proveniência\n"
        f"> Comentário [#{entry['source_comment']}]({entry['source_url']}) de "
        f"@{entry['author']}, vinculado à Issue #{entry['source_issue']}. "
        "O conteúdo ainda não foi verificado.\n\n"
        f"**Pesquisa pai:** {parent_link}\n\n"
        f"**Domínio:** {moc_link}\n\n"
        "## Conhecimento capturado\n\n"
        f"{content}\n\n"
        "## Captura bruta do comentário\n\n"
        "<details>\n<summary>Exibir comentário original</summary>\n\n"
        f"{raw_body.rstrip()}\n\n"
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
    manifest["sources"] = sorted(
        manifest["sources"],
        key=lambda item: (
            item["source_issue"],
            1 if "source_comment" in item else 0,
            item.get("source_comment", 0),
            item["id"],
        ),
    )
    atomic_write(path, json.dumps(manifest, ensure_ascii=False, indent=2, sort_keys=True) + "\n")


def rebuild_mocs(root: Path, sources: list[dict[str, Any]]) -> None:
    moc_dir = root / "vault" / "30-mocs"
    grouped: dict[str, list[dict[str, Any]]] = {}
    for source in sources:
        domain = validate_domain(source.get("domain"))
        grouped.setdefault(domain, []).append(source)

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
            manifest_path = Path(entry["path"])
            if manifest_path.is_absolute() or ".." in manifest_path.parts or manifest_path.suffix != ".md":
                raise IngestError("manifest contains an unsafe note path")
            try:
                note_path = Path("..") / manifest_path.relative_to("vault")
            except ValueError as exc:
                raise IngestError("manifest contains a note path outside the vault") from exc
            provenance = (
                f"Comentário #{entry['source_comment']} · Issue #{entry['source_issue']}"
                if "source_comment" in entry
                else f"Issue #{entry['source_issue']}"
            )
            lines.append(
                f"- [[{note_path.as_posix()}|{wiki_alias(entry['title'])}]] "
                f"— {entry['created']} · {provenance}"
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


def process_comment(event_path: Path, root: Path) -> dict[str, Any]:
    try:
        payload = json.loads(event_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise IngestError(f"cannot read event JSON: {exc}") from exc

    issue = issue_from_payload(payload)
    if "pull_request" in issue:
        raise IngestError("pull request comments are not knowledge sources")
    comment = payload.get("comment") if isinstance(payload, dict) else None
    if not isinstance(comment, dict):
        raise IngestError("event does not contain a comment object")
    comment_id = comment.get("id")
    if not isinstance(comment_id, int) or comment_id <= 0:
        raise IngestError("comment.id must be a positive integer")
    raw_body = comment.get("body")
    content = extract_comment_content(raw_body)
    author = comment.get("user", {}).get("login") if isinstance(comment.get("user"), dict) else None
    if not isinstance(author, str) or not author.strip():
        raise IngestError("comment.user.login must be a non-empty string")

    manifest_path = root / "data" / "manifest.json"
    manifest = load_manifest(manifest_path)
    parent_id = f"gh-issue-{issue['number']}"
    parent = next((item for item in manifest["sources"] if item.get("id") == parent_id), None)
    if parent is None:
        raise IngestError("parent issue must be ingested before its comments")
    if not isinstance(parent.get("path"), str):
        raise IngestError("parent source has no valid path")
    validate_source_path(parent["path"])
    domain = validate_domain(parent.get("domain"))
    tags = parent.get("tags")
    parent_title = parent.get("title")
    if (
        not isinstance(tags, list)
        or not all(isinstance(tag, str) for tag in tags)
        or not isinstance(parent_title, str)
        or not parent_title
    ):
        raise IngestError("parent source has invalid title or tags")

    source_id = f"gh-comment-{comment_id}"
    previous = next((item for item in manifest["sources"] if item.get("id") == source_id), None)
    relative_path = (
        validate_comment_path(previous["path"])
        if previous and isinstance(previous.get("path"), str)
        else f"vault/10-sources/github/comments/{source_id}.md"
    )
    entry = {
        "author": author.strip(),
        "created": parse_date(comment.get("created_at")),
        "domain": domain,
        "id": source_id,
        "kind": "research-comment",
        "parent_id": parent_id,
        "path": relative_path,
        "source_comment": comment_id,
        "source_issue": issue["number"],
        "source_url": str(comment.get("html_url") or issue.get("html_url") or ""),
        "status": "captured",
        "tags": sorted(set(tags + ["source/github-comment"])),
        "title": f"Complemento à Issue #{issue['number']}: {parent_title}",
        "updated": parse_date(comment.get("updated_at") or comment.get("created_at")),
    }

    atomic_write(root / relative_path, render_comment(entry, raw_body, content, parent))
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
        "--comment",
        action="store_true",
        help=f"process an issue_comment event that starts with {KNOWLEDGE_COMMAND!r}",
    )
    parser.add_argument(
        "--allow-unready",
        action="store_true",
        help=f"allow issues without {READY_LABEL!r}; intended for local development",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        if args.comment:
            entry = process_comment(args.event.resolve(), args.root.resolve())
        else:
            entry = process(args.event.resolve(), args.root.resolve(), allow_unready=args.allow_unready)
    except IngestError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2
    print(json.dumps(entry, ensure_ascii=False, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
