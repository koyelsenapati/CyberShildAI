#!/usr/bin/env python3
from __future__ import annotations

import argparse
import os
import re
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
AUDIT_DIR = ROOT / "audit"
OUT = AUDIT_DIR / "audit-results"
REPORT = OUT / "audit-report.md"

OUT.mkdir(parents=True, exist_ok=True)

PHASES = {
    1: ("Authentication & Core Security", [
        "backend/app/api",
        "backend/app/core",
        "backend/app/models",
        "backend/app/schemas",
        "backend/app/services",
        "frontend/src/pages/Login.tsx",
        "frontend/src/services",
    ], ["auth", "login", "register", "jwt", "security"]),

    2: ("Core Security Scanners", [
        "backend/app/api",
        "backend/app/services",
        "backend/app/engines",
        "frontend/src/pages",
        "frontend/src/services",
    ], ["phishing", "password", "header", "whois", "dns", "ssl"]),

    3: ("Network Security", [
        "backend/app/api",
        "backend/app/services",
        "backend/app/engines",
        "frontend/src/pages",
        "frontend/src/services",
    ], ["network", "port", "scanner", "socket", "nmap"]),

    4: ("Vulnerability Detection", [
        "backend/app/api",
        "backend/app/services",
        "backend/app/engines",
        "frontend/src/pages",
        "frontend/src/services",
    ], ["vulnerability", "cve", "cvss", "finding"]),

    5: ("File Integrity & Monitoring", [
        "backend/app/api",
        "backend/app/services",
        "backend/app/engines",
        "frontend/src/pages",
        "frontend/src/services",
    ], ["integrity", "hash", "monitor", "file"]),

    6: ("Security Dashboard & Integration", [
        "backend/app/api",
        "backend/app/services",
        "backend/app/crud",
        "backend/app/models",
        "backend/app/schemas",
        "frontend/src/pages",
        "frontend/src/hooks",
        "frontend/src/services",
        "frontend/src/types",
    ], ["dashboard", "statistics", "scan", "security_score"]),

    7: ("Scan History / Master Scan", [
        "backend/app/api/master_scan.py",
        "backend/app/services/master_scan_service.py",
        "backend/app/crud/master_scan.py",
        "backend/app/models/master_scan.py",
        "backend/app/models/scan.py",
        "backend/app/schemas/master_scan.py",
        "frontend/src/pages/Dashboard.tsx",
    ], ["master_scan", "scan_history", "scan history"]),

    8: ("Security Reports", [
        "backend/app/api/reports.py",
        "backend/app/services/report_service.py",
        "backend/app/reports",
        "frontend/src/pages/Reports.tsx",
    ], ["report", "pdf", "json", "cvss", "owasp", "remediation"]),

    9: ("AI Security Assistant", [
        "backend/app",
        "frontend/src/pages/AIChat.tsx",
        "frontend/src/services",
        "frontend/src/types",
    ], ["ai", "assistant", "chat", "llm", "prompt", "remediation"]),

    10: ("Alerts / Threat Intelligence", [
        "backend/app",
        "frontend/src/pages/ThreatIntel.tsx",
        "frontend/src/services",
        "frontend/src/types",
    ], ["alert", "threat", "notification", "intel"]),

    11: ("Dashboard", [
        "backend/app",
        "frontend/src/pages/Dashboard.tsx",
        "frontend/src/hooks",
        "frontend/src/services",
        "frontend/src/types",
    ], ["dashboard", "security_score", "total_scans", "threat_summary"]),

    12: ("Database / Migrations", [
        "backend/app/database",
        "backend/app/models",
        "backend/app/schemas",
        "backend/app/crud",
        "backend/alembic",
    ], ["created_at", "updated_at", "ForeignKey", "relationship", "DATABASE_URL"]),

    13: ("Zero Trust / Passwordless", [
        "backend/app",
        "frontend/src",
    ], ["passwordless", "webauthn", "passkey", "zero_trust", "session"]),

    14: ("Testing", [
        "backend/tests",
        "autotest",
        "frontend/tests",
        "frontend",
    ], ["pytest", "playwright", "websocket", "authorization", "authentication"]),

    15: ("Final SOC UI/UX", [
        "frontend/src/layouts",
        "frontend/src/pages",
        "frontend/src/components",
        "frontend/src/assets",
    ], ["Dashboard", "NetworkAnalyzer", "VulnerabilityScanner",
        "WebSecurity", "ThreatIntel", "AIChat", "Reports", "Settings"]),
}

