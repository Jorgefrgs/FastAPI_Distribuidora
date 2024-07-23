"""Add placas nos veiculos

Revision ID: 2e4a48651864
Revises: f415f0d2aa8f
Create Date: 2024-07-23 14:59:30.361012

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '2e4a48651864'
down_revision: Union[str, None] = 'f415f0d2aa8f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('veiculos', sa.Column('placa', sa.String(), nullable=True))
    op.create_index(op.f('ix_veiculos_placa'), 'veiculos', ['placa'], unique=True)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_veiculos_placa'), table_name='veiculos')
    op.drop_column('veiculos', 'placa')
    # ### end Alembic commands ###