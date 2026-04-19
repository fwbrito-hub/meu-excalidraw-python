"""Add auth and data migration

Revision ID: cba4148c7366
Revises: 1129db4de2c3
Create Date: 2026-04-18 22:45:33.170149

"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = 'cba4148c7366'
down_revision: Union[str, Sequence[str], None] = '1129db4de2c3'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade() -> None:
    # 1. Criar tabela de usuários
    op.create_table('users',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('username', sa.String(), nullable=True),
        sa.Column('email', sa.String(), nullable=True),
        sa.Column('hashed_password', sa.String(), nullable=True),
        sa.Column('is_active', sa.Boolean(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_users_email'), 'users', ['email'], unique=True)
    op.create_index(op.f('ix_users_id'), 'users', ['id'], unique=False)
    op.create_index(op.f('ix_users_username'), 'users', ['username'], unique=True)

    # 2. Criar usuário Admin padrão (password: admin123)
    # Hash pré-gerado para admin123
    admin_hash = "$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6L6s57gzRTfG6v/W"
    op.execute(
        f"INSERT INTO users (username, email, hashed_password, is_active) "
        f"VALUES ('admin', 'admin@excalidraw.py', '{admin_hash}', 1)"
    )

    # 3. Alterar tabela Projetos (Usando Batch para suporte ao SQLite)
    with op.batch_alter_table('projetos', schema=None) as batch_op:
        # Adicionar owner_id permitindo null inicialmente
        batch_op.add_column(sa.Column('owner_id', sa.Integer(), nullable=True))
        
        # Criar FK
        batch_op.create_foreign_key('fk_projetos_users', 'users', ['owner_id'], ['id'])

    # 4. Vincular projetos órfãos ao Admin (ID 1)
    op.execute("UPDATE projetos SET owner_id = 1 WHERE owner_id IS NULL")

    # 5. (Opcional) Tornar owner_id obrigatório se desejar
    # No SQLite isso exige recriação da tabela, vamos manter nullable por enquanto para simplicidade didática
    # ou usar batch_op para mudar se for pro.

def downgrade() -> None:
    with op.batch_alter_table('projetos', schema=None) as batch_op:
        batch_op.drop_constraint('fk_projetos_users', type_='foreignkey')
        batch_op.drop_column('owner_id')
    
    op.drop_index(op.f('ix_users_username'), table_name='users')
    op.drop_index(op.f('ix_users_id'), table_name='users')
    op.drop_index(op.f('ix_users_email'), table_name='users')
    op.drop_table('users')
