import uuid
import logging
from typing import Optional, Dict, Any, List, Tuple
from datetime import datetime, timezone
from sqlalchemy.orm import Session

from app.core.config import settings
from app.models.customer import Booking, Customer
from app.models.user import User
from app.models.notification import NotificationLog
from app.services import email_service
from app.services.notification.whatsapp_adapter import (
    get_whatsapp_adapter,
    validate_and_normalize_phone,
    WhatsAppDeliveryResult,
)

logger = logging.getLogger("smartserve.services.notification")

MAX_NOTIFICATION_RETRIES = 3

EVENT_TITLES: Dict[str, str] = {
    "booking.confirmed": "Booking Confirmed",
    "booking.accepted": "Booking Accepted by Provider",
    "booking.rejected": "Booking Update: Reassigned",
    "booking.assigned": "Provider Assigned to Your Booking",
    "booking.rescheduled": "Booking Rescheduled",
    "booking.cancelled": "Booking Cancelled",
    "service.started": "Service Started",
    "service.completed": "Service Completed",
    "payment.collection_reported": "Cash Payment Collection Reported",
    "payment.verified": "Payment Verified & Paid",
    "payment.rejected": "Payment Collection Follow-up Required",
}


def _build_email_content(
    event_type: str,
    customer_name: str,
    booking_ref: str,
    service_name: str,
    scheduled_date: str,
    scheduled_time: str,
    status: str,
    amount: Optional[str] = None,
    payment_status: Optional[str] = None,
    notes: Optional[str] = None,
    booking_id: Optional[str] = None,
) -> Tuple[str, str, str]:
    """
    Generate professional email subject, plain text, and HTML body.
    Never exposes passwords, tokens, or OTP codes.
    """
    title = EVENT_TITLES.get(event_type, "Booking Status Update")
    subject = f"[SmartServe] {title} - {booking_ref}"

    booking_url = f"{settings.FRONTEND_URL}/bookings/{booking_id or booking_ref}"
    price_info = f"₹{amount}" if amount else "N/A"
    pay_status_info = payment_status or "Pending"

    # Plain text body
    text_lines = [
        f"Hello {customer_name},",
        "",
        f"Your SmartServe booking update: {title}",
        "--------------------------------------------------",
        f"Booking Reference: {booking_ref}",
        f"Service:           {service_name}",
        f"Scheduled Date:    {scheduled_date}",
        f"Scheduled Time:    {scheduled_time}",
        f"Booking Status:    {status}",
        f"Agreed Amount:     {price_info}",
        f"Payment Status:    {pay_status_info}",
    ]
    if notes:
        text_lines.append(f"Notes:             {notes}")
    text_lines.extend([
        "--------------------------------------------------",
        f"View your booking details online: {booking_url}",
        "",
        "Thank you for choosing SmartServe!",
        "SmartServe Customer Care Team",
    ])
    body_text = "\n".join(text_lines)

    # HTML body with clean styling
    body_html = f"""<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8">
  <title>{subject}</title>
  <style>
    body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; background-color: #FAF7F0; margin: 0; padding: 24px; color: #1F2A1E; }}
    .container {{ max-width: 600px; margin: 0 auto; background: #ffffff; border: 1px solid #E5DEC9; border-radius: 16px; overflow: hidden; box-shadow: 0 4px 12px rgba(31,42,30,0.04); }}
    .header {{ background: #2F5233; color: #FAF7F0; padding: 24px 32px; text-align: left; }}
    .header h1 {{ margin: 0; font-size: 22px; font-weight: 700; letter-spacing: -0.5px; }}
    .header p {{ margin: 6px 0 0 0; font-size: 13px; opacity: 0.85; }}
    .content {{ padding: 32px; }}
    .salutation {{ font-size: 16px; font-weight: 600; margin-bottom: 16px; }}
    .status-badge {{ display: inline-block; padding: 6px 14px; background: #F2EDE1; color: #2F5233; font-weight: 700; font-size: 13px; border-radius: 20px; border: 1px solid #E5DEC9; margin-bottom: 20px; }}
    .card {{ background: #FAF7F0; border: 1px solid #E5DEC9; border-radius: 12px; padding: 20px; margin-bottom: 24px; }}
    .row {{ display: flex; justify-content: space-between; margin-bottom: 10px; font-size: 14px; }}
    .row:last-child {{ margin-bottom: 0; }}
    .label {{ color: #1F2A1E; opacity: 0.7; }}
    .val {{ font-weight: 600; text-align: right; }}
    .button-wrap {{ text-align: center; margin: 28px 0; }}
    .btn {{ display: inline-block; background: #2F5233; color: #ffffff !important; text-decoration: none; padding: 12px 28px; border-radius: 10px; font-weight: 700; font-size: 14px; }}
    .footer {{ background: #F2EDE1; padding: 16px 32px; font-size: 12px; color: #1F2A1E; opacity: 0.7; text-align: center; border-top: 1px solid #E5DEC9; }}
  </style>
</head>
<body>
  <div class="container">
    <div class="header">
      <h1>SmartServe</h1>
      <p>Verified Home & Professional Services</p>
    </div>
    <div class="content">
      <div class="salutation">Hello {customer_name},</div>
      <p style="font-size: 14px; line-height: 1.6; margin-top: 0;">We would like to inform you that your booking status has been updated:</p>
      <div><span class="status-badge">{title}</span></div>
      <div class="card">
        <div class="row"><span class="label">Booking Ref:</span><span class="val">{booking_ref}</span></div>
        <div class="row"><span class="label">Service:</span><span class="val">{service_name}</span></div>
        <div class="row"><span class="label">Scheduled Date:</span><span class="val">{scheduled_date}</span></div>
        <div class="row"><span class="label">Scheduled Time:</span><span class="val">{scheduled_time}</span></div>
        <div class="row"><span class="label">Booking Status:</span><span class="val">{status}</span></div>
        <div class="row"><span class="label">Agreed Amount:</span><span class="val">{price_info}</span></div>
        <div class="row"><span class="label">Payment Status:</span><span class="val">{pay_status_info}</span></div>
      </div>
      <div class="button-wrap">
        <a href="{booking_url}" class="btn" target="_blank">View Booking Details</a>
      </div>
    </div>
    <div class="footer">
      This is an automated notification regarding your SmartServe service order. Please do not reply directly to this email.
    </div>
  </div>
</body>
</html>"""
    return subject, body_text, body_html


