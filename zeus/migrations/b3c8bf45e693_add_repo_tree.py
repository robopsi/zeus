"""add_repo_tree

Revision ID: b3c8bf45e693
Revises: 1cb2c54f3831
Create Date: 2018-03-30 15:13:33.197801

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b3c8bf45e693'
down_revision = '1cb2c54f3831'
branch_labels = ()
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('repository_ref',
                    sa.Column('name', sa.String(), nullable=False),
                    sa.Column('repository_id', zeus.db.types.guid.GUID(), nullable=False),
                    sa.ForeignKeyConstraint(
                        ['repository_id'], ['repository.id'], ondelete='CASCADE'),
                    sa.PrimaryKeyConstraint('name')
                    )
    op.create_index(
        op.f('ix_repository_ref_repository_id'),
        'repository_ref',
        ['repository_id'],
        unique=False)
    op.create_table('repository_tree',
                    sa.Column('ref_id', zeus.db.types.guid.GUID(), nullable=False),
                    sa.Column('order', sa.Integer(), nullable=False),
                    sa.Column('revision_sha', sa.String(length=40), nullable=True),
                    sa.Column('repository_id', zeus.db.types.guid.GUID(), nullable=False),
                    sa.ForeignKeyConstraint(['ref_id'], ['author.id'], ),
                    sa.ForeignKeyConstraint(
                        ['repository_id'], ['repository.id'], ondelete='CASCADE'),
                    sa.ForeignKeyConstraint(['revision_sha'], ['revision.sha'], ),
                    sa.PrimaryKeyConstraint('ref_id', 'order'),
                    sa.UniqueConstraint('ref_id', 'revision_sha', name='unq_tree_revision')
                    )
    op.create_index(
        op.f('ix_repository_tree_repository_id'),
        'repository_tree',
        ['repository_id'],
        unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_repository_tree_repository_id'), table_name='repository_tree')
    op.drop_table('repository_tree')
    op.drop_index(op.f('ix_repository_ref_repository_id'), table_name='repository_ref')
    op.drop_table('repository_ref')
    # ### end Alembic commands ###
