# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import logging
logger = logging.getLogger("webapi")

import socorro.webapi.webapiService as webapi
import socorro.database.database as db
import web

class Bugzilla(webapi.JsonServiceBase):

  def __init__(self, configContext):
    super(Bugzilla, self).__init__(configContext)
    logger.debug('Bugzilla __init__')

  # use HTTP POST with multiple "id" args
  # curl -X POST -F id='js::mjit::EnterMethodJIT(JSContext*, JSStackFrame*, void*, js::Value*)' -F id='js::gc::MarkObject' 'http://localhost:8085/bugs/by/signatures'
  uri = '/bugs/by/signatures'

  def post(self, *args):
    columns = ['signature','bug_id']

    getSignatures = """
                    /* socorro.services.bugzilla getSignatures */
                    SELECT ba.signature, bugs.id FROM bugs
                    JOIN bug_associations AS ba ON bugs.id = ba.bug_id
                      AND signature = ANY (%s)"""

    signatures = (web.input(id=[]).id,)

    connection = self.database.connection()
    cursor = connection.cursor()
    cursor.execute(getSignatures, signatures)

    result = []

    for row in cursor.fetchall():
      rowAsDict = dict(zip(columns, row))
      result.append(rowAsDict)

    return {'bug_associations': result}
