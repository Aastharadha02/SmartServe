import uuid
from datetime import datetime, timezone, timedelta
from app.repositories.db import get_db
from app.models.email import EmailTemplate, EmailLog

def seed_email_templates_and_logs():
    db = next(get_db())

    existing_tmpls = db.query(EmailTemplate).count()
    if existing_tmpls >= 4:
        print(f"Email templates already exist ({existing_tmpls} records). Skipping seed.")
        return

    print("Seeding initial system email templates & dispatch history into PostgreSQL...")

    sample_templates = [
        {
            "template_key": "booking_confirmation",
            "subject": "SmartServe Booking Confirmation — #{{booking_id}}",
            "body_html": """
<div style="font-family: Arial, sans-serif; padding: 20px; color: #1e293b;">
  <h2>Booking Confirmed!</h2>
  <p>Dear <strong>{{customer_name}}</strong>,</p>
  <p>Your booking for <strong>{{service_name}}</strong> has been confirmed.</p>
  <div style="background: #f8fafc; padding: 15px; border-radius: 8px; border: 1px solid #e2e8f0;">
    <p><strong>Booking Reference:</strong> #{{booking_id}}</p>
    <p><strong>Scheduled Time:</strong> {{scheduled_time}}</p>
    <p><strong>Total Price:</strong> ₹{{amount}}</p>
    <p><strong>Start Verification OTP:</strong> <span style="font-size: 18px; font-weight: bold; color: #2563eb;">{{otp_code}}</span></p>
  </div>
  <p style="margin-top: 20px;">Thank you for choosing SmartServe!</p>
</div>
            """.strip()
        },
        {
            "template_key": "provider_assignment",
            "subject": "Provider Assigned for Your Booking #{{booking_id}}",
            "body_html": """
<div style="font-family: Arial, sans-serif; padding: 20px; color: #1e293b;">
  <h2>Provider Assigned</h2>
  <p>Hi <strong>{{customer_name}}</strong>,</p>
  <p>Professional provider <strong>{{provider_name}}</strong> has been assigned to your service request <strong>{{service_name}}</strong>.</p>
  <p>Scheduled arrival time: <strong>{{scheduled_time}}</strong>.</p>
</div>
            """.strip()
        },
        {
            "template_key": "emergency_dispatch_alert",
            "subject": "🚨 URGENT: Emergency Service Dispatch — #{{booking_id}}",
            "body_html": """
<div style="font-family: Arial, sans-serif; padding: 20px; color: #1e293b;">
  <h2 style="color: #dc2626;">Emergency Dispatch Triggered</h2>
  <p>Emergency unit dispatched for <strong>{{customer_name}}</strong>.</p>
  <p>Service: <strong>{{service_name}}</strong></p>
  <p>Address: {{address}}</p>
</div>
            """.strip()
        },
        {
            "template_key": "payment_invoice_receipt",
            "subject": "SmartServe Payment Receipt — ₹{{amount}}",
            "body_html": """
<div style="font-family: Arial, sans-serif; padding: 20px; color: #1e293b;">
  <h2>Payment Invoice Receipt</h2>
  <p>Dear <strong>{{customer_name}}</strong>,</p>
  <p>Payment of <strong>₹{{amount}}</strong> for booking <strong>#{{booking_id}}</strong> ({{service_name}}) has been received successfully.</p>
  <p>Status: <strong style="color: #16a34a;">Paid & Verified</strong></p>
</div>
            """.strip()
        }
    ]

    for tdata in sample_templates:
        existing = db.query(EmailTemplate).filter(EmailTemplate.template_key == tdata["template_key"]).first()
        if not existing:
            tmpl = EmailTemplate(
                id=uuid.uuid4(),
                template_key=tdata["template_key"],
                subject=tdata["subject"],
                body_html=tdata["body_html"],
                updated_at=datetime.now(timezone.utc) - timedelta(days=5)
            )
            db.add(tmpl)

    sample_logs = [
        {
            "recipient_email": "ananya.rao@example.com",
            "subject": "SmartServe Booking Confirmation — #5716e23b",
            "template_key": "booking_confirmation",
            "status": "Sent",
            "sent_at": datetime.now(timezone.utc) - timedelta(hours=8)
        },
        {
            "recipient_email": "priya.sharma@smartserve.com",
            "subject": "Provider Assigned for Your Booking #726cf75f",
            "template_key": "provider_assignment",
            "status": "Sent",
            "sent_at": datetime.now(timezone.utc) - timedelta(hours=6)
        },
        {
            "recipient_email": "rahul.verma@example.com",
            "subject": "🚨 URGENT: Emergency Service Dispatch — #f2cffabd",
            "template_key": "emergency_dispatch_alert",
            "status": "Sent",
            "sent_at": datetime.now(timezone.utc) - timedelta(hours=2)
        },
        {
            "recipient_email": "invalid.customer@domain.test",
            "subject": "SmartServe Payment Receipt — ₹1,499",
            "template_key": "payment_invoice_receipt",
            "status": "Failed",
            "sent_at": datetime.now(timezone.utc) - timedelta(hours=1)
        }
    ]

    for ldata in sample_logs:
        log_e = EmailLog(
            id=uuid.uuid4(),
            recipient_email=ldata["recipient_email"],
            subject=ldata["subject"],
            template_key=ldata["template_key"],
            status=ldata["status"],
            sent_at=ldata["sent_at"]
        )
        db.add(log_e)

    db.commit()
    print("Initial email templates & dispatch history seeded successfully!")

if __name__ == "__main__":
    seed_email_templates_and_logs()
