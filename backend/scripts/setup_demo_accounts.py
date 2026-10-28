#!/usr/bin/env python3
"""
SmartServe CLI - Setup Reusable Local Demo Accounts

Usage:
    python scripts/setup_demo_accounts.py [--no-password-reset]

Guarantees:
- Idempotently creates or reuses:
    * Demo Customer:      demo.customer@smartserve.com / DemoCustomer123!
    * Demo Provider:      demo.provider@smartserve.com / DemoProvider123!
    * Demo Administrator: demo.admin@smartserve.com    / DemoAdmin123!
- Preserves existing accounts and user IDs on repeated runs.
- Sets up verified provider KYC documents, catalog associations, and free calendar slots.
- Never destroys or modifies real accounts or existing bookings.
"""

import os
import sys
import argparse

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from dotenv import load_dotenv
load_dotenv(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".env")))

from app.repositories.db import get_db
from app.services.demo_service import setup_demo_accounts


def main():
    parser = argparse.ArgumentParser(description="Initialize or refresh SmartServe local demo accounts.")
    parser.add_argument(
        "--no-password-reset",
        action="store_true",
        help="Do not reset passwords if demo accounts already exist.",
    )
    args = parser.parse_args()

    print("=" * 72)
    print(" SmartServe - Reusable Demo Accounts Setup & Verification")
    print("=" * 72)

    db = next(get_db())
    try:
        results = setup_demo_accounts(db, update_passwords=not args.no_password_reset)

        print("\n[OK] Demo Accounts Ready for Local Development & Testing:\n")
        print(f"  1. CUSTOMER PORTAL (http://localhost:5174/login)")
        print(f"     Email:     {results['customer']['email']}")
        print(f"     Password:  {results['customer']['password']}")
        print(f"     Role:      {results['customer']['role']}")
        print(f"     Name:      {results['customer']['full_name']}")
        print(f"     User ID:   {results['customer']['user_id']}\n")

        print(f"  2. PROVIDER PORTAL (http://localhost:5175/login)")
        print(f"     Email:     {results['provider']['email']}")
        print(f"     Password:  {results['provider']['password']}")
        print(f"     Role:      {results['provider']['role']}")
        print(f"     Name:      {results['provider']['full_name']}")
        print(f"     Category:  {results['provider']['category']}")
        print(f"     Services:  {results['provider']['services_count']} catalog services linked")
        print(f"     User ID:   {results['provider']['user_id']}\n")

        print(f"  3. ADMIN OPERATIONS DASHBOARD (http://localhost:5173/admin/login)")
        print(f"     Email:     {results['admin']['email']}")
        print(f"     Password:  {results['admin']['password']}")
        print(f"     Role:      {results['admin']['role']}")
        print(f"     User ID:   {results['admin']['user_id']}\n")

        if results["created_records"]:
            print(f"--> Newly Created Records ({len(results['created_records'])}):")
            for r in results["created_records"]:
                print(f"    + {r}")
        if results["reused_records"]:
            print(f"--> Reused Existing Records ({len(results['reused_records'])}):")
            for r in results["reused_records"]:
                print(f"    * {r}")

        print("\n" + "=" * 72)
        print(" [SUCCESS] Demo environment is configured. Ready to demonstrate.")
        print("=" * 72)
    except PermissionError as pe:
        print(f"\n[SECURITY ERROR] {pe}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"\n[SETUP ERROR] Failed to setup demo accounts: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        sys.exit(1)
    finally:
        db.close()


if __name__ == "__main__":
    main()
