"""Create initial police admin user.

Usage:
    cd backend
    python -m scripts.create_admin
"""
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlmodel import Session, select
from app.database import engine
from app.models.user import User
from app.utils.security import hash_password


def create_admin():
    with Session(engine) as session:
        existing = session.exec(
            select(User).where(User.role == "police_admin")
        ).first()
        if existing:
            print(f"Admin user already exists: {existing.username}")
            return

        admin = User(
            full_name="Police Admin",
            cnic="00000-0000000-0",
            mobile="03000000000",
            email="admin@sindhpolice.gov.pk",
            username="policeadmin",
            password_hash=hash_password("Admin@123456"),
            role="police_admin",
            is_active=True,
        )
        session.add(admin)
        session.commit()
        print("Admin user created successfully!")
        print("Username: policeadmin")
        print("Password: Admin@123456")
        print("IMPORTANT: Change the password after first login!")


if __name__ == "__main__":
    create_admin()