BAD_WORDS = [
    "mock",
    "demo",
    "dummy",
    "fake",
    "simulated",
    "sampleDashboard",
    "demoDashboardStatistics",
]

SKIP = {
    ".git",
    ".venv",
    ".venv-linux",
    "venv",
    "node_modules",
    "dist",
    "build",
    "__pycache__",
    ".pytest_cache",
    ".mypy_cache",
    ".ruff_cache",
    "audit",
}

EXTENSIONS = {
    ".py",
    ".ts",
    ".tsx",
    ".js",
    ".jsx",
    ".json",
    ".yaml",
    ".yml",
    ".toml",
}

def timestamp():
    return datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")

def rel(path):
    return str(path.relative_to(ROOT)).replace("\\", "/")

def source_files():
    for p in ROOT.rglob("*"):
        if not p.is_file():
            continue
        if any(part in SKIP for part in p.parts):
            continue
        if p.suffix.lower() not in EXTENSIONS:
            continue
        yield p

def run(cmd, cwd, timeout, env=None):
    try:
        p = subprocess.run(
            cmd,
            cwd=cwd,
            text=True,
            capture_output=True,
            timeout=timeout,
            env=env,
        )
        output = ((p.stdout or "") + "\n" + (p.stderr or "")).strip()
        return {
            "status": "PASS" if p.returncode == 0 else "FAIL",
            "code": p.returncode,
            "command": " ".join(map(str, cmd)),
            "output": output[-6000:],
        }
    except subprocess.TimeoutExpired:
        return {
            "status": "TIMEOUT",
            "code": None,
            "command": " ".join(map(str, cmd)),
            "output": "Command timed out.",
        }
    except Exception as e:
        return {
            "status": "BLOCKED",
            "code": None,
            "command": " ".join(map(str, cmd)),
            "output": repr(e),
        }

def find_equivalents(target):
    name = Path(target).name.lower()
    stem = Path(target).stem.lower()
    matches = []

    for p in ROOT.rglob("*"):
        if not p.is_file():
            continue
        if any(part in SKIP for part in p.parts):
            continue

        n = p.name.lower()
        s = p.stem.lower()

        if n == name or s == stem or stem in s:
            matches.append(rel(p))

    return sorted(set(matches))[:15]

def inspect_phase(phase):
    name, paths, terms = PHASES[phase]
    rows = []

    for target in paths:
        p = ROOT / target

        if p.exists():
            rows.append({
                "path": target,
                "status": "EXISTS",
                "equivalent": [],
            })
        else:
            rows.append({
                "path": target,
                "status": "MISSING",
                "equivalent": find_equivalents(target),
            })

    return name, terms, rows

def search_terms(terms):
    hits = []

    patterns = [
        re.compile(re.escape(term), re.I)
        for term in terms
    ]

    for p in source_files():
        try:
            text = p.read_text(
                encoding="utf-8",
                errors="ignore",
            )
        except Exception:
            continue

        for number, line in enumerate(text.splitlines(), 1):
            for pattern in patterns:
                if pattern.search(line):
                    hits.append(
                        f"{rel(p)}:{number} -> {pattern.pattern}"
                    )
                    break

    return hits

