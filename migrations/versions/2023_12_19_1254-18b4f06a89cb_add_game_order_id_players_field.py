"""add game_order_id players field

Revision ID: 18b4f06a89cb
Revises: 4ad64efd1b0f
Create Date: 2023-12-19 12:54:42.413706

"""
from typing import Sequence, Union

from alembic import op

import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '18b4f06a89cb'
down_revision: Union[str, None] = '4ad64efd1b0f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('players', sa.Column('game_order_id', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'players', 'games', ['game_order_id'], ['id'])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'players', type_='foreignkey')
    op.drop_column('players', 'game_order_id')
    # ### end Alembic commands ###
