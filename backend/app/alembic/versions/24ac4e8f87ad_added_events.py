"""added events

Revision ID: 24ac4e8f87ad
Revises: 1a31ce608336
Create Date: 2024-10-19 02:46:10.478554

"""
from alembic import op
import sqlalchemy as sa
import sqlmodel.sql.sqltypes


# revision identifiers, used by Alembic.
revision = '24ac4e8f87ad'
down_revision = '1a31ce608336'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('event',
    sa.Column('id', sa.Uuid(), nullable=False),
    sa.Column('host', sqlmodel.sql.sqltypes.AutoString(length=20), nullable=False),
    sa.Column('source', sqlmodel.sql.sqltypes.AutoString(length=30), nullable=False),
    sa.Column('service', sqlmodel.sql.sqltypes.AutoString(length=30), nullable=False),
    sa.Column('environment', sqlmodel.sql.sqltypes.AutoString(length=20), nullable=False),
    sa.Column('context', sqlmodel.sql.sqltypes.AutoString(), nullable=True),
    sa.Column('request_id', sqlmodel.sql.sqltypes.AutoString(length=50), nullable=True),
    sa.Column('correlation_id', sqlmodel.sql.sqltypes.AutoString(length=50), nullable=True),
    sa.Column('level', sqlmodel.sql.sqltypes.AutoString(length=20), nullable=False),
    sa.Column('stack_trace', sqlmodel.sql.sqltypes.AutoString(length=1000), nullable=True),
    sa.Column('message', sqlmodel.sql.sqltypes.AutoString(length=255), nullable=False),
    sa.Column('owner_id', sa.Uuid(), nullable=False),
    sa.ForeignKeyConstraint(['owner_id'], ['user.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('event')
    # ### end Alembic commands ###
