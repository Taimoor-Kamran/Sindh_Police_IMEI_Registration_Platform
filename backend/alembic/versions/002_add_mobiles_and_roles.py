"""Add mobiles, ownership_history, audit_logs tables and shop keeper fields to users

Revision ID: 002
Revises: 001
Create Date: 2024-01-15 00:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

revision: str = "002"
down_revision: Union[str, None] = "001"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Add shop keeper columns to users
    op.add_column("users", sa.Column("shop_license_number", sa.String(50), nullable=True))
    op.add_column("users", sa.Column("is_shop_verified", sa.Boolean(), server_default=sa.text("false")))

    # Create mobiles table
    op.create_table(
        "mobiles",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("imei", sa.String(15), nullable=False, unique=True),
        sa.Column("mobile_number", sa.String(15), nullable=False),
        sa.Column("brand", sa.String(100), nullable=True),
        sa.Column("model", sa.String(100), nullable=True),
        sa.Column("current_owner_cnic", sa.String(15), nullable=False),
        sa.Column(
            "registered_by_user_id",
            sa.Integer(),
            sa.ForeignKey("users.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column("registration_type", sa.String(10), nullable=False),
        sa.Column("status", sa.String(20), server_default="active"),
        sa.Column("invoice_path", sa.String(500), nullable=True),
        sa.Column("registration_date", sa.DateTime(), server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(), server_default=sa.func.now()),
        sa.Column("notes", sa.Text(), nullable=True),
    )

    op.create_index("idx_mobiles_imei", "mobiles", ["imei"])
    op.create_index("idx_mobiles_current_owner_cnic", "mobiles", ["current_owner_cnic"])
    op.create_index("idx_mobiles_registered_by_user_id", "mobiles", ["registered_by_user_id"])

    # Create ownership_history table
    op.create_table(
        "ownership_history",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column(
            "mobile_id",
            sa.Integer(),
            sa.ForeignKey("mobiles.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column("imei", sa.String(15), nullable=False),
        sa.Column("old_owner_cnic", sa.String(15), nullable=False),
        sa.Column("new_owner_cnic", sa.String(15), nullable=False),
        sa.Column(
            "transferred_by_user_id",
            sa.Integer(),
            sa.ForeignKey("users.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column("transfer_type", sa.String(20), nullable=False),
        sa.Column("transfer_date", sa.DateTime(), server_default=sa.func.now()),
        sa.Column("notes", sa.Text(), nullable=True),
    )

    op.create_index("idx_ownership_mobile_id", "ownership_history", ["mobile_id"])
    op.create_index("idx_ownership_imei", "ownership_history", ["imei"])
    op.create_index("idx_ownership_old_owner", "ownership_history", ["old_owner_cnic"])
    op.create_index("idx_ownership_new_owner", "ownership_history", ["new_owner_cnic"])

    # Create audit_logs table
    op.create_table(
        "audit_logs",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column(
            "user_id",
            sa.Integer(),
            sa.ForeignKey("users.id", ondelete="SET NULL"),
            nullable=True,
        ),
        sa.Column("action_type", sa.String(50), nullable=False),
        sa.Column("entity_type", sa.String(50), nullable=True),
        sa.Column("entity_id", sa.Integer(), nullable=True),
        sa.Column("description", sa.Text(), nullable=False),
        sa.Column("metadata", sa.JSON(), nullable=True),
        sa.Column("ip_address", sa.String(45), nullable=True),
        sa.Column("user_agent", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(), server_default=sa.func.now()),
    )

    op.create_index("idx_audit_user_id", "audit_logs", ["user_id"])
    op.create_index("idx_audit_action_type", "audit_logs", ["action_type"])
    op.create_index("idx_audit_created_at", "audit_logs", ["created_at"])


def downgrade() -> None:
    op.drop_table("audit_logs")
    op.drop_table("ownership_history")
    op.drop_table("mobiles")
    op.drop_column("users", "is_shop_verified")
    op.drop_column("users", "shop_license_number")