def _build_whatsapp_content(
    event_type: str,
    customer_name: str,
    booking_ref: str,
    service_name: str,
    scheduled_date: str,
    scheduled_time: str,
    status: str,
    amount: Optional[str] = None,
    payment_status: Optional[str] = None,
    booking_id: Optional[str] = None,
) -> Tuple[str, Dict[str, Any], str]:
    """
    Generate WhatsApp template name, parameters, and formatted fallback text.
    Strictly professional, transactional notification format.
    """
    title = EVENT_TITLES.get(event_type, "Booking Update")
    booking_url = f"{settings.FRONTEND_URL}/bookings/{booking_id or booking_ref}"
    price_info = f"₹{amount}" if amount else "N/A"
    pay_status_info = payment_status or "Pending"

    fallback_text = (
        f"✨ *SmartServe — {title}*\n\n"
        f"Hello *{customer_name}*,\n"
        f"Your booking status has been updated.\n\n"
        f"📋 *Reference:* {booking_ref}\n"
        f"🛠️ *Service:* {service_name}\n"
        f"📅 *Date:* {scheduled_date}\n"
        f"⏰ *Time:* {scheduled_time}\n"
        f"📌 *Status:* {status}\n"
        f"💰 *Amount:* {price_info} ({pay_status_info})\n\n"
        f"👉 *View Booking:* {booking_url}\n\n"
        f"_SmartServe Customer Care_"
    )

    template_name = f"smartserve_{event_type.replace('.', '_')}"
    parameters = {
        "customer_name": customer_name,
        "booking_reference": booking_ref,
        "service_name": service_name,
        "scheduled_date": scheduled_date,
        "scheduled_time": scheduled_time,
        "status": status,
        "amount": price_info,
        "payment_status": pay_status_info,
        "booking_url": booking_url,
    }
    return template_name, parameters, fallback_text


def _resolve_customer_for_booking(db: Session, booking: Booking) -> Optional[Customer]:
    """Safely resolve the registered Customer record associated with the booking."""
    if booking.customer:
        return booking.customer
    if booking.customer_id:
        return db.query(Customer).filter(Customer.id == booking.customer_id).first()
    return None


