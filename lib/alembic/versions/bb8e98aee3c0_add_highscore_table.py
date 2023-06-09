"""Add HighScore table

Revision ID: bb8e98aee3c0
Revises: 46bd58a364d5
Create Date: 2023-05-18 19:08:52.853169

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'bb8e98aee3c0'
down_revision = '46bd58a364d5'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('players', sa.Column('highscore_id', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'players', 'highscores', ['highscore_id'], ['id'])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'players', type_='foreignkey')
    op.drop_column('players', 'highscore_id')
    # ### end Alembic commands ###