def production_audit():
    hits = []

    patterns = [
        re.compile(rf"\b{re.escape(x)}\b", re.I)
        for x in BAD_WORDS
    ]

    for p in source_files():
        path = rel(p)

        if (
            "/tests/" in path
            or path.startswith("tests/")
            or path.startswith("autotest/")
        ):
            continue

        try:
            text = p.read_text(
                encoding="utf-8",
                errors="ignore",
            )
        except Exception:
            continue

        for number, line in enumerate(text.splitlines(), 1):
            for pattern in patterns:
                if pattern.search(line):
                    hits.append(
                        f"{path}:{number} -> {pattern.pattern}"
                    )
                    break

    return hits

def objective_tests():
    results = []

    backend = ROOT / "backend"
    frontend = ROOT / "frontend"

    if backend.exists():
        test_env = os.environ.copy()
        test_db = backend / "tests" / ".cybershield_audit.db"
        test_env.update({
            "DATABASE_URL": f"sqlite:///{test_db.as_posix()}",
            "SECRET_KEY": "audit-test-secret-not-for-production",
            "ALGORITHM": "HS256",
            "ACCESS_TOKEN_EXPIRE_MINUTES": "30",
        })
        results.append(
            run(
                [sys.executable, "-m", "compileall", "-q", "app"],
                backend,
                600,
            )
        )

        if (backend / "tests").exists():
            results.append(
                run(
                    [sys.executable, "-m", "pytest", "-q"],
                    backend,
                    1800,
                    env=test_env,
                )
            )

        if (backend / "alembic.ini").exists():
            results.append(
                run(
                    [sys.executable, "-m", "alembic", "heads"],
                    backend,
                    900,
                    env=test_env,
                )
            )

    if frontend.exists() and (frontend / "package.json").exists():
        results.append(
            run(
                ["npm", "run", "build"],
                frontend,
                1800,
            )
        )

        if (frontend / "tsconfig.json").exists():
            results.append(
                run(
                    ["npx", "tsc", "--noEmit"],
                    frontend,
                    900,
                )
            )

        if (
            (frontend / "playwright.config.ts").exists()
            or
            (frontend / "playwright.config.js").exists()
        ):
            results.append(
                run(
                    ["npx", "playwright", "test"],
                    frontend,
                    2400,
                )
            )

    return results

def write_report(
    round_no,
    start_phase,
    phase_data,
    tests,
    production_hits,
    repair_result=None,
):
    lines = []

    lines.append("# CYBERSHIELD AI â€” CONTINUOUS AUDIT REPORT")
    lines.append("")
    lines.append(f"Generated: {timestamp()}")
    lines.append(f"Round: {round_no}")
    lines.append(f"Scope: Phase {start_phase} -> Phase 15")
    lines.append("")

    failed_tests = [
        x for x in tests
        if x["status"] != "PASS"
    ]

    missing = []

    for phase in phase_data:
        for item in phase["files"]:
            if item["status"] == "MISSING":
                missing.append(item)

    if not failed_tests and not missing and not production_hits:
        verdict = "OBJECTIVE GATES PASSED"
    else:
        verdict = "NOT PROVEN"

    lines.append(f"## VERDICT: {verdict}")
    lines.append("")

    for phase in phase_data:
        lines.append(
            f"## PHASE {phase['number']} â€” {phase['name']}"
        )
        lines.append("")

        for item in phase["files"]:
            if item["status"] == "EXISTS":
                lines.append(
                    f"- [PASS] `{item['path']}`"
                )
            else:
                lines.append(
                    f"- [MISSING] `{item['path']}`"
                )

                for eq in item["equivalent"]:
                    lines.append(
                        f"  - Possible equivalent: `{eq}`"
                    )

        if phase["hits"]:
            lines.append("")
            lines.append("Relevant implementation references:")
            for hit in phase["hits"][:30]:
                lines.append(f"- `{hit}`")

        lines.append("")

    lines.append("## OBJECTIVE TESTS")
    lines.append("")

    for test in tests:
        lines.append(
            f"- [{test['status']}] `{test['command']}`"
        )

        if test["status"] != "PASS":
            lines.append("```text")
            lines.append(test["output"])
            lines.append("```")

    lines.append("")

    lines.append("## PRODUCTION DATA AUDIT")
    lines.append("")

    if production_hits:
        for hit in production_hits[:200]:
            lines.append(f"- `{hit}`")
    else:
        lines.append("- No configured production-data keyword findings.")

    lines.append("")

    if repair_result:
        lines.append("## REPAIR AGENT")
        lines.append("")
        lines.append(
            f"Status: **{repair_result['status']}**"
        )
        lines.append("")

    lines.append("## RELEASE NOTE")
    lines.append("")
    lines.append(
        "PASS means only that the configured objective gates "
        "passed. It is not a substitute for external penetration "
        "testing, dependency review, infrastructure review, or "
        "manual security assessment."
    )

    REPORT.write_text(
        "\n".join(lines),
        encoding="utf-8",
    )

