"""create prospectivity results

Revision ID: prospectivity001
Revises: a6c2196f98fe
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "prospectivity001"
down_revision: Union[str, Sequence[str], None] = "a6c2196f98fe"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "prospectivity_results",

        sa.Column(
            "id",
            sa.Integer(),
            primary_key=True,
            nullable=False,
        ),

        sa.Column(
            "mine_id",
            sa.Integer(),
            sa.ForeignKey(
                "mines.id",
                ondelete="CASCADE",
            ),
            nullable=False,
        ),

        sa.Column(
            "prospectivity_score",
            sa.Float(),
            nullable=False,
        ),

        sa.Column(
            "classification",
            sa.String(length=30),
            nullable=False,
        ),

        sa.Column(
            "geological_score",
            sa.Float(),
            nullable=False,
        ),

        sa.Column(
            "remote_sensing_score",
            sa.Float(),
            nullable=False,
        ),

        sa.Column(
            "structural_score",
            sa.Float(),
            nullable=False,
        ),

        sa.Column(
            "historical_score",
            sa.Float(),
            nullable=False,
        ),

        sa.Column(
            "explanation",
            sa.Text(),
            nullable=False,
        ),

        sa.Column(
            "model_version",
            sa.String(length=50),
            nullable=False,
        ),

        sa.Column(
            "created_at",
            sa.DateTime(),
            nullable=False,
            server_default=sa.text("CURRENT_TIMESTAMP"),
        ),
    )

    op.create_index(
        "ix_prospectivity_results_id",
        "prospectivity_results",
        ["id"],
        unique=False,
    )

    op.create_index(
        "ix_prospectivity_results_mine_id",
        "prospectivity_results",
        ["mine_id"],
        unique=False,
    )


def downgrade() -> None:
    op.drop_index(
        "ix_prospectivity_results_mine_id",
        table_name="prospectivity_results",
    )

    op.drop_index(
        "ix_prospectivity_results_id",
        table_name="prospectivity_results",
    )

    op.drop_table("prospectivity_results")