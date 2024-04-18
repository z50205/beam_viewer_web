"""add revise_filenam

Revision ID: 2a8f119f90bb
Revises: 85639d478de0
Create Date: 2024-04-05 02:35:56.553492

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2a8f119f90bb'
down_revision = '85639d478de0'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('beam__inform', schema=None) as batch_op:
        batch_op.add_column(sa.Column('revise_filename', sa.String(length=36), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('beam__inform', schema=None) as batch_op:
        batch_op.drop_column('revise_filename')

    # ### end Alembic commands ###