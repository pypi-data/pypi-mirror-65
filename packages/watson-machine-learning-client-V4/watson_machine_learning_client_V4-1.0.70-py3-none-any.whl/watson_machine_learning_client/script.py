################################################################################
#
# Licensed Materials - Property of IBM
# (C) Copyright IBM Corp. 2020
# US Government Users Restricted Rights - Use, duplication disclosure restricted
# by GSA ADP Schedule Contract with IBM Corp.
#
################################################################################

from __future__ import print_function
import requests
from watson_machine_learning_client.utils import SPACES_DETAILS_TYPE, INSTANCE_DETAILS_TYPE, MEMBER_DETAILS_TYPE,DATA_ASSETS_DETAILS_TYPE, STR_TYPE, STR_TYPE_NAME, docstring_parameter, meta_props_str_conv, str_type_conv, get_file_from_cos
from watson_machine_learning_client.metanames import ScriptMetaNames
from watson_machine_learning_client.wml_resource import WMLResource
from watson_machine_learning_client.wml_client_error import WMLClientError, ApiRequestFailure
import os

_DEFAULT_LIST_LENGTH = 50


class Script(WMLResource):
    """
    Store and manage your scripts assets.

    """
    ConfigurationMetaNames = ScriptMetaNames()
    """MetaNames for script Assets creation."""

    def __init__(self, client):
        WMLResource.__init__(self, __name__, client)
        self._ICP = client.ICP

    @docstring_parameter({'str_type': STR_TYPE_NAME})
    def get_details(self, script_uid):
        """
            Get script asset details.

            **Parameters**

            .. important::
                #. **script_uid**: Unique id  of script\n
                   **type**: str\n

            **Output**

            .. important::
                **returns**: Metadata of the stored script asset\n
                **return type**: dict\n

            **Example**

             >>> script_details = client.scripts.get_details(script_uid)

        """
        Script._validate_type(script_uid, u'script_uid', STR_TYPE, True)


        if not self._ICP:
            response = requests.get(self._href_definitions.get_data_asset_href(script_uid), params=self._client._params(),
                                    headers=self._client._get_headers())
        else:
            response = requests.get(self._href_definitions.get_data_asset_href(script_uid), params=self._client._params(),
                                      headers=self._client._get_headers(), verify=False)
        if response.status_code == 200:
            return self._get_required_element_from_response(self._handle_response(200, u'get asset details', response))
        else:
            return self._handle_response(200, u'get asset details', response)

    @docstring_parameter({'str_type': STR_TYPE_NAME})
    def store(self, meta_props, file_path):
        """
                Creates a Scripts asset and uploads content to it.

                **Parameters**

                .. important::
                   #. **meta_props**:  Name to be given to the Scripts asset\n

                      **type**: str\n

                   #. **file_path**:  Path to the content file to be uploaded\n

                      **type**: str\n

                **Output**

                .. important::

                    **returns**: metadata of the stored Scripts asset\n
                    **return type**: dict\n

                **Example**
                 >>> metadata = {
                 >>>        client.script.ConfigurationMetaNamess.NAME: 'my first script',
                 >>>        client.script.ConfigurationMetaNames.DESCRIPTION: 'description of the script',
                 >>>        client.script.ConfigurationMetaNames.SOFTWARE_SPEC_UID: '0cdb0f1e-5376-4f4d-92dd-da3b69aa9bda'
                 >>>    }
                 >>>
                 >>> asset_details = client.scripts.store(meta_props=metadata,file_path="/path/to/file")

        """

        #Script._validate_type(name, u'name', str, True)
        Script._validate_type(file_path, u'file_path', str, True)
        script_meta = self.ConfigurationMetaNames._generate_resource_metadata(
            meta_props,
            with_validation=True,
            client=self._client
        )
        return self._create_asset(script_meta, file_path)

    def _create_asset(self, script_meta, file_path):

        ##Step1: Create a data asset
        f = {'file': open(file_path, 'rb')}
        name = script_meta[u'name']

        if script_meta.get('description') is not None:
            desc = script_meta[u'description']
        else:
            desc = ""

        if script_meta.get('software_spec_uid') is not None:
            if script_meta[u'software_spec_uid'] == "":
                raise WMLClientError("Failed while creating a script asset, SOFTWARE_SPEC_UID cannot be empty")
                return

        base_script_asset = {
            "description": "Script File",
            "fields": [
                {
                    "key": "language",
                    "type": "string",
                    "facet": False,
                    "is_array": False,
                    "search_path": "asset.type",
                    "is_searchable_across_types": True
                }
            ],
            "relationships": [
                {
                    "key": "software_spec.id",
                    "target_asset_type": "software_specification",
                    "on_delete_target": "IGNORE",
                    "on_delete": "IGNORE",
                    "on_clone_target": "IGNORE"
                }
            ],
            "name": "script",
            "version": 1
        }

        #check if the software spec specified is base or derived and
        # accordingly update the entity for asset creation


        sw_spec_details = self._client.software_specifications.get_details(script_meta[u'software_spec_uid'])

        if(sw_spec_details[u'entity'][u'software_specification'][u'type'] == 'base'):
            asset_meta = {
                "metadata": {
                    "name": name,
                    "description": desc,
                    "asset_type": "script",
                    "origin_country": "us",
                    "asset_category": "USER"
                },
                "entity": {
                    "script": {
                        "language": {
                            "name": "python3"
                        },
                        "software_spec": {
                            "base_id": script_meta[u'software_spec_uid']
                        }
                    }
                }
            }
        else:
            asset_meta = {
                "metadata": {
                    "name": name,
                    "description": desc,
                    "asset_type": "script",
                    "origin_country": "us",
                    "asset_category": "USER"
                },
                "entity": {
                    "script": {
                        "language": {
                            "name": "python3"
                        },
                        "software_spec": {
                            "id": script_meta[u'software_spec_uid']
                        }
                    }
                }
            }

        #Step1  : Create an asset
        print("Creating Script asset...")

        if self._client.WSD:
            # For WSD the asset creation is done within _wsd_create_asset function using polyglot
            # Thus using the same for data_assets type


            meta_props = {
                    "name": name
            }
            details = Script._wsd_create_asset(self, "script", input_payload, meta_props, file_path)
            return self._get_required_element_from_response(details)
        else:
            if not self._ICP:
                creation_response = requests.post(
                        self._href_definitions.get_data_assets_href(),
                        headers=self._client._get_headers(),
                        params = self._client._params(),
                        json=asset_meta
                )
            else:
                asset_type_response = requests.post(
                    self._wml_credentials['url'] + "/v2/asset_types?",
                    headers=self._client._get_headers(),
                    json=base_script_asset,
                    params=self._client._params(),
                    verify=False
                )
                if asset_type_response.status_code == 201 or asset_type_response.status_code == 409:
                    creation_response = requests.post(
                        self._href_definitions.get_data_assets_href(),
                        headers=self._client._get_headers(),
                        json=asset_meta,
                        params=self._client._params(),
                        verify=False
                    )

            asset_details = self._handle_response(201, u'creating new asset', creation_response)
            #Step2: Create attachment
            if creation_response.status_code == 201:
                asset_id = asset_details["metadata"]["asset_id"]
                attachment_meta = {
                        "asset_type": "script",
                        "name": "attachment_"+asset_id
                    }

                if not self._ICP:
                    attachment_response = requests.post(
                        self._wml_credentials['url']+"/v2/assets/"+asset_id+"/attachments",
                        headers=self._client._get_headers(),
                        params=self._client._params(),
                        json=attachment_meta
                    )
                else:
                    attachment_response = requests.post(
                        self._wml_credentials['url']+"/v2/assets/"+asset_id+"/attachments",
                        headers=self._client._get_headers(),
                        json=attachment_meta,
                        params=self._client._params(),
                        verify=False
                    )
                attachment_details = self._handle_response(201, u'creating new attachment', attachment_response)
                if attachment_response.status_code == 201:
                    attachment_id = attachment_details["attachment_id"]
                    attachment_url = attachment_details["url1"]


                    #Step3: Put content to attachment
                    if not self._ICP:
                        put_response = requests.put(
                            self._wml_credentials['url'] + attachment_url,
                            files = f
                        )
                    else:
                        put_response = requests.put(
                            self._wml_credentials['url'] + attachment_url,
                            files=f,
                            verify=False
                        )
                    if put_response.status_code == 201:
                        # Step4: Complete attachment
                        if not self._ICP:
                            complete_response = requests.post(
                                self._href_definitions.get_attachment_href(asset_id,attachment_id)+"/complete",
                                headers=self._client._get_headers(),
                                params = self._client._params()

                            )
                        else:
                            complete_response = requests.post(
                                self._href_definitions.get_attachment_href(asset_id,attachment_id)+"/complete",
                                headers=self._client._get_headers(),
                                params=self._client._params(),
                                verify=False
                            )
                        if complete_response.status_code == 200:
                            print("SUCCESS")
                            return self._get_required_element_from_response(asset_details)
                        else:
                            self._delete(asset_id)
                            raise WMLClientError("Failed while creating a script asset. Try again.")
                    else:
                        self._delete(asset_id)
                        raise WMLClientError("Failed while creating a script asset. Try again.")
                else:
                    print("SUCCESS")
                    return self._get_required_element_from_response(asset_details)
            else:
                raise WMLClientError("Failed while creating a script asset. Try again.")


    def list(self, limit=None):
        """
           List stored scripts. If limit is set to None there will be only first 50 records shown.

           **Parameters**

           .. important::
                #. **limit**:  limit number of fetched records\n
                   **type**: int\n

           **Output**

           .. important::
                This method only prints the list of all script in a table format.\n
                **return type**: None\n

           **Example**

            >>> client.script.list()
        """

        Script._validate_type(limit, u'limit', int, False)
        href = self._href_definitions.get_search_script_href()

        data = {
                "query": "*:*"
        }
        if limit is not None:
            data.update({"limit": limit})

        if not self._ICP:
            response = requests.post(href, params=self._client._params(), headers=self._client._get_headers(),json=data)
        else:
            response = requests.post(href, params=self._client._params(), headers=self._client._get_headers(),json=data, verify=False)
        self._handle_response(200, u'list assets', response)
        asset_details = self._handle_response(200, u'list assets', response)["results"]
        space_values = [
            (m[u'metadata'][u'name'], m[u'metadata'][u'asset_type'], m["metadata"]["asset_id"]) for
            m in asset_details]

        self._list(space_values, [u'NAME', u'ASSET_TYPE',u'ASSET_ID'], None, _DEFAULT_LIST_LENGTH)

    @docstring_parameter({'str_type': STR_TYPE_NAME})
    def download(self, asset_uid, filename):
        """
            Download the content of a script asset.

            **Parameters**

            .. important::
                 #. **asset_uid**:  The Unique Id of the script asset to be downloaded\n
                    **type**: str\n

                 #. **filename**:  filename to be used for the downloaded file\n
                    **type**: str\n

            **Output**

                 **returns**: Path to the downloaded asset content\n
                 **return type**: str\n

            **Example**

             >>> client.script.download(asset_uid,"script_file.zip")

         """

        Script._validate_type(asset_uid, u'asset_uid', STR_TYPE, True)

        import urllib
        if not self._ICP:
            asset_response = requests.get(self._href_definitions.get_data_asset_href(asset_uid),
                                          params=self._client._params(),
                                          headers=self._client._get_headers())
        else:
            asset_response = requests.get(self._href_definitions.get_data_asset_href(asset_uid),
                                          params=self._client._params(),
                                          headers=self._client._get_headers(), verify=False)
        asset_details = self._handle_response(200, u'get assets', asset_response)

        if self._WSD:
            attachment_url = asset_details['attachments'][0]['object_key']
            artifact_content_url = self._href_definitions.get_wsd_model_attachment_href() + \
                                   urllib.parse.quote('script/' + attachment_url, safe='')

            r = requests.get(artifact_content_url, params=self._client._params(), headers=self._client._get_headers(),
                             stream=True, verify=False)
            if r.status_code != 200:
                raise ApiRequestFailure(u'Failure during {}.'.format("downloading data asset"), r)

            downloaded_asset = r.content
            try:
                with open(filename, 'wb') as f:
                    f.write(downloaded_asset)
                print(u'Successfully saved data asset content to file: \'{}\''.format(filename))
                return os.getcwd() + "/" + filename
            except IOError as e:
                raise WMLClientError(u'Saving data asset with artifact_url: \'{}\'  to local file failed.'.format(filename), e)
        else:
            attachment_id = asset_details["attachments"][0]["id"]
            if not self._ICP:
                response = requests.get(self._href_definitions.get_attachment_href(asset_uid,attachment_id), params=self._client._params(),
                                        headers=self._client._get_headers())
            else:
                response = requests.get(self._href_definitions.get_attachment_href(asset_uid,attachment_id), params=self._client._params(),
                                          headers=self._client._get_headers(), verify=False)
            if response.status_code == 200:
                attachment_signed_url = response.json()["url"]
                if 'connection_id' in asset_details["attachments"][0]:
                    if not self._ICP:
                        att_response = requests.get(attachment_signed_url)
                    else:
                        att_response = requests.get(attachment_signed_url,
                                                    verify=False)
                else:
                    if not self._ICP:
                        att_response = requests.get(self._wml_credentials["url"]+attachment_signed_url)
                    else:
                        att_response = requests.get(self._wml_credentials["url"]+attachment_signed_url,
                                                verify=False)
                if att_response.status_code != 200:
                    raise ApiRequestFailure(u'Failure during {}.'.format("downloading asset"), att_response)

                downloaded_asset = att_response.content
                try:
                    with open(filename, 'wb') as f:
                        f.write(downloaded_asset)
                    print(u'Successfully saved data asset content to file: \'{}\''.format(filename))
                    return os.getcwd() + "/" + filename
                except IOError as e:
                    raise WMLClientError(u'Saving asset with artifact_url to local file: \'{}\' failed.'.format(filename), e)
            else:
                raise WMLClientError("Failed while downloading the asset " + asset_uid)

    @staticmethod
    @docstring_parameter({'str_type': STR_TYPE_NAME})
    def get_uid(asset_details):
        """
                Get Unique Id  of stored script asset.

                **Parameters**

                .. important::

                   #. **asset_details**:  Metadata of the stored script asset\n
                      **type**: dict\n
                      **type**: dict\n

                **Output**

                .. important::

                    **returns**: Unique Id of stored script asset\n
                    **return type**: str\n

                **Example**

                 >>> asset_uid = client.script.get_uid(asset_details)

        """
        Script._validate_type(asset_details, u'asset_details', object, True)
        Script._validate_type_of_details(asset_details, DATA_ASSETS_DETAILS_TYPE)

        return WMLResource._get_required_element_from_dict(asset_details, u'data_assets_details',
                                                           [u'metadata', u'guid'])


    @staticmethod
    @docstring_parameter({'str_type': STR_TYPE_NAME})
    def get_href(asset_details):
        """
            Get url of stored scripts asset.

           **Parameters**

           .. important::
                #. **asset_details**:  stored script details\n
                   **type**: dict\n

           **Output**

           .. important::
                **returns**: href of stored script asset\n
                **return type**: str\n

           **Example**

             >>> asset_details = client.script.get_details(asset_uid)
             >>> asset_href = client.script.get_href(asset_details)

        """
        Script._validate_type(asset_details, u'asset_details', object, True)
        Script._validate_type_of_details(asset_details, DATA_ASSETS_DETAILS_TYPE)

        return WMLResource._get_required_element_from_dict(asset_details, u'asset_details', [u'metadata', u'href'])


    @docstring_parameter({'str_type': STR_TYPE_NAME})
    def delete(self, asset_uid):
        """
            Delete a stored script asset.

            **Parameters**

            .. important::
                #. **asset_uid**:  Unique Id of script asset\n
                   **type**: str\n

            **Output**

            .. important::
                **returns**: status ("SUCCESS" or "FAILED")\n
                **return type**: str\n

            **Example**

             >>> client.script.delete(asset_uid)

        """
        Script._validate_type(asset_uid, u'asset_uid', STR_TYPE, True)

        if not self._ICP:
            response = requests.delete(self._href_definitions.get_asset_href(asset_uid), params=self._client._params(),
                                    headers=self._client._get_headers())
        else:
            response = requests.delete(self._href_definitions.get_asset_href(asset_uid), params=self._client._params(),
                                      headers=self._client._get_headers(), verify=False)
        if response.status_code == 200:
            return self._get_required_element_from_response(response.json())
        else:
            return self._handle_response(204, u'delete assets', response)

    @docstring_parameter({'str_type': STR_TYPE_NAME})
    def _delete(self, asset_uid):
        Script._validate_type(asset_uid, u'asset_uid', STR_TYPE, True)

        if not self._ICP:
            response = requests.delete(self._href_definitions.get_asset_href(asset_uid), params=self._client._params(),
                                       headers=self._client._get_headers())
        else:
            response = requests.delete(self._href_definitions.get_asset_href(asset_uid), params=self._client._params(),
                                       headers=self._client._get_headers(), verify=False)


    def _get_required_element_from_response(self, response_data):

        WMLResource._validate_type(response_data, u'model_definition_response', dict)
        try:
            if self._client.default_space_id is not None:
                new_el = {'metadata': {'space_id': response_data['metadata']['space_id'],
                                       'guid': response_data['metadata']['asset_id'],
                                       'href': response_data['href'],
                                       'asset_type': response_data['metadata']['asset_type'],
                                       'created_at': response_data['metadata']['created_at'],
                                       'last_updated_at': response_data['metadata']['usage']['last_updated_at']
                                       },
                          'entity': response_data['entity']

                          }
            elif self._client.default_project_id is not None:
                if self._client.WSD:

                    href = "/v2/assets/" + response_data['metadata']['asset_id'] + "?" + "project_id=" + response_data['metadata']['project_id']

                    new_el = {'metadata': {'project_id': response_data['metadata']['project_id'],
                                           'guid': response_data['metadata']['asset_id'],
                                           'href': href,
                                           'asset_type': response_data['metadata']['asset_type'],
                                           'created_at': response_data['metadata']['created_at'],
                                           'last_updated_at': response_data['metadata']['usage']['last_updated_at']
                                           },
                              'entity': response_data['entity']

                              }
                else:
                    new_el = {'metadata': {'project_id': response_data['metadata']['project_id'],
                                       'guid': response_data['metadata']['asset_id'],
                                       'href': response_data['href'],
                                       'asset_type': response_data['metadata']['asset_type'],
                                       'created_at': response_data['metadata']['created_at'],
                                       'last_updated_at': response_data['metadata']['usage']['last_updated_at']
                                       },
                             'entity': response_data['entity']

                            }
            return new_el
        except Exception as e:
            raise WMLClientError("Failed to read Response from down-stream service: " + response_data.text)
