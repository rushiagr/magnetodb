# Copyright 2014 Mirantis Inc.
# All Rights Reserved.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.
import uuid
import datetime
from magnetodb.storage.models import BackupMeta


class BackupManager(object):

    def __init__(self, backup_info_repo):
        self.backup_info_repo = backup_info_repo

    def create_backup(self, context, table_name, backup_name, strategy):
        """
        Create backup

        :param context: current request context
        :param table_name: String, name of the table to backup
        :param backup_name: String, name of the backup to create
        :param strategy: Dict, strategy used for the backup

        :returns:

        :raises: BackendInteractionException
        """

        backup_meta = BackupMeta(
            id=uuid.uuid4(),
            name=backup_name,
            table_name=table_name,
            status=BackupMeta.BACKUP_STATUS_CREATING,
            location='location',
            strategy=strategy,
            start_date_time=datetime.datetime.now())

        return self.backup_info_repo.save(context, backup_meta)

    def describe_backup(self, context, table_name, backup_id):
        return self.backup_info_repo.get(context, table_name, backup_id)

    def delete_backup(self, context, table_name, backup_id):
        return self.backup_info_repo.delete(context, table_name, backup_id)

    def list_backups(self, context, table_name,
                     exclusive_start_backup_id, limit):

        return self.backup_info_repo.list(
            context, table_name, exclusive_start_backup_id, limit)
