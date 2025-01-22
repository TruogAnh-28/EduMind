"""modify tables

Revision ID: cb4d73491e75
Revises: 40a38ee6f816
Create Date: 2025-01-17 22:07:41.388299

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = 'cb4d73491e75'
down_revision: Union[str, None] = '40a38ee6f816'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('student_lessons')
    op.alter_column('admins', 'created_at',
               existing_type=postgresql.TIMESTAMP(),
               type_=sa.DateTime(timezone=True),
               existing_nullable=False)
    op.add_column('exercises', sa.Column('deadline', sa.DateTime(), nullable=True))
    op.add_column('exercises', sa.Column('time', sa.Integer(), nullable=True))
    op.add_column('exercises', sa.Column('topic', sa.String(), nullable=True))
    op.add_column('exercises', sa.Column('attempts', sa.Integer(), nullable=True))
    op.add_column('exercises', sa.Column('difficulty', sa.Enum('easy', 'medium', 'hard', name='difficultylevel'), nullable=False))
    op.add_column('exercises', sa.Column('questions', postgresql.JSONB(astext_type=sa.Text()), nullable=False))
    op.drop_column('exercises', 'duration')
    op.drop_column('exercises', 'type')
    op.add_column('lessons', sa.Column('learning_outcomes', postgresql.ARRAY(sa.String()), nullable=True))
    op.add_column('recommend_lessons', sa.Column('lesson_id', sa.UUID(), nullable=True))
    op.drop_constraint('recommend_lessons_id_fkey', 'recommend_lessons', type_='foreignkey')
    op.create_foreign_key(None, 'recommend_lessons', 'lessons', ['lesson_id'], ['id'])
    op.drop_column('recommend_lessons', 'learning_outcomes')
    op.alter_column('students', 'created_at',
               existing_type=postgresql.TIMESTAMP(),
               type_=sa.DateTime(timezone=True),
               existing_nullable=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('students', 'created_at',
               existing_type=sa.DateTime(timezone=True),
               type_=postgresql.TIMESTAMP(),
               existing_nullable=False)
    op.add_column('recommend_lessons', sa.Column('learning_outcomes', postgresql.ARRAY(sa.TEXT()), autoincrement=False, nullable=True))
    op.drop_constraint(None, 'recommend_lessons', type_='foreignkey')
    op.create_foreign_key('recommend_lessons_id_fkey', 'recommend_lessons', 'lessons', ['id'], ['id'])
    op.drop_column('recommend_lessons', 'lesson_id')
    op.drop_column('lessons', 'learning_outcomes')
    op.add_column('exercises', sa.Column('type', postgresql.ENUM('original', 'recommended', name='exercisetype'), autoincrement=False, nullable=False))
    op.add_column('exercises', sa.Column('duration', sa.INTEGER(), autoincrement=False, nullable=True))
    op.drop_column('exercises', 'questions')
    op.drop_column('exercises', 'difficulty')
    op.drop_column('exercises', 'attempts')
    op.drop_column('exercises', 'topic')
    op.drop_column('exercises', 'time')
    op.drop_column('exercises', 'deadline')
    op.alter_column('admins', 'created_at',
               existing_type=sa.DateTime(timezone=True),
               type_=postgresql.TIMESTAMP(),
               existing_nullable=False)
    op.create_table('student_lessons',
    sa.Column('student_id', sa.UUID(), autoincrement=False, nullable=False),
    sa.Column('lesson_id', sa.UUID(), autoincrement=False, nullable=False),
    sa.Column('course_id', sa.UUID(), autoincrement=False, nullable=False),
    sa.Column('bookmark', sa.BOOLEAN(), autoincrement=False, nullable=False),
    sa.ForeignKeyConstraint(['course_id'], ['courses.id'], name='student_lessons_course_id_fkey'),
    sa.ForeignKeyConstraint(['lesson_id'], ['lessons.id'], name='student_lessons_lesson_id_fkey'),
    sa.ForeignKeyConstraint(['student_id'], ['students.id'], name='student_lessons_student_id_fkey'),
    sa.PrimaryKeyConstraint('student_id', 'lesson_id', 'course_id', name='student_lessons_pkey')
    )
    # ### end Alembic commands ###
