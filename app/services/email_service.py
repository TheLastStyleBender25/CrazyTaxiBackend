import resend
from app.core.config import RESEND_API_KEY
from app.core.logger import logger
from app.models import User
from datetime import datetime


resend.api_key = RESEND_API_KEY


def send_verification_email(
    email: str,
    verification_url: str
):

    resend.Emails.send({
        "from": "noreply@frostbite.co.in",
        "to": email,
        "subject": "Verify your Frostbite account",
        "html": f"""
        <h2>Verify Your Email</h2>
        <p>
        Click the button below to verify your account.
        </p>
        <a href="{verification_url}">
            Verify Email
        </a>
        <p>
        This link will expire in 15 minutes.
        </p>
        """
    })

def verify_email_user(token: str,db):

    user = db.query(User).filter(
        User.verification_token == token
    ).first()

    if not user:
        logger.error(f"no user {token}")
        raise ValueError(f"no user: {token}")

    if datetime.now() > user.verification_expiry:
        logger.error(f"Verification link expired: {token}")
        raise ValueError(f"Verification link expired: {token}")

    user.is_verified = True

    user.verification_token = None

    user.verification_expiry = None

    db.commit()

    return {
        "message":
        "Email verified successfully"
    }