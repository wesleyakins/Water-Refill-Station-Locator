"""empty message

Revision ID: 62aebfc3ab16
Revises: dec236fcf8fe
Create Date: 2023-03-01 15:03:21.724945

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '62aebfc3ab16'
down_revision = 'dec236fcf8fe'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('points',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('reward_points', sa.Integer(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('points')
    # ### end Alembic commands ###
