"""Add core domain models

Revision ID: 9a429f208192
Revises: 263db664c5fe
Create Date: 2026-04-11 12:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '9a429f208192'
down_revision: Union[str, Sequence[str], None] = '263db664c5fe'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # Create enum types first
    op.execute("CREATE TYPE sessionstatus AS ENUM ('ACTIVE', 'ARCHIVED', 'DELETED')")
    
    # Add new columns to usersession
    op.add_column('usersession', sa.Column('title', sa.String(), nullable=False))
    op.add_column('usersession', sa.Column('last_activity_at', sa.DateTime(), nullable=True))
    op.add_column('usersession', sa.Column('status', postgresql.ENUM('ACTIVE', 'ARCHIVED', 'DELETED', name='sessionstatus'), nullable=True))
    op.add_column('usersession', sa.Column('user_identifier', sa.String(), nullable=False))

    # Create message table
    op.create_table('message',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('session_id', sa.Integer(), nullable=False),
    sa.Column('sender', postgresql.ENUM('USER', 'AI', name='sender'), nullable=False),
    sa.Column('content', sa.String(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('order', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['session_id'], ['usersession.id'], ),
    sa.PrimaryKeyConstraint('id')
    )

    # Create quizrequest table
    op.create_table('quizrequest',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('session_id', sa.Integer(), nullable=False),
    sa.Column('topic', sa.String(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('status', postgresql.ENUM('PENDING', 'GENERATED', 'COMPLETED', name='quizstatus'), nullable=True),
    sa.ForeignKeyConstraint(['session_id'], ['usersession.id'], ),
    sa.PrimaryKeyConstraint('id')
    )

    # Create quizitem table
    op.create_table('quizitem',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('quiz_request_id', sa.Integer(), nullable=False),
    sa.Column('question_text', sa.String(), nullable=False),
    sa.Column('answer_options', postgresql.JSON(astext_type=sa.Text()), nullable=True),
    sa.Column('correct_answer', sa.String(), nullable=False),
    sa.Column('difficulty', sa.String(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['quiz_request_id'], ['quizrequest.id'], ),
    sa.PrimaryKeyConstraint('id')
    )

    # Create submittedanswer table
    op.create_table('submittedanswer',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('quiz_item_id', sa.Integer(), nullable=False),
    sa.Column('session_id', sa.Integer(), nullable=False),
    sa.Column('user_response', sa.String(), nullable=False),
    sa.Column('submitted_at', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['quiz_item_id'], ['quizitem.id'], ),
    sa.ForeignKeyConstraint(['session_id'], ['usersession.id'], ),
    sa.PrimaryKeyConstraint('id')
    )

    # Create evaluationresult table
    op.create_table('evaluationresult',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('submitted_answer_id', sa.Integer(), nullable=False),
    sa.Column('is_correct', sa.Boolean(), nullable=False),
    sa.Column('feedback', sa.String(), nullable=False),
    sa.Column('explanation', sa.String(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['submitted_answer_id'], ['submittedanswer.id'], ),
    sa.PrimaryKeyConstraint('id')
    )

    # Add indexes
    op.create_index(op.f('ix_message_session_id'), 'message', ['session_id'], unique=False)
    op.create_index(op.f('ix_message_created_at'), 'message', ['created_at'], unique=False)
    op.create_index(op.f('ix_quizrequest_session_id'), 'quizrequest', ['session_id'], unique=False)
    op.create_index(op.f('ix_quizitem_quiz_request_id'), 'quizitem', ['quiz_request_id'], unique=False)
    op.create_index(op.f('ix_submittedanswer_quiz_item_id'), 'submittedanswer', ['quiz_item_id'], unique=False)
    op.create_index(op.f('ix_submittedanswer_session_id'), 'submittedanswer', ['session_id'], unique=False)
    op.create_index(op.f('ix_evaluationresult_submitted_answer_id'), 'evaluationresult', ['submitted_answer_id'], unique=False)


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_index(op.f('ix_evaluationresult_submitted_answer_id'), table_name='evaluationresult')
    op.drop_index(op.f('ix_submittedanswer_session_id'), table_name='submittedanswer')
    op.drop_index(op.f('ix_submittedanswer_quiz_item_id'), table_name='submittedanswer')
    op.drop_index(op.f('ix_quizitem_quiz_request_id'), table_name='quizitem')
    op.drop_index(op.f('ix_quizrequest_session_id'), table_name='quizrequest')
    op.drop_index(op.f('ix_message_created_at'), table_name='message')
    op.drop_index(op.f('ix_message_session_id'), table_name='message')
    op.drop_table('evaluationresult')
    op.drop_table('submittedanswer')
    op.drop_table('quizitem')
    op.drop_table('quizrequest')
    op.drop_table('message')
    op.drop_column('usersession', 'user_identifier')
    op.drop_column('usersession', 'status')
    op.drop_column('usersession', 'last_activity_at')
    op.drop_column('usersession', 'title')
    
    # Drop enum types
    op.execute("DROP TYPE IF EXISTS sessionstatus")