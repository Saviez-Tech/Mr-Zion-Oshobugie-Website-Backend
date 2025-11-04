import requests
from django.conf import settings

def send_course_payment_email(email, full_name, course_title, access_code, course_link):
    """Send a payment confirmation email via SendGrid HTTP API."""
    try:
        subject = f"Payment Confirmed for {course_title} 🎉"
        from_email = settings.DEFAULT_FROM_EMAIL

        # Plain text fallback
        text_content = f"""
Hi {full_name},

Your payment for "{course_title}" has been confirmed successfully.

Here are your access details:
Access Code: {access_code}
Course Link: {course_link}

You can now begin your course and start learning right away!

Thank you for choosing MrZion.
"""

        # HTML version
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Payment Successful</title>
        </head>
        <body style="margin:0; padding:0; font-family: Arial, sans-serif; background-color:#f4f8f4;">
            <table align="center" width="100%" cellpadding="0" cellspacing="0"
                style="max-width:600px; background-color:#ffffff; border-radius:10px; overflow:hidden; box-shadow:0 2px 12px rgba(0,0,0,0.1);">

                <tr>
                    <td style="background-color:#2563eb; padding:25px; text-align:center; color:#ffffff; font-size:28px; font-weight:bold;">
                        MrZion Courses
                    </td>
                </tr>

                <tr>
                    <td style="padding:40px 30px; text-align:center; color:#333333;">
                        <h2 style="color:#2563eb;">Payment Successful 🎉</h2>
                        <p style="font-size:16px;">Hi {full_name},</p>
                        <p style="font-size:16px;">
                            Your payment for <strong>{course_title}</strong> has been successfully confirmed.
                        </p>

                        <div style="margin:25px 0; background-color:#f4f8f4; border-radius:8px; padding:20px;">
                            <p><strong>Access Code:</strong>
                                <span style="font-size:18px; font-weight:bold; color:#2563eb;">{access_code}</span>
                            </p>
                            <p><strong>Course Link:</strong>
                                <a href="{course_link}" style="color:#2563eb;">{course_link}</a>
                            </p>
                        </div>

                        <a href="{course_link}"
                            style="display:inline-block; margin-top:25px; background-color:#2563eb; color:#ffffff; text-decoration:none;
                            padding:14px 32px; border-radius:6px; font-weight:bold; font-size:16px;">
                            Access Your Course
                        </a>
                    </td>
                </tr>

                <tr>
                    <td style="padding:20px; background-color:#f6f6f6; text-align:center; font-size:13px; color:#777;">
                        If you have any issues, contact 
                        <a href="mailto:mrzion.noreply@gmail.com" style="color:#2563eb;">smrzion.noreply@gmail.com</a><br><br>
                        &copy; 2025 MrZion. All rights reserved.
                    </td>
                </tr>
            </table>
        </body>
        </html>
        """

        # ✅ Send via SendGrid HTTP API
        headers = {
            "Authorization": f"Bearer {settings.SENDGRID_API_KEY}",
            "Content-Type": "application/json",
        }

        data = {
            "personalizations": [
                {"to": [{"email": email}], "subject": subject}
            ],
            "from": {"email": from_email, "name": "MrZion Courses"},
            "content": [
                {"type": "text/plain", "value": text_content},
                {"type": "text/html", "value": html_content}
            ]
        }

        response = requests.post("https://api.sendgrid.com/v3/mail/send", json=data, headers=headers)

        if response.status_code not in [200, 202]:
            print(f"❌ SendGrid Error ({response.status_code}): {response.text}")
        else:
            print(f"✅ Payment confirmation email sent successfully to {email}")

    except Exception as e:
        print(f"❌ Error sending payment confirmation email: {e}")
        raise e





def send_service_payment_email(email, full_name, service_name):
    """Send a service payment confirmation email via SendGrid HTTP API."""
    try:
        subject = f"Service Payment Received – {service_name}"
        from_email = settings.DEFAULT_FROM_EMAIL

        # Plain text fallback
        text_content = f"""
Hi {full_name},

Your payment for the service "{service_name}" has been received successfully.

Our team will contact you shortly to proceed with the next steps.