def notify_booking_event(
    db: Session,
    booking: Booking,
    event_type: str,
    extra_context: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    """
    Central dispatcher for automated booking and payment notifications.
    Processes Email and WhatsApp independently, prevents duplicate sends,
    and logs durable records in notification_logs.
    """
    results: Dict[str, Any] = {"email": None, "whatsapp": None}

    customer = _resolve_customer_for_booking(db, booking)
    customer_name = customer.full_name if customer and customer.full_name else "Valued Customer"
    customer_email = customer.email if customer and customer.email else None
    customer_phone = customer.phone if customer and customer.phone else None

    # If customer profile phone is missing, try checking linked User record
    if not customer_phone and customer and customer.user_id:
        linked_user = db.query(User).filter(User.id == customer.user_id).first()
        if linked_user and getattr(linked_user, "phone", None):
            customer_phone = getattr(linked_user, "phone")

    booking_ref = getattr(booking, "booking_reference", str(booking.id)[:8])
    service_name = getattr(booking, "service_name", "Home Service")
    if hasattr(booking, "service") and booking.service and not service_name:
        service_name = booking.service.name

    scheduled_date = getattr(booking, "scheduled_date", "")
    sched_dt = getattr(booking, "scheduled_time", None)
    if not scheduled_date and sched_dt:
        scheduled_date = sched_dt.strftime("%Y-%m-%d") if hasattr(sched_dt, "strftime") else str(sched_dt)[:10]

    scheduled_time = ""
    if sched_dt:
        scheduled_time = sched_dt.strftime("%I:%M %p") if hasattr(sched_dt, "strftime") else str(sched_dt)

    status_val = str(booking.status.value if hasattr(booking.status, "value") else booking.status)
    payment_status_val = str(booking.payment_status or "Pending")
    amount_val = str(booking.total_price) if booking.total_price is not None else None
    notes = extra_context.get("notes") if extra_context else None

    now_utc = datetime.now(timezone.utc)

    # -------------------------------------------------------------------------
    # CHANNEL 1: EMAIL NOTIFICATION
    # -------------------------------------------------------------------------
    email_idempotency = f"{booking.id}:{event_type}:email"
    if extra_context and extra_context.get("payment_id"):
        email_idempotency += f":{extra_context['payment_id']}"

    existing_email_log = (
        db.query(NotificationLog)
        .filter(NotificationLog.idempotency_key == email_idempotency)
        .first()
    )

    if existing_email_log and existing_email_log.delivery_status in ("Sent", "Delivered"):
        logger.info("Email notification for %s already sent (%s). Skipping duplicate.", email_idempotency, existing_email_log.id)
        results["email"] = {"status": "AlreadySent", "log_id": str(existing_email_log.id)}
    else:
        # Prepare email details
        subject, body_text, body_html = _build_email_content(
            event_type=event_type,
            customer_name=customer_name,
            booking_ref=booking_ref,
            service_name=service_name,
            scheduled_date=scheduled_date,
            scheduled_time=scheduled_time,
            status=status_val,
            amount=amount_val,
            payment_status=payment_status_val,
            notes=notes,
            booking_id=str(booking.id),
        )

        email_status = "Pending"
        email_error = None

        if not customer_email or "@" not in customer_email:
            email_status = "Failed"
            email_error = "Customer email is missing or syntactically invalid"
            logger.warning("Cannot dispatch email: missing recipient for booking %s", booking_ref)
        else:
            try:
                # Dispatch using email_service
                elog = email_service.send_email_dispatch(
                    db=db,
                    recipient_email=customer_email,
                    subject=subject,
                    body_text=body_text,
                    body_html=body_html,
                    template_key=f"booking_{event_type}",
                    actor_email=f"system@smartserve.com",
                )
                if elog and getattr(elog, "status", None) == "Failed":
                    email_status = "Failed"
                    email_error = "Email delivery failed via transport"
                else:
                    email_status = "Sent"
            except Exception as exc:
                email_status = "Failed"
                email_error = f"Email delivery failed: {type(exc).__name__}"
                logger.error("Failed to deliver email for %s: %s", booking_ref, exc)

        if not existing_email_log:
            email_log = NotificationLog(
                id=uuid.uuid4(),
                booking_id=booking.id,
                booking_reference=booking_ref,
                customer_id=customer.id if customer else None,
                event_type=event_type,
                channel="email",
                recipient=customer_email or "missing-email",
                delivery_status=email_status,
                idempotency_key=email_idempotency,
                retry_count=0,
                last_attempt_at=now_utc,
                error_message=email_error,
                metadata_json={
                    "service_name": service_name,
                    "status": status_val,
                    "payment_status": payment_status_val,
                    "amount": amount_val,
                },
                created_at=now_utc,
            )
            db.add(email_log)
        else:
            existing_email_log.delivery_status = email_status
            existing_email_log.last_attempt_at = now_utc
            existing_email_log.error_message = email_error
            email_log = existing_email_log

        try:
            db.commit()
            results["email"] = {"status": email_status, "log_id": str(email_log.id)}
        except Exception as e:
            db.rollback()
            logger.error("Failed to persist email notification log: %s", e)

    # -------------------------------------------------------------------------
    # CHANNEL 2: WHATSAPP NOTIFICATION
    # -------------------------------------------------------------------------
    wa_idempotency = f"{booking.id}:{event_type}:whatsapp"
    if extra_context and extra_context.get("payment_id"):
        wa_idempotency += f":{extra_context['payment_id']}"

    existing_wa_log = (
        db.query(NotificationLog)
        .filter(NotificationLog.idempotency_key == wa_idempotency)
        .first()
    )

    if existing_wa_log and existing_wa_log.delivery_status in ("Sent", "Delivered"):
        logger.info("WhatsApp notification for %s already sent (%s). Skipping duplicate.", wa_idempotency, existing_wa_log.id)
        results["whatsapp"] = {"status": "AlreadySent", "log_id": str(existing_wa_log.id)}
    else:
        norm_phone = validate_and_normalize_phone(customer_phone)
        wa_status = "Pending"
        wa_error = None
        wa_msg_id = None

        if not norm_phone:
            wa_status = "Failed"
            wa_error = "Customer registered phone number is missing or invalid format"
            logger.warning("Cannot dispatch WhatsApp: missing or invalid phone for booking %s", booking_ref)
        else:
            tmpl_name, tmpl_params, fallback_body = _build_whatsapp_content(
                event_type=event_type,
                customer_name=customer_name,
                booking_ref=booking_ref,
                service_name=service_name,
                scheduled_date=scheduled_date,
                scheduled_time=scheduled_time,
                status=status_val,
                amount=amount_val,
                payment_status=payment_status_val,
                booking_id=str(booking.id),
            )
            try:
                adapter = get_whatsapp_adapter()
                wa_res: WhatsAppDeliveryResult = adapter.send_notification(
                    recipient_phone=norm_phone,
                    event_type=event_type,
                    template_name=tmpl_name,
                    parameters=tmpl_params,
                    fallback_text=fallback_body,
                )
                wa_status = wa_res.status
                wa_msg_id = wa_res.provider_message_id
                wa_error = wa_res.error_message
            except Exception as exc:
                wa_status = "Failed"
                wa_error = f"WhatsApp adapter exception: {type(exc).__name__}"
                logger.error("WhatsApp delivery error for %s: %s", booking_ref, exc)

        if not existing_wa_log:
            wa_log = NotificationLog(
                id=uuid.uuid4(),
                booking_id=booking.id,
                booking_reference=booking_ref,
                customer_id=customer.id if customer else None,
                event_type=event_type,
                channel="whatsapp",
                recipient=norm_phone or (customer_phone or "missing-phone"),
                delivery_status=wa_status,
                idempotency_key=wa_idempotency,
                retry_count=0,
                last_attempt_at=now_utc,
                provider_message_id=wa_msg_id,
                error_message=wa_error,
                metadata_json={
                    "service_name": service_name,
                    "status": status_val,
                    "payment_status": payment_status_val,
                    "amount": amount_val,
                },
                created_at=now_utc,
            )
            db.add(wa_log)
        else:
            existing_wa_log.delivery_status = wa_status
            existing_wa_log.last_attempt_at = now_utc
            existing_wa_log.provider_message_id = wa_msg_id
            existing_wa_log.error_message = wa_error
            wa_log = existing_wa_log

        try:
            db.commit()
            results["whatsapp"] = {"status": wa_status, "log_id": str(wa_log.id)}
        except Exception as e:
            db.rollback()
            logger.error("Failed to persist WhatsApp notification log: %s", e)

    return results


def retry_notification(db: Session, notification_id: uuid.UUID, max_retries: int = MAX_NOTIFICATION_RETRIES) -> NotificationLog:
    """
    Controlled retry mechanism for failed notifications.
    Respects maximum retry policy, updates retry count and timestamps.
    """
    log_entry = db.query(NotificationLog).filter(NotificationLog.id == notification_id).first()
    if not log_entry:
        raise ValueError(f"NotificationLog with ID {notification_id} not found.")

    if log_entry.delivery_status in ("Sent", "Delivered"):
        return log_entry

    if log_entry.retry_count >= max_retries:
        raise ValueError(f"Maximum retry limit ({max_retries}) reached for notification {notification_id}.")

    now_utc = datetime.now(timezone.utc)
    log_entry.retry_count += 1
    log_entry.last_attempt_at = now_utc

    booking = log_entry.booking
    if not booking:
        log_entry.error_message = "Associated booking no longer exists for retry."
        log_entry.delivery_status = "Failed"
        db.commit()
        return log_entry

    customer = _resolve_customer_for_booking(db, booking)
    customer_name = customer.full_name if customer and customer.full_name else "Valued Customer"
    booking_ref = log_entry.booking_reference or getattr(booking, "booking_reference", str(booking.id)[:8])
    service_name = getattr(booking, "service_name", "Home Service")
    scheduled_date = getattr(booking, "scheduled_date", "")
    sched_dt = getattr(booking, "scheduled_time", None)
    scheduled_time = sched_dt.strftime("%I:%M %p") if sched_dt and hasattr(sched_dt, "strftime") else str(sched_dt or "")
    status_val = str(booking.status.value if hasattr(booking.status, "value") else booking.status)
    payment_status_val = str(booking.payment_status or "Pending")
    amount_val = str(booking.total_price) if booking.total_price is not None else None

    if log_entry.channel == "email":
        recipient_email = log_entry.recipient
        if not recipient_email or "@" not in recipient_email:
            log_entry.delivery_status = "Failed"
            log_entry.error_message = "Customer email is missing or invalid."
        else:
            subject, body_text, body_html = _build_email_content(
                event_type=log_entry.event_type,
                customer_name=customer_name,
                booking_ref=booking_ref,
                service_name=service_name,
                scheduled_date=scheduled_date,
                scheduled_time=scheduled_time,
                status=status_val,
                amount=amount_val,
                payment_status=payment_status_val,
                booking_id=str(booking.id),
            )
            try:
                elog = email_service.send_email_dispatch(
                    db=db,
                    recipient_email=recipient_email,
                    subject=subject,
                    body_text=body_text,
                    body_html=body_html,
                    template_key=f"retry_{log_entry.event_type}",
                )
                if elog and getattr(elog, "status", None) == "Failed":
                    log_entry.delivery_status = "Failed"
                    log_entry.error_message = "Retry email delivery failed via transport"
                else:
                    log_entry.delivery_status = "Sent"
                    log_entry.error_message = None
            except Exception as exc:
                log_entry.delivery_status = "Failed"
                log_entry.error_message = f"Retry email delivery failed: {type(exc).__name__}"

    elif log_entry.channel == "whatsapp":
        norm_phone = validate_and_normalize_phone(log_entry.recipient)
        if not norm_phone:
            log_entry.delivery_status = "Failed"
            log_entry.error_message = "Customer phone number is missing or invalid format."
        else:
            tmpl_name, tmpl_params, fallback_body = _build_whatsapp_content(
                event_type=log_entry.event_type,
                customer_name=customer_name,
                booking_ref=booking_ref,
                service_name=service_name,
                scheduled_date=scheduled_date,
                scheduled_time=scheduled_time,
                status=status_val,
                amount=amount_val,
                payment_status=payment_status_val,
                booking_id=str(booking.id),
            )
            try:
                adapter = get_whatsapp_adapter()
                wa_res = adapter.send_notification(
                    recipient_phone=norm_phone,
                    event_type=log_entry.event_type,
                    template_name=tmpl_name,
                    parameters=tmpl_params,
                    fallback_text=fallback_body,
                )
                log_entry.delivery_status = wa_res.status
                log_entry.provider_message_id = wa_res.provider_message_id
                log_entry.error_message = wa_res.error_message
            except Exception as exc:
                log_entry.delivery_status = "Failed"
                log_entry.error_message = f"Retry WhatsApp delivery failed: {type(exc).__name__}"

    db.commit()
    db.refresh(log_entry)
    return log_entry
