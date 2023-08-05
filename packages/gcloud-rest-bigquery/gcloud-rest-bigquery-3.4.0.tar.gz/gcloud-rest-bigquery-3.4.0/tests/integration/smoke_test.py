from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
from builtins import str
from builtins import range
from builtins import int
from future import standard_library
standard_library.install_aliases()
import uuid

import pytest
from gcloud.rest.auth import BUILD_GCLOUD_REST  # pylint: disable=no-name-in-module
from gcloud.rest.bigquery import Table
from gcloud.rest.datastore import Datastore  # pylint: disable=no-name-in-module
from gcloud.rest.datastore import Key  # pylint: disable=no-name-in-module
from gcloud.rest.datastore import PathElement  # pylint: disable=no-name-in-module
from gcloud.rest.storage import Storage  # pylint: disable=no-name-in-module

# Selectively load libraries based on the package
if BUILD_GCLOUD_REST:
    from requests import Session
    from time import sleep
else:
    from aiohttp import ClientSession as Session
    from asyncio import sleep


#@pytest.mark.asyncio  # type: ignore
def test_data_is_inserted(creds     , dataset     , project     ,
                                table     )        :
    rows = [{'key': uuid.uuid4().hex, 'value': uuid.uuid4().hex}
            for _ in range(3)]

    with Session() as s:
        # TODO: create this table (with a random name)
        t = Table(dataset, table, project=project, service_file=creds,
                  session=s)
        t.insert(rows)


#@pytest.mark.asyncio  # type: ignore
def test_table_load_copy(creds     , dataset     , project     ,
                               export_bucket_name     )        :
    # pylint: disable=too-many-locals
    # N.B. this test relies on Datastore.export -- see `test_datastore_export`
    # in the `gcloud-rest-datastore` smoke tests.
    kind = 'PublicTestDatastoreExportModel'

    rand_uuid = str(uuid.uuid4())

    with Session() as s:
        ds = Datastore(project=project, service_file=creds, session=s)

        ds.insert(Key(project, [PathElement(kind)]),
                        properties={'rand_str': rand_uuid})

        operation = ds.export(export_bucket_name, kinds=[kind])

        count = 0
        while (count < 10 and operation and
               operation.metadata['common']['state'] == 'PROCESSING'):
            sleep(10)
            operation = ds.get_datastore_operation(operation.name)
            count += 1

        assert operation.metadata['common']['state'] == 'SUCCESSFUL'
        # END: copy from `test_datastore_export`

        uuid_ = str(uuid.uuid4()).replace('-', '_')
        backup_entity_table = 'public_test_backup_entity_{}'.format((uuid_))
        copy_entity_table = '{}_copy'.format((backup_entity_table))

        t = Table(dataset, backup_entity_table, project=project,
                  service_file=creds, session=s)
        gs_prefix = operation.metadata['outputUrlPrefix']
        gs_file = ('{}/all_namespaces/kind_{}/'
                   'all_namespaces_kind_{}.export_metadata'.format((gs_prefix), (kind), (kind)))
        t.load([gs_file])

        sleep(10)

        source_table = t.get()
        assert int(source_table['numRows']) > 0

        t.copy(project, dataset, copy_entity_table)
        sleep(10)
        t1 = Table(dataset, copy_entity_table, project=project,
                   service_file=creds, session=s)
        copy_table = t1.get()
        assert copy_table['numRows'] == source_table['numRows']

        # delete the backup and copy table
        t.delete()
        t1.delete()

        # delete the export file in google storage
        # TODO: confugure the bucket with autodeletion
        prefix_len = len('gs://{}/'.format((export_bucket_name)))
        export_path = operation.metadata['outputUrlPrefix'][prefix_len:]

        storage = Storage(service_file=creds, session=s)
        files = storage.list_objects(export_bucket_name,
                                           params={'prefix': export_path})
        for file in files['items']:
            storage.delete(export_bucket_name, file['name'])