Thank you for choosing MrZion.
"""

        # HTML content
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head><meta charset="UTF-8"></head>
        <body style="margin:0;padding:0;font-family:Arial,sans-serif;background-color:#f4f8f4;">
            <table align="center" width="100%" cellpadding="0" cellspacing="0"
                style="max-width:600px;background-color:#ffffff;border-radius:10px;overflow:hidden;
                       box-shadow:0 2px 12px rgba(0,0,0,0.1);">
                <tr>
                    <td style="background-color:#2563eb;padding:25px;text-align:center;color:#fff;
                               font-size:28px;font-weight:bold;">
                        MrZion Services
                    </td>
                </tr>
                <tr>
                    <td style="padding:40px 30px;text-align:center;color:#333;">
                        <h2 style="color:#2563eb;">Payment Received 💼</h2>
                        <p style="font-size:16px;">Hi {full_name},</p>
                        <p style="font-size:16px;">
                            We’ve received your payment for the service <strong>{service_name}</strong>.
                        </p>
                        <p style="font-size:16px;">
                            Our team will reach out to you shortly to proceed with your request.
                        </p>
                        <p style="margin-top:30px;">Thank you for trusting <strong>MrZion</strong>!</p>
                    </td>
                </tr>
                <tr>
                    <td style="padding:20px;background-color:#f6f6f6;text-align:center;
                               font-size:13px;color:#777;">
                        For any questions, contact 
                        <a href="mailto:mrzion.noreply@gmail.com" style="color:#2563eb;">mrzion.noreply@gmail.com</a><br><br>
                        &copy; 2025 MrZion. All rights reserved.
                    </td>
                </tr>
            </table>
        </body>
        </html>
        """

        # SendGrid HTTP Request
        headers = {
            "Authorization": f"Bearer {settings.SENDGRID_API_KEY}",
            "Content-Type": "application/json",
        }

        data = {
            "personalizations": [
                {"to": [{"email": email}], "subject": subject}
            ],
            "from": {"email": from_email, "name": "MrZion Services"},
            "content": [
                {"type": "text/plain", "value": text_content},
                {"type": "text/html", "value": html_content}
            ]
        }

        response = requests.post("https://api.sendgrid.com/v3/mail/send", json=data, headers=headers)
        if response.status_code not in [200, 202]:
            print(f"❌ SendGrid Error ({response.status_code}): {response.text}")
        else:
            print(f"✅ Service payment email sent successfully to {email}")

    except Exception as e:
        print(f"❌ Error sending service payment email: {e}")
        raise e





def send_book_payment_email(email, full_name, book_title, book_links):
    """
    Send a book payment confirmation email via SendGrid HTTP API.
    book_links: dict like {"Kindle": "...", "Paperback": "...", "PDF": "..."}
    """
    try:
        subject = f"Payment Confirmed for {book_title} 📚"
        from_email = settings.DEFAULT_FROM_EMAIL

        text_links = "\n".join([f"{k}: {v}" for k, v in book_links.items() if v])
        text_content = f"""
Hi {full_name},

Your payment for "{book_title}" has been confirmed successfully.

Here are your book access links:
{text_links}

Thank you for choosing MrZion.
"""

        link_html = "".join([
            f'<p><strong>{k}:</strong> <a href="{v}" style="color:#2563eb;">{v}</a></p>'
            for k, v in book_links.items() if v
        ])

        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head><meta charset="UTF-8"></head>
        <body style="margin:0;padding:0;font-family:Arial,sans-serif;background-color:#f4f8f4;">
            <table align="center" width="100%" cellpadding="0" cellspacing="0"
                style="max-width:600px;background-color:#ffffff;border-radius:10px;overflow:hidden;
                       box-shadow:0 2px 12px rgba(0,0,0,0.1);">
                <tr>
                    <td style="background-color:#2563eb;padding:25px;text-align:center;color:#fff;
                               font-size:28px;font-weight:bold;">
                        MrZion Store
                    </td>
                </tr>
                <tr>
                    <td style="padding:40px 30px;text-align:center;color:#333;">
                        <h2 style="color:#2563eb;">Payment Successful 📚</h2>
                        <p style="font-size:16px;">Hi {full_name},</p>
                        <p style="font-size:16px;">Your payment for <strong>{book_title}</strong> has been confirmed.</p>
                        <p style="font-size:16px;">Here are your book links:</p>
                        {link_html}
                        <p style="margin-top:30px;">Enjoy your reading, and thank you for supporting <strong>MrZion</strong>!</p>
                    </td>
                </tr>
                <tr>
                    <td style="padding:20px;background-color:#f6f6f6;text-align:center;
                               font-size:13px;color:#777;">
                        For any questions, contact 
                        <a href="mrzion.noreply@gmail.com" style="color:#2563eb;">mrzion.noreply@gmail.com</a><br><br>
                        &copy; 2025 MrZion. All rights reserved.
                    </td>
                </tr>
            </table>
        </body>
        </html>
        """

        headers = {
            "Authorization": f"Bearer {settings.SENDGRID_API_KEY}",
            "Content-Type": "application/json",
        }

        data = {
            "personalizations": [
                {"to": [{"email": email}], "subject": subject}
            ],
            "from": {"email": from_email, "name": "MrZion Store"},
            "content": [
                {"type": "text/plain", "value": text_content},
                {"type": "text/html", "value": html_content}
            ]
        }

        response = requests.post("https://api.sendgrid.com/v3/mail/send", json=data, headers=headers)
        if response.status_code not in [200, 202]:
            print(f"❌ SendGrid Error ({response.status_code}): {response.text}")
        else:
            print(f"✅ Book payment email sent successfully to {email}")

    except Exception as e:
        print(f"❌ Error sending book payment email: {e}")
        raise e
