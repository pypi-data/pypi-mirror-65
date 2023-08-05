# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.

from aliyunsdkcore.request import RpcRequest
from aliyunsdkcsb.endpoint import endpoint_data

class PublishUnionCasServiceRequest(RpcRequest):

	def __init__(self):
		RpcRequest.__init__(self, 'CSB', '2017-11-18', 'PublishUnionCasService')
		self.set_protocol_type('https')
		self.set_method('POST')
		if hasattr(self, "endpoint_map"):
			setattr(self, "endpoint_map", endpoint_data.getEndpointMap())
		if hasattr(self, "endpoint_regional"):
			setattr(self, "endpoint_regional", endpoint_data.getEndpointRegional())


	def get_CasCsbName(self):
		return self.get_query_params().get('CasCsbName')

	def set_CasCsbName(self,CasCsbName):
		self.add_query_param('CasCsbName',CasCsbName)

	def get_Data(self):
		return self.get_body_params().get('Data')

	def set_Data(self,Data):
		self.add_body_params('Data', Data)