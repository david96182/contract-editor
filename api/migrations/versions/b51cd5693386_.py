"""empty message

Revision ID: b51cd5693386
Revises: e8794dc419d1
Create Date: 2024-06-18 23:12:51.788597

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b51cd5693386'
down_revision = 'e8794dc419d1'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('contracts', schema=None) as batch_op:
        batch_op.add_column(sa.Column('employee_id', sa.Integer(), nullable=False))
        batch_op.drop_constraint('contracts_employer_id_fkey', type_='foreignkey')
        batch_op.create_foreign_key(None, 'employees', ['employee_id'], ['id'])
        batch_op.drop_column('employer_id')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('contracts', schema=None) as batch_op:
        batch_op.add_column(sa.Column('employer_id', sa.INTEGER(), autoincrement=False, nullable=False))
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.create_foreign_key('contracts_employer_id_fkey', 'employees', ['employer_id'], ['id'])
        batch_op.drop_column('employee_id')

    # ### end Alembic commands ###