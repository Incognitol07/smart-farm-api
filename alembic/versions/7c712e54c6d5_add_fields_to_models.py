'''add fields to models (batch mode)

Revision ID: 7c712e54c6d5
Revises: 
Create Date: 2025-04-24 17:22:48.538168
'''  
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = '7c712e54c6d5'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema using batch operations for SQLite."""
    # Add new columns that SQLite supports directly
    op.add_column('commands', sa.Column('executed_at', sa.DateTime(timezone=True), nullable=True))
    op.add_column('commands', sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('(CURRENT_TIMESTAMP)'), nullable=True))

    # Use batch_alter_table to handle alter_column and drop_column for SQLite
    with op.batch_alter_table('actuators') as batch_op:
        batch_op.alter_column(
            'id',
            existing_type=sa.VARCHAR(),
            type_=sa.Integer(),
            existing_nullable=False,
            autoincrement=True
        )
        batch_op.alter_column(
            'state',
            existing_type=sa.VARCHAR(length=20),
            type_=sa.Enum('ON', 'OFF', 'ERROR', name='actuatorstate'),
            existing_nullable=True
        )
        batch_op.drop_column('type')
        batch_op.create_index(op.f('ix_actuators_id'), ['id'], unique=False)

    with op.batch_alter_table('commands') as batch_op:
        batch_op.alter_column(
            'id',
            existing_type=sa.VARCHAR(),
            type_=sa.Integer(),
            existing_nullable=False,
            autoincrement=True
        )
        batch_op.alter_column(
            'command',
            existing_type=sa.VARCHAR(length=20),
            type_=sa.Enum('ON', 'OFF', 'ERROR', name='actuatorstate'),
            existing_nullable=True
        )
        batch_op.drop_column('timestamp')
        batch_op.create_index(op.f('ix_commands_id'), ['id'], unique=False)

    with op.batch_alter_table('readings') as batch_op:
        batch_op.alter_column(
            'id',
            existing_type=sa.VARCHAR(),
            type_=sa.Integer(),
            existing_nullable=False,
            autoincrement=True
        )
        batch_op.create_index(op.f('ix_readings_id'), ['id'], unique=False)

    with op.batch_alter_table('sensors') as batch_op:
        batch_op.alter_column(
            'id',
            existing_type=sa.VARCHAR(),
            type_=sa.Integer(),
            existing_nullable=False,
            autoincrement=True
        )
        batch_op.create_index(op.f('ix_sensors_id'), ['id'], unique=False)


def downgrade() -> None:
    """Downgrade schema using batch operations for SQLite."""
    # Reverse operations in batches
    with op.batch_alter_table('sensors') as batch_op:
        batch_op.drop_index(op.f('ix_sensors_id'))
        batch_op.alter_column(
            'id',
            existing_type=sa.Integer(),
            type_=sa.VARCHAR(),
            existing_nullable=False,
            autoincrement=True
        )

    with op.batch_alter_table('readings') as batch_op:
        batch_op.drop_index(op.f('ix_readings_id'))
        batch_op.alter_column(
            'id',
            existing_type=sa.Integer(),
            type_=sa.VARCHAR(),
            existing_nullable=False,
            autoincrement=True
        )

    with op.batch_alter_table('commands') as batch_op:
        batch_op.drop_index(op.f('ix_commands_id'))
        batch_op.alter_column(
            'command',
            existing_type=sa.Enum('ON', 'OFF', 'ERROR', name='actuatorstate'),
            type_=sa.VARCHAR(length=20),
            existing_nullable=True
        )
        batch_op.alter_column(
            'id',
            existing_type=sa.Integer(),
            type_=sa.VARCHAR(),
            existing_nullable=False,
            autoincrement=True
        )
        batch_op.add_column(sa.Column('timestamp', sa.DATETIME(), server_default=sa.text('(CURRENT_TIMESTAMP)'), nullable=True))

    with op.batch_alter_table('actuators') as batch_op:
        batch_op.drop_index(op.f('ix_actuators_id'))
        batch_op.alter_column(
            'state',
            existing_type=sa.Enum('ON', 'OFF', 'ERROR', name='actuatorstate'),
            type_=sa.VARCHAR(length=20),
            existing_nullable=True
        )
        batch_op.alter_column(
            'id',
            existing_type=sa.Integer(),
            type_=sa.VARCHAR(),
            existing_nullable=False,
            autoincrement=True
        )
        batch_op.add_column(sa.Column('type', sa.VARCHAR(length=50), nullable=True))
    # Drop columns added in upgrade
    op.drop_column('commands', 'created_at')
    op.drop_column('commands', 'executed_at')
    op.drop_column('actuators', 'name')
