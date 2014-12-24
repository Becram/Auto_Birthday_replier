"""empty message

Revision ID: 3cf285288c33
Revises: 2995184a21ba
Create Date: 2014-11-10 15:14:40.027206

"""

# revision identifiers, used by Alembic.
revision = '3cf285288c33'
down_revision = '2995184a21ba'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('questions', sa.Column('question_types', sa.String(length=50), nullable=True))
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('questions', 'question_types')
    ### end Alembic commands ###