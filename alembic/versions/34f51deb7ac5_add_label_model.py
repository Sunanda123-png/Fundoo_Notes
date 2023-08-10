"""Add Label model

Revision ID: 34f51deb7ac5
Revises: d78f08886898
Create Date: 2023-08-10 01:35:28.478076

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '34f51deb7ac5'
down_revision = 'd78f08886898'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('labels',
    sa.Column('id', sa.BigInteger(), nullable=False),
    sa.Column('name', sa.String(length=20), nullable=True),
    sa.Column('colour_field', sa.String(length=7), nullable=True),
    sa.Column('user_id', sa.BigInteger(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_labels_id'), 'labels', ['id'], unique=True)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_labels_id'), table_name='labels')
    op.drop_table('labels')
    # ### end Alembic commands ###
