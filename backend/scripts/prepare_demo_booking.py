#!/usr/bin/env python3
"""
SmartServe CLI - Prepare Repeatable Demo Booking for COD & OTP Workflow

Usage:
    python scripts/prepare_demo_booking.py [--status Requested|Arrived|Started] [--amount 850.0]

Purpose:
Prepares a clean, realistic booking between demo.customer and demo.provider
with authentic Start OTP and Completion OTP generation and COD payment record.

Allows repeating the COD / Two-Stage OTP verification without registering new accounts!
"""

import os
import sys
import argparse

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from dotenv import load_dotenv
load_dotenv(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".env")))

from app.repositories.db import get_db
from app.services.demo_service import prepare_demo_booking


def main():
    parser = argparse.ArgumentParser(description="Create a fresh demo booking for testing COD & OTP.")
    parser.add_argument(
        "--status",
        choices=["Requested", "Accepted", "Arrived", "Started"],
        default="Arrived",
        help="Initial booking status (default: 'Arrived' - ready for Start OTP verification)",
    )
    parser.add_argument(
        "--amount",
        type=float,
        default=None,
        help="Agreed service amount in INR (default: service base price)",
    )
    args = parser.parse_args()

    print("=" * 72)
    print(" SmartServe - Repeatable Demo Booking Generator")
    print("=" * 72)

    db = next(get_db())
    try:
        booking = prepare_demo_booking(
            db,
            status=args.status,
            agreed_amount=args.amount,
        )

        print("\n[OK] Fresh Demo Booking Created Successfully:\n")
        print(f"  Booking ID:        {booking['booking_id']}")
        print(f"  Booking Reference: {booking['booking_reference']}")
        print(f"  Service:           {booking['service_name']}")
        print(f"  Agreed Amount:     Rs. {booking['agreed_amount']:.2f}")
        print(f"  Payment Method:    {booking['payment_method']}")
        print(f"  Payment Status:    {booking['payment_status']}")
        print(f"  Booking Status:    {booking['status']}")
        print(f"  Customer:          {booking['customer_email']}")
        print(f"  Provider:          {booking['provider_email']}")
        print(f"  Scheduled Time:    {booking['scheduled_time']}")
        print(f"  Address:           {booking['address']}\n")

        print("------------------------------------------------------------------------")
        print(" DEMO INSTRUCTIONS & OTP CODES:")
        print("------------------------------------------------------------------------")
        print(f"  >> Start Service OTP:      {booking['start_otp']}")
        if booking.get("completion_otp"):
            print(f"  >> Complete Service OTP:   {booking['completion_otp']}")
        else:
            print("  >> Complete Service OTP:   (Will be generated once service is started)")
        print("\n  Steps to demonstrate:")
        print("  1. Customer Portal (http://localhost:5174/bookings):")
        print("     - Log in as demo.customer@smartserve.com")
        print(f"     - Open booking {booking['booking_reference']}")
        print(f"     - Notice the Start OTP code ({booking['start_otp']}) and COD payment badge.")
        print("  2. Provider Portal (http://localhost:5175/):")
        print("     - Log in as demo.provider@smartserve.com")
        print("     - Open the assigned booking.")
        print(f"     - Click 'Start Service' and enter OTP: {booking['start_otp']}")
        print("     - Service transitions to 'Started'. Customer now sees Completion OTP.")
        print("     - Click 'Complete Service' and enter customer's Completion OTP.")
        print(f"     - Click 'Mark Cash Collected' and report Rs. {booking['agreed_amount']:.2f}.")
        print("  3. Admin Portal (http://localhost:5173/admin/bookings):")
        print("     - Log in as demo.admin@smartserve.com")
        print("     - View COD Payment Review queue and click 'Verify' to mark as Paid.\n")
        print("=" * 72)
    except PermissionError as pe:
        print(f"\n[SECURITY ERROR] {pe}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"\n[ERROR] Failed to prepare demo booking: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        sys.exit(1)
    finally:
        db.close()


if __name__ == "__main__":
    main()
