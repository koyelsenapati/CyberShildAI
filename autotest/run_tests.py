import sys
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BACKEND = ROOT / "backend"
FRONTEND = ROOT / "frontend"

def run_command(name, command, cwd):
    print("\n" + "=" * 65)
    print(f" TEST: {name}")
    print("=" * 65)

    try:
        result = subprocess.run(
            command,
            cwd=str(cwd),
            shell=True,
            text=True,
            capture_output=True,
        )

        if result.stdout:
            print(result.stdout)

        if result.stderr:
            print(result.stderr)

        if result.returncode == 0:
            print(f"[PASS] {name}")
            return True

        print(f"[FAIL] {name}")
        return False

    except Exception as e:
        print(f"[ERROR] {name}: {e}")
        return False

def main():
    results = []

    print("\n" + "#" * 65)
    print("#          CYBERSHIELD AI AUTOMATED TEST SUITE")
    print("#" * 65)

    # =================================================
    # BACKEND TESTS
    # =================================================

    print("\n" + "-" * 65)
    print(" BACKEND TESTS")
    print("-" * 65)

    backend_python = BACKEND / ".venv" / "Scripts" / "python.exe"

    if not backend_python.exists():
        print("\n[FAIL] Backend virtual environment not found.")
        print(f"Expected: {backend_python}")
        sys.exit(1)

    # 1. Python Compile Test
    results.append(
        run_command(
            "Backend Python Compile",
            f'"{backend_python}" -m compileall app',
            BACKEND,
        )
    )

    # 2. Main Application Import
    results.append(
        run_command(
            "Backend Main Import",
            f'"{backend_python}" -c "from app.main import app; print(\'BACKEND IMPORT: OK\')"',
            BACKEND,
        )
    )

    # 3. Risk Orchestrator
    results.append(
        run_command(
            "Risk Orchestrator",
            f'"{backend_python}" -c "from app.engines.ai_engine.risk_orchestrator import orchestrate_risk; print(orchestrate_risk({{}}))"',
            BACKEND,
        )
    )

    # 4. Master Scan
    results.append(
        run_command(
            "Master Scan Import",
            f'"{backend_python}" -c "from app.services.master_scan_service import start_master_scan; from app.api.master_scan import router; print(\'MASTER SCAN: OK\')"',
            BACKEND,
        )
    )

    # 5. Alembic
    results.append(
        run_command(
            "Alembic Current Revision",
            f'"{backend_python}" -m alembic current',
            BACKEND,
        )
    )

    # =================================================
    # FRONTEND TESTS
    # =================================================

    print("\n" + "-" * 65)
    print(" FRONTEND TESTS")
    print("-" * 65)

    if FRONTEND.exists():

        # 6. NPM Check
        results.append(
            run_command(
                "Frontend NPM Check",
                "npm.cmd --version",
                FRONTEND,
            )
        )

        package_json = FRONTEND / "package.json"

        if package_json.exists():

            # 7. Frontend Build
            results.append(
                run_command(
                    "Frontend Production Build",
                    "npm.cmd run build",
                    FRONTEND,
                )
            )

        else:
            print("\n[SKIP] frontend/package.json not found.")

    else:
        print("\n[SKIP] frontend directory not found.")

    # =================================================
    # FINAL REPORT
    # =================================================

    passed = sum(results)
    total = len(results)
    failed = total - passed

    print("\n")
    print("#" * 65)
    print("#                 FINAL TEST REPORT")
    print("#" * 65)

    print(f"\nTotal Tests : {total}")
    print(f"Passed      : {passed}")
    print(f"Failed      : {failed}")

    print("\n" + "-" * 65)

    if failed == 0:
        print("STATUS : ALL AUTOMATED TESTS PASSED")
        print("RESULT : CYBERSHIELD AI IS READY")
        print("-" * 65)
        sys.exit(0)

    print("STATUS : SOME AUTOMATED TESTS FAILED")
    print("ACTION : FIX FAILED TESTS BEFORE CONTINUING")
    print("-" * 65)

    sys.exit(1)

if __name__ == "__main__":
    main()
