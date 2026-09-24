#!/usr/bin/env python3
"""
glm_worker.py — Worker delegato per l'architettura multi-agente (Planner → Worker → Reviewer).

RUOLI
  Planner/Reviewer : Claude Code (scrive le istruzioni, revisiona, approva)
  Worker           : GLM (contesto lungo, costo basso) — scrive il codice

CONTRATTO
  `generate` NON tocca MAI i file di progetto: produce un patch JSON in staging.
  `apply`    applica il patch SOLO dopo revisione, con ancore testuali esatte.
             Rifiuta ancore mancanti o ambigue: fallisce rumorosamente, mai in silenzio.

USO
  export GLM_API_KEY="..."
  # opzionale: export GLM_BASE_URL / GLM_MODEL

  # 1) genera (Claude scrive task.md con istruzioni ferree)
  python3 glm_worker.py generate --task task.md --file css/styles.css --file index.html

  # 2) ispeziona il piano senza scrivere nulla
  python3 glm_worker.py apply --patch .glm/patch.json

  # 3) applica davvero (dopo la review di Claude)
  python3 glm_worker.py apply --patch .glm/patch.json --yes

  # utile: vedi il prompt senza spendere token
  python3 glm_worker.py generate --task task.md --file x.css --dry-run
"""

from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import sys
from datetime import datetime
from pathlib import Path

# --------------------------------------------------------------------------- #
# Config
# --------------------------------------------------------------------------- #

PROJECT_ROOT = Path(__file__).resolve().parent
STAGING_DIR = PROJECT_ROOT / ".glm"

# NB: verifica endpoint e model id sulla doc del provider — cambiano nel tempo.
#     Zhipu/Z.ai espongono un'API OpenAI-compatible.
DEFAULT_BASE_URL = os.environ.get("GLM_BASE_URL", "https://api.z.ai/api/paas/v4/")
DEFAULT_MODEL = os.environ.get("GLM_MODEL", "glm-4.6")

SYSTEM_PROMPT = """You are a senior implementation engineer working as the WORKER in a
Planner -> Worker -> Reviewer pipeline. A senior architect wrote the instructions.
Your output is reviewed by another engineer before it touches the codebase.

ABSOLUTE RULES
1. Do EXACTLY what the instructions say. Do not add features, refactors, comments,
   renames or "improvements" that were not requested. Out-of-scope work is a failure.
2. Never invent facts, APIs, file paths or content that are not in the instructions
   or in the provided files.
3. If the instructions are ambiguous or an anchor you need does not exist in the files,
   DO NOT GUESS. Emit an operation-free response and explain in "blockers".
4. Preserve the existing code style, indentation and conventions of each file.

OUTPUT FORMAT — return ONE JSON object and nothing else. No prose, no markdown fences.

{
  "summary": "one paragraph: what you changed and why",
  "assumptions": ["assumptions you had to make (empty list if none)"],
  "risks": ["things the reviewer must check carefully (empty list if none)"],
  "blockers": ["reasons you could NOT complete the task (empty list if none)"],
  "operations": [
    {
      "op": "replace",
      "path": "relative/path/from/project/root.css",
      "find": "EXACT text currently in the file, copied verbatim, long enough to be UNIQUE",
      "replace": "the new text",
      "expect_count": 1,
      "reason": "why this edit"
    },
    {
      "op": "write_file",
      "path": "relative/path/new_or_rewritten.py",
      "content": "the COMPLETE file content",
      "reason": "why this file"
    }
  ]
}

RULES FOR "replace"
- "find" MUST be copied character-for-character from the provided file content,
  including indentation and newlines. If it does not match exactly, the patch is rejected.
- "find" MUST appear exactly "expect_count" times in the file. Include enough
  surrounding context to make it unique. Never use a short ambiguous snippet.
- Do not use regex. It is literal text matching.

Use "write_file" only for new files or genuine full rewrites. Prefer "replace" for edits.
"""

# --------------------------------------------------------------------------- #
# Helpers
# --------------------------------------------------------------------------- #


def fail(msg: str, code: int = 1) -> None:
    print(f"✗ {msg}", file=sys.stderr)
    sys.exit(code)


def safe_path(rel: str) -> Path:
    """Risolve un path dentro il progetto. Rifiuta escape (.. / assoluti)."""
    p = (PROJECT_ROOT / rel).resolve()
    if not str(p).startswith(str(PROJECT_ROOT) + os.sep) and p != PROJECT_ROOT:
        raise ValueError(f"path fuori dal progetto: {rel}")
    return p


def read_project_file(rel: str) -> str:
    """Legge un file DI PROGETTO (vincolato alla root)."""
    try:
        p = safe_path(rel)
    except ValueError as e:
        fail(str(e))
    if not p.is_file():
        fail(f"file non trovato: {rel}")
    return p.read_text(encoding="utf-8")


def read_any_file(path: str) -> str:
    """Legge un file di sole ISTRUZIONI: può stare ovunque (input, mai scritto)."""
    p = Path(path).expanduser()
    if not p.is_file():
        fail(f"file istruzioni non trovato: {path}")
    return p.read_text(encoding="utf-8")


