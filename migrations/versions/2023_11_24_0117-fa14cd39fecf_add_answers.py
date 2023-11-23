"""add answers

Revision ID: fa14cd39fecf
Revises: cc4ad4e15f13
Create Date: 2023-11-24 01:17:37.171830

"""
from typing import Sequence, Union

from alembic import op

import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'fa14cd39fecf'
down_revision: Union[str, None] = 'cc4ad4e15f13'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        'answers',
        sa.Column('pk', sa.Integer(), nullable=False),
        sa.Column('question_id', sa.Integer(), nullable=False),
        sa.Column('is_correct', sa.Boolean(), nullable=False),
        sa.ForeignKeyConstraint(['question_id'], ['questions.pk']),
        sa.PrimaryKeyConstraint('pk'),
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('answers')
    # ### end Alembic commands ###
