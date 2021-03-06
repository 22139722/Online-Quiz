"""empty message

Revision ID: 6bdbb24331d3
Revises: 
Create Date: 2020-05-22 21:52:37.800217

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6bdbb24331d3'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('level',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=120), nullable=False),
    sa.Column('image', sa.String(length=120), nullable=False),
    sa.Column('priority', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('image'),
    sa.UniqueConstraint('name'),
    sa.UniqueConstraint('priority')
    )
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=80), nullable=False),
    sa.Column('email', sa.String(length=120), nullable=False),
    sa.Column('password', sa.String(length=120), nullable=False),
    sa.Column('is_admin', sa.Boolean(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email'),
    sa.UniqueConstraint('name')
    )
    op.create_table('question',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('level_id', sa.Integer(), nullable=False),
    sa.Column('question_type', sa.Enum('mcq', 'long_text', 'fuzzy', name='questiontype'), nullable=True),
    sa.ForeignKeyConstraint(['level_id'], ['level.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('user_score_board',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('test_time', sa.TIMESTAMP(), nullable=False),
    sa.Column('level_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['level_id'], ['level.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('long_text_question',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('question_id', sa.Integer(), nullable=False),
    sa.Column('question', sa.Text(), nullable=False),
    sa.ForeignKeyConstraint(['question_id'], ['question.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('mcq_question',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('question_id', sa.Integer(), nullable=False),
    sa.Column('question', sa.Text(), nullable=False),
    sa.Column('answer_one', sa.Text(), nullable=False),
    sa.Column('answer_two', sa.Text(), nullable=False),
    sa.Column('answer_three', sa.Text(), nullable=False),
    sa.Column('answer_four', sa.Text(), nullable=False),
    sa.Column('correct', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['question_id'], ['question.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('score_board_detail',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('scoreboard_id', sa.Integer(), nullable=False),
    sa.Column('level', sa.Text(), nullable=False),
    sa.Column('question_type', sa.Enum('mcq', 'long_text', 'fuzzy', name='scoreboardquestiontype'), nullable=False),
    sa.Column('total_marks', sa.Integer(), nullable=False),
    sa.Column('obtained_marks', sa.Integer(), nullable=False),
    sa.Column('answer_one', sa.Text(), nullable=False),
    sa.Column('answer_two', sa.Text(), nullable=False),
    sa.Column('answer_three', sa.Text(), nullable=False),
    sa.Column('answer_four', sa.Text(), nullable=False),
    sa.Column('correct', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['scoreboard_id'], ['user_score_board.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('short_text_question',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('question_id', sa.Integer(), nullable=False),
    sa.Column('question', sa.Text(), nullable=False),
    sa.Column('answer', sa.Text(), nullable=False),
    sa.ForeignKeyConstraint(['question_id'], ['question.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('long_text_question_answer',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('question_id', sa.Integer(), nullable=False),
    sa.Column('question', sa.Text(), nullable=False),
    sa.Column('answer', sa.Text(), nullable=True),
    sa.ForeignKeyConstraint(['question_id'], ['score_board_detail.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('mcq_question_answer',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('question_id', sa.Integer(), nullable=False),
    sa.Column('question', sa.Text(), nullable=False),
    sa.Column('answer_one', sa.Text(), nullable=False),
    sa.Column('answer_two', sa.Text(), nullable=False),
    sa.Column('answer_three', sa.Text(), nullable=False),
    sa.Column('answer_four', sa.Text(), nullable=False),
    sa.Column('correct', sa.Integer(), nullable=False),
    sa.Column('user_answer', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['question_id'], ['score_board_detail.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('short_text_question_answer',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('question_id', sa.Integer(), nullable=False),
    sa.Column('question', sa.Text(), nullable=False),
    sa.Column('answer', sa.Text(), nullable=False),
    sa.Column('user_answer', sa.Text(), nullable=False),
    sa.ForeignKeyConstraint(['question_id'], ['score_board_detail.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('short_text_question_answer')
    op.drop_table('mcq_question_answer')
    op.drop_table('long_text_question_answer')
    op.drop_table('short_text_question')
    op.drop_table('score_board_detail')
    op.drop_table('mcq_question')
    op.drop_table('long_text_question')
    op.drop_table('user_score_board')
    op.drop_table('question')
    op.drop_table('user')
    op.drop_table('level')
    # ### end Alembic commands ###
