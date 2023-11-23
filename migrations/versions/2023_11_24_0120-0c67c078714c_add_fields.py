"""add fields

Revision ID: 0c67c078714c
Revises: 18bc66f5334a
Create Date: 2023-11-24 01:20:14.482614

"""
from typing import Sequence, Union

from alembic import op

import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '0c67c078714c'
down_revision: Union[str, None] = '18bc66f5334a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        'fields',
        sa.Column('pk', sa.Integer(), nullable=False),
        sa.Column('game_id', sa.Integer(), nullable=False),
        sa.Column('owner_id', sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(['game_id'], ['games.pk']),
        sa.ForeignKeyConstraint(['owner_id'], ['players.pk']),
        sa.PrimaryKeyConstraint('pk'),
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('fields')
    # ### end Alembic commands ###
