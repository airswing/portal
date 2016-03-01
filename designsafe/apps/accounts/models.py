from django.db import models
from django.db import connections, DatabaseError
import logging
import six

logger = logging.getLogger(__name__)


class NEESUser(object):

    def __init__(self, **kwargs):
        for k, v in six.iteritems(kwargs):
            setattr(self, k, v)

    _lookup_sql = "SELECT u.username, u.email, p.givenName, p.middleName, p.surname, " \
                  "p.organization, p.countryresident, p.countryorigin, p.phone, " \
                  "a.address1, a.address2, a.addressCity, a.addressRegion, " \
                  "a.addressPostal, a.addressCountry " \
                  "FROM jos_users u JOIN jos_xprofiles p ON p.uidNumber = u.id " \
                  "LEFT JOIN jos_xprofiles_address a ON a.uidNumber = u.id " \
                  "WHERE u.email = %s"

    @classmethod
    def lookup_user(cls, email):
        if 'nees_users' in connections:
            cursor = connections['nees_users'].cursor()
            try:
                cursor.execute(cls._lookup_sql, [email])
                columns = [col[0] for col in cursor.description]
                return [
                    cls(**dict(zip(columns, row)))
                    for row in cursor.fetchall()
                ]
            finally:
                cursor.close()
        else:
            logger.error('Database connection for `nees_users` is not defined')
            raise DatabaseError('The NEES users database connection is unavailable.')
