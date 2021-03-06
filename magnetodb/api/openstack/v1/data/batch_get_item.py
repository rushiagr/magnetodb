# Copyright 2014 Symantec Corporation
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

from magnetodb import storage
from magnetodb.api import validation
from magnetodb.api import enforce_policy

from magnetodb.api.openstack.v1 import parser
from magnetodb.common import probe


class BatchGetItemController(object):
    """ The BatchGetitem operation returns the attributes
    of one or more items from one or more tables.
    """

    @enforce_policy("mdb:batch_get_item")
    @probe.Probe(__name__)
    def process_request(self, req, body, project_id):
        with probe.Probe(__name__ + '.validation'):
            validation.validate_object(body, "body")

            request_items_json = body.pop(parser.Props.REQUEST_ITEMS, None)
            validation.validate_object(request_items_json,
                                       parser.Props.REQUEST_ITEMS)

            validation.validate_unexpected_props(body, "body")

        # parse request_items
        request_list = parser.Parser.parse_batch_get_request_items(
            request_items_json
        )

        result, unprocessed = storage.execute_get_batch(
            req.context, request_list)

        responses = {}
        for tname, res in result:
            if not res.items:
                continue
            table_items = responses.get(tname, None)
            if table_items is None:
                table_items = []
                responses[tname] = table_items
            item = parser.Parser.format_item_attributes(res.items[0])
            table_items.append(item)

        return {
            'responses': responses,
            'unprocessed_keys': parser.Parser.format_batch_get_unprocessed(
                unprocessed, request_items_json)
        }
