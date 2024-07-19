"""Inicializar tablas de usuario, alumno y pago

Revision ID: 0131cb84c6c8
Revises: 
Create Date: 2024-07-19 00:09:06.231415

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0131cb84c6c8'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('alumno',
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('nombre', sa.String(length=100), nullable=False),
    sa.Column('nombre_apoderado', sa.String(length=100), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('usuario',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('nombre_usuario', sa.String(length=150), nullable=False),
    sa.Column('contraseña', sa.String(length=150), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('nombre_usuario')
    )
    op.create_table('pago',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('alumno_id', sa.UUID(), nullable=False),
    sa.Column('monto', sa.Float(), nullable=False),
    sa.Column('concepto', sa.String(length=100), nullable=False),
    sa.Column('fecha_hora', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['alumno_id'], ['alumno.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.drop_table('payment')
    op.drop_table('user')
    op.drop_table('student')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('student',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('name', sa.VARCHAR(length=100), nullable=False),
    sa.Column('guardian_name', sa.VARCHAR(length=100), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('user',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('username', sa.VARCHAR(length=150), nullable=False),
    sa.Column('password', sa.VARCHAR(length=150), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('username')
    )
    op.create_table('payment',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('student_id', sa.INTEGER(), nullable=False),
    sa.Column('amount', sa.FLOAT(), nullable=False),
    sa.Column('concept', sa.VARCHAR(length=100), nullable=False),
    sa.Column('date_time', sa.DATETIME(), nullable=False),
    sa.ForeignKeyConstraint(['student_id'], ['student.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.drop_table('pago')
    op.drop_table('usuario')
    op.drop_table('alumno')
    # ### end Alembic commands ###
