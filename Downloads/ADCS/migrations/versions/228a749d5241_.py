"""empty message

Revision ID: 228a749d5241
Revises: b5cd7133cbf
Create Date: 2014-11-14 11:40:21.958269

"""

# revision identifiers, used by Alembic.
revision = '228a749d5241'
down_revision = 'b5cd7133cbf'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('projects', sa.Column('concluding_info_file', sa.String(length=255), nullable=True))
    op.add_column('projects', sa.Column('start_info_file', sa.String(length=255), nullable=True))
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('projects', 'start_info_file')
    op.drop_column('projects', 'concluding_info_file')
    ### end Alembic commands ###