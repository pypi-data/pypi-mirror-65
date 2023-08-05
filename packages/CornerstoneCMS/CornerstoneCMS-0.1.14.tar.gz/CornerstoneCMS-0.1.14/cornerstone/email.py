from email.errors import MessageError
from email.message import EmailMessage
from smtplib import SMTP, SMTP_SSL, SMTPException
from ssl import create_default_context

from cornerstone.settings import get_setting


def send_email(to_addrs, subject, message):
    """
    Send an e-mail
    """
    email_hostname = get_setting('email-hostname')
    email_from = get_setting('email-from')
    if not email_hostname or not email_from:
        return False

    email_port = get_setting('email-port')
    email_encryption = get_setting('email-encryption')
    email_needs_auth = get_setting('email-needs-auth')

    if email_encryption in ['STARTSSL', 'SSL/TLS']:
        ssl_context = create_default_context()

    is_success = False
    try:
        # Set up either SSL, STARTSSL or no encryption
        if email_encryption == 'SSL/TLS':
            server = SMTP_SSL(email_hostname, email_port, context=ssl_context)
        else:
            server = SMTP(email_hostname, email_port)
            if email_encryption == 'STARTSSL':
                server.starttls(context=ssl_context)
        # Log in if necessary
        if email_needs_auth:
            server.login(get_setting('email-username'), get_setting('email-password'))
        # Send that e-mail (finally!)
        msg = EmailMessage()
        msg['Subject'] = subject
        msg['From'] = email_from
        msg['To'] = ', '.join(to_addrs)
        msg.set_content(message)
        server.send_message(msg)
        is_success = True
    except (SMTPException, MessageError):
        is_success = False
    finally:
        server.quit()
    return is_success
