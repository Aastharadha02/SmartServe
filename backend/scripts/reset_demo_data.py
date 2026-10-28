#!/usr/bin/env python3
"""
SmartServe CLI - Safe Local Demo Reset Utility

Usage:
    python scripts/reset_demo_data.py --confirm

Safety Constraints:
1. Strictly blocked if ENVIRONMENT='production' or 'prod'.
2. Blocked if database is external/remote unless explicitly forced.
3. Requires explicit '--confirm' flag to prevent accidental execution.
4. Purges ONLY demo-owned bookings, payments, and OTP records.
5. PRESERVES all user accounts (including demo accounts and credentials).
6. NEVER touches real customer, provider, admin, or unrelated bookings.
"""

import os
import sys
import argparse

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from dotenv import load_dotenv
load_dotenv(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".env")))

from app.core.config import settings
from app.repositories.db import get_db
from app.services.demo_service import reset_demo_data


def main():
    parser = argparse.ArgumentParser(description="Safely reset demo bookings and payment test data.")
    parser.add_argument(
        "--confirm",
        action="store_true",
        help="Explicit confirmation required to execute the demo data reset.",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Override non-local database check (still strictly blocked in production).",
    )
    args = parser.parse_args()

    print("=" * 72)
    print(" SmartServe - Safe Demo Data Reset Utility")
    print("=" * 72)

    env = (settings.ENVIRONMENT or "dev").strip().lower()
    print(f"  Target Environment: {settings.ENVIRONMENT}")
    print(f"  Database Host:      {str(settings.DATABASE_URL).split('@')[-1] if '@' in str(settings.DATABASE_URL) else 'local'}")

    if not args.confirm:
        print("\n[SAFETY NOTICE]")
        print("  This command will purge all demo-owned bookings, test payments, and OTPs")
        print("  associated with 'demo.customer@smartserve.com' and 'demo.provider@smartserve.com'.")
        print("  Demo user accounts and non-demo records will be preserved.")
        print("\n  To execute, you must pass the --confirm flag:")
        print("    python scripts/reset_demo_data.py --confirm\n")
        sys.exit(0)

    db = next(get_db())
    try:
        results = reset_demo_data(db, force=args.force)

        print("\n[OK] Reset Completed Safely:\n")
        print(f"  Status:             {results['message']}")
        print(f"  Deleted Bookings:   {results['deleted_bookings']}")
        print(f"  Deleted Payments:   {results['deleted_payments']}")
        print(f"  Deleted OTPs:       {results['deleted_otps']}")
        print(f"  Preserved Accounts: {', '.join(results.get('preserved_accounts', []))}\n")
        print("=" * 72)
    except PermissionError as pe:
        print(f"\n[SECURITY VIOLATION] {pe}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"\n[ERROR] Demo reset failed: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        sys.exit(1)
    finally:
        db.close()


if __name__ == "__main__":
    main()