def main():
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--start-phase",
        type=int,
        default=1,
        choices=range(1, 16),
    )

    parser.add_argument(
        "--max-rounds",
        type=int,
        default=20,
    )

    parser.add_argument(
        "--once",
        action="store_true",
    )

    parser.add_argument(
        "--sleep",
        type=int,
        default=5,
    )

    parser.add_argument(
        "--repair-command",
        default=os.getenv(
            "CYBERSHIELD_REPAIR_COMMAND",
            "",
        ),
    )

    args = parser.parse_args()

    print("=" * 50)
    print("CYBERSHIELD AI CONTINUOUS AUTOPILOT")
    print("=" * 50)
    print(f"Repository : {ROOT}")
    print(f"Scope      : Phase {args.start_phase} -> Phase 15")
    print(f"Max Rounds : {args.max_rounds}")
    print(f"Report     : {REPORT}")
    print()

    for round_no in range(1, args.max_rounds + 1):
        print(f"========== AUDIT ROUND {round_no} ==========")

        phase_data = []

        for phase in range(args.start_phase, 16):
            name, terms, files = inspect_phase(phase)
            hits = search_terms(terms)

            phase_data.append({
                "number": phase,
                "name": name,
                "files": files,
                "hits": hits,
            })

            missing = [
                x for x in files
                if x["status"] == "MISSING"
            ]

            print(
                f"Phase {phase}: "
                f"{'PASS' if not missing else 'PARTIAL'}"
            )

            for item in missing:
                print(f"  MISSING: {item['path']}")

        print()
        print("========== OBJECTIVE TESTS ==========")

        tests = objective_tests()

        for test in tests:
            print(
                f"[{test['status']}] "
                f"{test['command']}"
            )

        production_hits = production_audit()

        repair_result = None

        write_report(
            round_no,
            args.start_phase,
            phase_data,
            tests,
            production_hits,
        )

        failed = [
            x for x in tests
            if x["status"] != "PASS"
        ]

        missing = [
            item
            for phase in phase_data
            for item in phase["files"]
            if item["status"] == "MISSING"
            and not item["equivalent"]
        ]

        print()
        print(f"Report saved: {REPORT}")

        if not failed and not missing and not production_hits:
            print()
            print("OBJECTIVE GATES PASSED.")
            return 0

        if args.once:
            print("One-shot mode enabled. Stopping.")
            return 2

        if not args.repair_command:
            print()
            print("No repair command configured.")
            print("Audit stopped without fabricating completion.")
            return 3

        print()
        print("Running repair agent...")

        repair_result = run(
            args.repair_command,
            ROOT,
            3600,
        )

        write_report(
            round_no,
            args.start_phase,
            phase_data,
            tests,
            production_hits,
            repair_result,
        )

        if repair_result["status"] != "PASS":
            print("Repair agent failed or was blocked.")
            return 4

        time.sleep(max(0, args.sleep))

    print()
    print("Maximum audit rounds reached.")
    return 5

if __name__ == "__main__":
    raise SystemExit(main())
