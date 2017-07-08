from cached_property import cached_property
from flask import current_app, g, session
from typing import List, Optional

from zeus.config import db
from zeus.models import RepositoryAccess, User


class Tenant(object):
    def __init__(self, repository_ids: Optional[str]=None):
        self.repository_ids = repository_ids or []

    def __repr__(self):
        return '<{} repository_ids={}>'.format(type(self).__name__, self.repository_ids)

    @classmethod
    def from_user(cls, user: User):
        if not user:
            return cls()

        # TODO(dcramer); we currently grant access to all repos
        return UserTenant(user_id=user.id)


class UserTenant(Tenant):
    def __init__(self, user_id: str):
        self.user_id = user_id

    def __repr__(self):
        return '<{} user_id={}>'.format(type(self).__name__, self.user_id)

    @cached_property
    def repository_ids(self) -> List:
        if not self.user_id:
            return None

        return [
            r[0]
            for r in db.session.query(RepositoryAccess.repository_id).filter(
                RepositoryAccess.user_id == self.user_id,
            )
        ]

    @classmethod
    def from_user(cls, user):
        if not user:
            return cls()

        # TODO(dcramer); we currently grant access to all repos
        return cls(user_id=user.id)


def get_user_from_request() -> Optional[User]:
    uid = session.get('uid')
    if not uid:
        return None
    return User.query.get(uid)


def get_current_user() -> Optional[User]:
    rv = getattr(g, 'current_user', None)
    if not rv:
        rv = get_user_from_request()
        g.current_user = rv
    return rv


def get_tenant_from_request():
    # auth = validate_auth(request.headers.get('Authorization'))
    user = get_current_user()
    return Tenant.from_user(user)


def set_current_tenant(tenant: Tenant):
    current_app.logger.info('Binding tenant as %r', tenant)
    g.current_tenant = tenant


def get_current_tenant() -> Tenant:
    rv = getattr(g, 'current_tenant', None)
    if rv is None:
        rv = get_tenant_from_request()
        set_current_tenant(rv)
    return rv