def extract_json(raw: str) -> dict:
    """GLM può incorniciare il JSON in ```json ... ``` o aggiungere prosa: recuperiamo."""
    raw = raw.strip()
    fence = re.search(r"```(?:json)?\s*(.*?)```", raw, re.S)
    if fence:
        raw = fence.group(1).strip()
    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        start, end = raw.find("{"), raw.rfind("}")
        if start == -1 or end <= start:
            fail("la risposta di GLM non contiene JSON valido.\n--- risposta ---\n" + raw[:2000])
        try:
            return json.loads(raw[start : end + 1])
        except json.JSONDecodeError as e:
            fail(f"JSON non parsabile: {e}\n--- risposta ---\n{raw[:2000]}")


def validate_patch(patch: dict) -> list[dict]:
    """Valida la forma dell'envelope. Ritorna le operazioni."""
    if not isinstance(patch, dict):
        fail("il patch non è un oggetto JSON")
    ops = patch.get("operations")
    if ops is None or not isinstance(ops, list):
        fail("campo 'operations' mancante o non è una lista")
    for i, op in enumerate(ops):
        kind = op.get("op")
        if kind not in ("replace", "write_file"):
            fail(f"operations[{i}]: op sconosciuta {kind!r} (ammesse: replace, write_file)")
        if not op.get("path"):
            fail(f"operations[{i}]: 'path' mancante")
        if kind == "replace":
            for k in ("find", "replace"):
                if k not in op:
                    fail(f"operations[{i}]: campo '{k}' mancante per op=replace")
            if not str(op["find"]).strip():
                fail(f"operations[{i}]: 'find' vuoto")
        else:
            if "content" not in op:
                fail(f"operations[{i}]: 'content' mancante per op=write_file")
    return ops


# --------------------------------------------------------------------------- #
# generate
# --------------------------------------------------------------------------- #


def cmd_generate(args: argparse.Namespace) -> None:
    task_text = sys.stdin.read() if args.task == "-" else read_any_file(args.task)

    blocks = []
    for rel in args.file:
        content = read_project_file(rel)
        blocks.append(f"----- FILE: {rel} -----\n{content}\n----- END FILE: {rel} -----")
    files_blob = "\n\n".join(blocks) if blocks else "(nessun file fornito)"

    user_prompt = (
        "## INSTRUCTIONS FROM THE ARCHITECT\n"
        f"{task_text}\n\n"
        "## CURRENT FILES (authoritative — copy 'find' anchors verbatim from here)\n"
        f"{files_blob}\n\n"
        "Return ONLY the JSON object described in the system prompt."
    )

    if args.dry_run:
        print("=== SYSTEM ===\n" + SYSTEM_PROMPT)
        print("\n=== USER ===\n" + user_prompt)
        approx = (len(SYSTEM_PROMPT) + len(user_prompt)) // 4
        print(f"\n(dry-run: nessuna chiamata API · ~{approx:,} token stimati in input)")
        return

    api_key = os.environ.get("GLM_API_KEY")
    if not api_key:
        fail("GLM_API_KEY non impostata.  export GLM_API_KEY='...'")

    try:
        from openai import OpenAI
    except ImportError:
        fail("libreria 'openai' mancante:  python3 -m pip install openai")

    client = OpenAI(api_key=api_key, base_url=args.base_url, timeout=args.timeout)

    print(f"→ modello: {args.model}  ·  endpoint: {args.base_url}")
    print(f"→ file in contesto: {len(args.file)}  ·  attendo GLM…")

    kwargs = dict(
        model=args.model,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_prompt},
        ],
        temperature=args.temperature,
    )
    if args.max_tokens:
        kwargs["max_tokens"] = args.max_tokens

    # Non tutti gli endpoint OpenAI-compatible supportano response_format: si riprova
    # SOLO se l'errore riguarda quel parametro. Un errore di auth/rete deve emergere subito,
    # senza una seconda chiamata inutile che maschererebbe la causa reale.
    try:
        resp = client.chat.completions.create(response_format={"type": "json_object"}, **kwargs)
    except Exception as e:
        msg = str(e).lower()
        unsupported = "response_format" in msg or "json_object" in msg or "unsupported" in msg
        if not unsupported:
            fail(f"chiamata API fallita: {e}")
        print("→ response_format non supportato dall'endpoint: riprovo senza (il JSON è comunque imposto dal system prompt)")
        try:
            resp = client.chat.completions.create(**kwargs)
        except Exception as e2:
            fail(f"chiamata API fallita: {e2}")

    raw = resp.choices[0].message.content or ""
    patch = extract_json(raw)
    validate_patch(patch)

    STAGING_DIR.mkdir(exist_ok=True)
    out = Path(args.out) if args.out else STAGING_DIR / "patch.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(patch, indent=2, ensure_ascii=False), encoding="utf-8")

    raw_path = out.with_suffix(".raw.txt")
    raw_path.write_text(raw, encoding="utf-8")

    usage = getattr(resp, "usage", None)
    if usage:
        print(
            f"→ token: in={getattr(usage,'prompt_tokens','?')} "
            f"out={getattr(usage,'completion_tokens','?')} "
            f"tot={getattr(usage,'total_tokens','?')}"
        )

    print(f"\n✓ patch salvato: {out}")
    print(f"  (risposta grezza: {raw_path})")
    print(f"\n— summary —\n{patch.get('summary','(nessuno)')}")
    for key, label in (("blockers", "⛔ BLOCKERS"), ("assumptions", "• assunzioni"), ("risks", "⚠ rischi")):
        items = patch.get(key) or []
        if items:
            print(f"\n{label}:")
            for it in items:
                print(f"  - {it}")
    print(f"\n{len(patch['operations'])} operazione/i proposte. Prossimo passo: review, poi")
    print(f"  python3 glm_worker.py apply --patch {out}")


