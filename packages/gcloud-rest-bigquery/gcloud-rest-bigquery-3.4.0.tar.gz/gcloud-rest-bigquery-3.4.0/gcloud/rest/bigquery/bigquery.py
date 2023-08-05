from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
from builtins import str
from future import standard_library
standard_library.install_aliases()
from builtins import object
import io
import json
import uuid
from typing import Any
from typing import Callable
from typing import Dict
from typing import List
from typing import Optional
from typing import Union

from gcloud.rest.auth import SyncSession  # pylint: disable=no-name-in-module
from gcloud.rest.auth import BUILD_GCLOUD_REST  # pylint: disable=no-name-in-module
from gcloud.rest.auth import Token  # pylint: disable=no-name-in-module

# Selectively load libraries based on the package
if BUILD_GCLOUD_REST:
    from requests import Session
else:
    from aiohttp import ClientSession as Session


API_ROOT = 'https://www.googleapis.com/bigquery/v2'
SCOPES = [
    'https://www.googleapis.com/auth/bigquery.insertdata',
    'https://www.googleapis.com/auth/bigquery',
]


class Table(object):
    def __init__(self, dataset_name     , table_name     ,
                 project                = None,
                 service_file                                  = None,
                 session                    = None,
                 token                  = None)        :
        self._project = project
        self.dataset_name = dataset_name
        self.table_name = table_name

        self.session = SyncSession(session)
        self.token = token or Token(service_file=service_file, scopes=SCOPES,
                                    session=self.session.session)

    def project(self)       :
        if self._project:
            return self._project

        self._project = self.token.get_project()
        if self._project:
            return self._project

        raise Exception('could not determine project, please set it manually')

    @staticmethod
    def _mk_unique_insert_id(row                )       :
        # pylint: disable=unused-argument
        return uuid.uuid4().hex

    def _make_copy_body(
            self, source_project     , destination_project     ,
            destination_dataset     ,
            destination_table     )                  :
        return {
            'configuration': {
                'copy': {
                    'writeDisposition': 'WRITE_TRUNCATE',
                    'destinationTable': {
                        'projectId': destination_project,
                        'datasetId': destination_dataset,
                        'tableId': destination_table,
                    },
                    'sourceTable': {
                        'projectId': source_project,
                        'datasetId': self.dataset_name,
                        'tableId': self.table_name,
                    }
                }
            }
        }

    @staticmethod
    def _make_insert_body(
            rows                      , **_3to2kwargs                                 )                  :
        insert_id_fn = _3to2kwargs['insert_id_fn']; del _3to2kwargs['insert_id_fn']
        ignore_unknown = _3to2kwargs['ignore_unknown']; del _3to2kwargs['ignore_unknown']
        skip_invalid = _3to2kwargs['skip_invalid']; del _3to2kwargs['skip_invalid']
        return {
            'kind': 'bigquery#tableDataInsertAllRequest',
            'skipInvalidRows': skip_invalid,
            'ignoreUnknownValues': ignore_unknown,
            'rows': [{
                'insertId': insert_id_fn(row),
                'json': row,
            } for row in rows],
        }

    def _make_load_body(
            self, source_uris           , project     )                  :
        return {
            'configuration': {
                'load': {
                    'sourceUris': source_uris,
                    'sourceFormat': 'DATASTORE_BACKUP',
                    'writeDisposition': 'WRITE_TRUNCATE',
                    'destinationTable': {
                        'projectId': project,
                        'datasetId': self.dataset_name,
                        'tableId': self.table_name,
                    },
                },
            },
        }

    def headers(self)                  :
        token = self.token.get()
        return {
            'Authorization': 'Bearer {}'.format((token)),
        }

    # https://cloud.google.com/bigquery/docs/reference/rest/v2/jobs/insert
    def copy(self, destination_project     , destination_dataset     ,
                   destination_table     , session                    = None,
                   timeout      = 60)                  :
        """Copy BQ table to another table in BQ"""
        project = self.project()
        url = '{}/projects/{}/jobs'.format((API_ROOT), (project))

        body = self._make_copy_body(
            project, destination_project,
            destination_dataset, destination_table)
        payload = json.dumps(body).encode('utf-8')

        headers = self.headers()
        headers.update({
            'Content-Length': str(len(payload)),
            'Content-Type': 'application/json',
        })

        s = SyncSession(session) if session else self.session
        resp = s.post(url, data=payload, headers=headers, params=None,
                            timeout=timeout)
        return resp.json()

    # https://cloud.google.com/bigquery/docs/reference/rest/v2/tables/delete
    def delete(self,
                     session                    = None,
                     timeout      = 60)                  :
        """Deletes the table specified by tableId from the dataset."""
        project = self.project()
        url = ('{}/projects/{}/datasets/'
               '{}/tables/{}'.format((API_ROOT), (project), (self.dataset_name), (self.table_name)))

        headers = self.headers()

        s = SyncSession(session) if session else self.session
        resp = s.session.delete(url, headers=headers, params=None,
                                      timeout=timeout)
        try:
            return resp.json()
        except Exception:  # pylint: disable=broad-except
            # For some reason, `gcloud-rest` seems to have intermittent issues
            # parsing this response. In that case, fall back to returning the
            # raw response body.
            try:
                return {'response': resp.text()}
            except (AttributeError, TypeError):
                return {'response': resp.text}

    # https://cloud.google.com/bigquery/docs/reference/rest/v2/tables/get
    def get(
            self, session                    = None,
            timeout      = 60)                  :
        """Gets the specified table resource by table ID."""
        project = self.project()
        url = ('{}/projects/{}/datasets/'
               '{}/tables/{}'.format((API_ROOT), (project), (self.dataset_name), (self.table_name)))

        headers = self.headers()

        s = SyncSession(session) if session else self.session
        resp = s.get(url, headers=headers, timeout=timeout)
        return resp.json()

    # https://cloud.google.com/bigquery/docs/reference/rest/v2/tabledata/insertAll
    def insert(
            self, rows                      , skip_invalid       = False,
            ignore_unknown       = True, session                    = None,
            timeout      = 60, **_3to2kwargs
    )                  :
        if 'insert_id_fn' in _3to2kwargs: insert_id_fn = _3to2kwargs['insert_id_fn']; del _3to2kwargs['insert_id_fn']
        else: insert_id_fn =  None
        """
        Streams data into BigQuery

        By default, each row is assigned a unique insertId. This can be
        customized by supplying an `insert_id_fn` which takes a row and
        returns an insertId.

        The response payload will include an `insertErrors` key if a subset of
        the rows failed to get inserted.
        """
        if not rows:
            return {}

        project = self.project()
        url = ('{}/projects/{}/datasets/{}/'
               'tables/{}/insertAll'.format((API_ROOT), (project), (self.dataset_name), (self.table_name)))

        body = self._make_insert_body(
            rows, skip_invalid=skip_invalid, ignore_unknown=ignore_unknown,
            insert_id_fn=insert_id_fn or self._mk_unique_insert_id)
        payload = json.dumps(body).encode('utf-8')

        headers = self.headers()
        headers.update({
            'Content-Length': str(len(payload)),
            'Content-Type': 'application/json',
        })

        s = SyncSession(session) if session else self.session
        resp = s.post(url, data=payload, headers=headers, params=None,
                            timeout=timeout)
        return resp.json()

    # https://cloud.google.com/bigquery/docs/reference/rest/v2/jobs/insert
    def load(
            self, source_uris           , session                    = None,
            timeout      = 60)                  :
        """Loads entities from storage to BigQuery."""
        if not source_uris:
            return {}

        project = self.project()
        url = '{}/projects/{}/jobs'.format((API_ROOT), (project))

        body = self._make_load_body(source_uris, project)
        payload = json.dumps(body).encode('utf-8')

        headers = self.headers()
        headers.update({
            'Content-Length': str(len(payload)),
            'Content-Type': 'application/json',
        })

        s = SyncSession(session) if session else self.session
        resp = s.post(url, data=payload, headers=headers, params=None,
                            timeout=timeout)
        return resp.json()

    def close(self):
        self.session.close()

    def __enter__(self)           :
        return self

    def __exit__(self, *args)        :
        self.close()