# --------------------------------------------------------------------------- #
# apply
# --------------------------------------------------------------------------- #


def cmd_apply(args: argparse.Namespace) -> None:
    patch = json.loads(Path(args.patch).read_text(encoding="utf-8"))
    ops = validate_patch(patch)

    if patch.get("blockers"):
        fail("il patch dichiara dei blockers: risolvili prima di applicare.")

    # ---- FASE 1: validazione a secco su TUTTE le operazioni (nessuna scrittura) ----
    planned: list[tuple[dict, Path, str | None]] = []
    for i, op in enumerate(ops):
        try:
            path = safe_path(op["path"])
        except ValueError as e:
            fail(f"operations[{i}]: {e}")

        if op["op"] == "write_file":
            planned.append((op, path, None))
            continue

        if not path.is_file():
            fail(f"operations[{i}]: file inesistente {op['path']}")
        original = path.read_text(encoding="utf-8")
        found = original.count(op["find"])
        expected = int(op.get("expect_count", 1))
        if found == 0:
            fail(
                f"operations[{i}] ({op['path']}): ancora 'find' NON trovata.\n"
                "  → GLM non ha copiato il testo esatto. Patch rifiutato."
            )
        if found != expected:
            fail(
                f"operations[{i}] ({op['path']}): ancora trovata {found}× ma expect_count={expected}.\n"
                "  → ambigua. Patch rifiutato per evitare modifiche errate."
            )
        planned.append((op, path, original))

    # ---- piano ----
    print(f"Piano ({len(planned)} operazioni):")
    for op, path, _ in planned:
        rel = path.relative_to(PROJECT_ROOT)
        if op["op"] == "write_file":
            exists = "sovrascrive" if path.exists() else "crea"
            print(f"  • write_file  {rel}  ({exists}, {len(op['content']):,} char)")
        else:
            print(f"  • replace     {rel}  ({len(op['find'])} → {len(op['replace'])} char)")
        if op.get("reason"):
            print(f"      ↳ {op['reason']}")

    if not args.yes:
        print("\n(dry-run: validazione superata, nessun file modificato)")
        print("Per applicare davvero:  --yes")
        return

    # ---- FASE 2: scrittura + backup ----
    stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    backup_dir = STAGING_DIR / "backup" / stamp
    written = []
    for op, path, original in planned:
        if path.exists():
            dest = backup_dir / path.relative_to(PROJECT_ROOT)
            dest.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(path, dest)
        if op["op"] == "write_file":
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(op["content"], encoding="utf-8")
        else:
            path.write_text(original.replace(op["find"], op["replace"]), encoding="utf-8")
        written.append(path.relative_to(PROJECT_ROOT))

    print(f"\n✓ applicate {len(written)} operazioni")
    if backup_dir.exists():
        print(f"  backup: {backup_dir.relative_to(PROJECT_ROOT)}")
    print("  verifica con:  git diff")


# --------------------------------------------------------------------------- #
# CLI
# --------------------------------------------------------------------------- #


def main() -> None:
    parser = argparse.ArgumentParser(description="Worker GLM per pipeline Planner→Worker→Reviewer")
    sub = parser.add_subparsers(dest="cmd", required=True)

    g = sub.add_parser("generate", help="chiama GLM e salva un patch JSON in staging")
    g.add_argument("--task", required=True, help="file con le istruzioni ('-' per stdin)")
    g.add_argument("--file", action="append", default=[], help="file di contesto (ripetibile)")
    g.add_argument("--out", help="path del patch (default: .glm/patch.json)")
    g.add_argument("--model", default=DEFAULT_MODEL)
    g.add_argument("--base-url", default=DEFAULT_BASE_URL)
    g.add_argument("--temperature", type=float, default=0.1)
    g.add_argument("--max-tokens", type=int, default=None)
    g.add_argument("--timeout", type=float, default=600.0)
    g.add_argument("--dry-run", action="store_true", help="stampa il prompt senza chiamare l'API")
    g.set_defaults(func=cmd_generate)

    a = sub.add_parser("apply", help="valida e (con --yes) applica un patch revisionato")
    a.add_argument("--patch", required=True)
    a.add_argument("--yes", action="store_true", help="scrive davvero i file")
    a.set_defaults(func=cmd_apply)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
