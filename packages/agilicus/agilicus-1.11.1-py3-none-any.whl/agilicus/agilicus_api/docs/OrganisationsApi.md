# agilicus_api.OrganisationsApi

All URIs are relative to *https://api.agilicus.com*

Method | HTTP request | Description
------------- | ------------- | -------------
[**delete_sub_org**](OrganisationsApi.md#delete_sub_org) | **DELETE** /v1/orgs/{org_id}/orgs/{sub_org_id} | Delete a sub organisation
[**get_org**](OrganisationsApi.md#get_org) | **GET** /v1/orgs/{org_id} | Get a single organisation
[**get_orgs**](OrganisationsApi.md#get_orgs) | **GET** /v1/orgs | Get all organisations
[**get_sub_orgs**](OrganisationsApi.md#get_sub_orgs) | **GET** /v1/orgs/{org_id}/orgs | Get all sub organisations
[**post_org**](OrganisationsApi.md#post_org) | **POST** /v1/orgs | Create an organisation
[**post_sub_org**](OrganisationsApi.md#post_sub_org) | **POST** /v1/orgs/{org_id}/orgs | Create a sub organisation
[**post_upgrade_orgs**](OrganisationsApi.md#post_upgrade_orgs) | **POST** /v1/orgs/upgrade | utility to upgrade organisations
[**put_org**](OrganisationsApi.md#put_org) | **PUT** /v1/orgs/{org_id} | Create or update an organisation


# **delete_sub_org**
> delete_sub_org(org_id, sub_org_id)

Delete a sub organisation

### Example

* Bearer (JWT) Authentication (token-valid):
```python
from __future__ import print_function
import time
import agilicus_api
from agilicus_api.rest import ApiException
from pprint import pprint
configuration = agilicus_api.Configuration()
# Configure Bearer authorization (JWT): token-valid
configuration.access_token = 'YOUR_BEARER_TOKEN'

# Defining host is optional and default to https://api.agilicus.com
configuration.host = "https://api.agilicus.com"
# Enter a context with an instance of the API client
with agilicus_api.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = agilicus_api.OrganisationsApi(api_client)
    org_id = '1234' # str | Organisation Unique identifier
sub_org_id = '1234' # str | Sub Organisation Unique identifier

    try:
        # Delete a sub organisation
        api_instance.delete_sub_org(org_id, sub_org_id)
    except ApiException as e:
        print("Exception when calling OrganisationsApi->delete_sub_org: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **org_id** | **str**| Organisation Unique identifier | 
 **sub_org_id** | **str**| Sub Organisation Unique identifier | 

### Return type

void (empty response body)

### Authorization

[token-valid](../README.md#token-valid)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: Not defined

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**204** | Organisation was deleted |  -  |
**404** | Organisation does not exist |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_org**
> Organisation get_org(org_id)

Get a single organisation

### Example

* Bearer (JWT) Authentication (token-valid):
```python
from __future__ import print_function
import time
import agilicus_api
from agilicus_api.rest import ApiException
from pprint import pprint
configuration = agilicus_api.Configuration()
# Configure Bearer authorization (JWT): token-valid
configuration.access_token = 'YOUR_BEARER_TOKEN'

# Defining host is optional and default to https://api.agilicus.com
configuration.host = "https://api.agilicus.com"
# Enter a context with an instance of the API client
with agilicus_api.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = agilicus_api.OrganisationsApi(api_client)
    org_id = '1234' # str | Organisation Unique identifier

    try:
        # Get a single organisation
        api_response = api_instance.get_org(org_id)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling OrganisationsApi->get_org: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **org_id** | **str**| Organisation Unique identifier | 

### Return type

[**Organisation**](Organisation.md)

### Authorization

[token-valid](../README.md#token-valid)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Return organisation |  -  |
**404** | Organisation does not exist |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_orgs**
> list[Organisation] get_orgs(limit=limit, org_id=org_id, organisation=organisation, issuer=issuer)

Get all organisations

### Example

* Bearer (JWT) Authentication (token-valid):
```python
from __future__ import print_function
import time
import agilicus_api
from agilicus_api.rest import ApiException
from pprint import pprint
configuration = agilicus_api.Configuration()
# Configure Bearer authorization (JWT): token-valid
configuration.access_token = 'YOUR_BEARER_TOKEN'

# Defining host is optional and default to https://api.agilicus.com
configuration.host = "https://api.agilicus.com"
# Enter a context with an instance of the API client
with agilicus_api.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = agilicus_api.OrganisationsApi(api_client)
    limit = 500 # int | limit the number of rows in the response (optional) (default to 500)
org_id = '1234' # str | Organisation Unique identifier (optional)
organisation = 'agilicus' # str | Organisation Name (optional)
issuer = 'example.com' # str | Organisation issuer (optional)

    try:
        # Get all organisations
        api_response = api_instance.get_orgs(limit=limit, org_id=org_id, organisation=organisation, issuer=issuer)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling OrganisationsApi->get_orgs: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **limit** | **int**| limit the number of rows in the response | [optional] [default to 500]
 **org_id** | **str**| Organisation Unique identifier | [optional] 
 **organisation** | **str**| Organisation Name | [optional] 
 **issuer** | **str**| Organisation issuer | [optional] 

### Return type

[**list[Organisation]**](Organisation.md)

### Authorization

[token-valid](../README.md#token-valid)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Return organisations |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_sub_orgs**
> list[Organisation] get_sub_orgs(org_id, limit=limit)

Get all sub organisations

### Example

* Bearer (JWT) Authentication (token-valid):
```python
from __future__ import print_function
import time
import agilicus_api
from agilicus_api.rest import ApiException
from pprint import pprint
configuration = agilicus_api.Configuration()
# Configure Bearer authorization (JWT): token-valid
configuration.access_token = 'YOUR_BEARER_TOKEN'

# Defining host is optional and default to https://api.agilicus.com
configuration.host = "https://api.agilicus.com"
# Enter a context with an instance of the API client
with agilicus_api.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = agilicus_api.OrganisationsApi(api_client)
    org_id = '1234' # str | Organisation Unique identifier
limit = 500 # int | limit the number of rows in the response (optional) (default to 500)

    try:
        # Get all sub organisations
        api_response = api_instance.get_sub_orgs(org_id, limit=limit)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling OrganisationsApi->get_sub_orgs: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **org_id** | **str**| Organisation Unique identifier | 
 **limit** | **int**| limit the number of rows in the response | [optional] [default to 500]

### Return type

[**list[Organisation]**](Organisation.md)

### Authorization

[token-valid](../README.md#token-valid)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Return sub-organisations |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **post_org**
> Organisation post_org(organisation_admin)

Create an organisation

### Example

* Bearer (JWT) Authentication (token-valid):
```python
from __future__ import print_function
import time
import agilicus_api
from agilicus_api.rest import ApiException
from pprint import pprint
configuration = agilicus_api.Configuration()
# Configure Bearer authorization (JWT): token-valid
configuration.access_token = 'YOUR_BEARER_TOKEN'

# Defining host is optional and default to https://api.agilicus.com
configuration.host = "https://api.agilicus.com"
# Enter a context with an instance of the API client
with agilicus_api.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = agilicus_api.OrganisationsApi(api_client)
    organisation_admin = agilicus_api.OrganisationAdmin() # OrganisationAdmin | 

    try:
        # Create an organisation
        api_response = api_instance.post_org(organisation_admin)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling OrganisationsApi->post_org: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **organisation_admin** | [**OrganisationAdmin**](OrganisationAdmin.md)|  | 

### Return type

[**Organisation**](Organisation.md)

### Authorization

[token-valid](../README.md#token-valid)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**201** | New organisation created |  -  |
**409** | Organisation already exists |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **post_sub_org**
> Organisation post_sub_org(org_id, organisation)

Create a sub organisation

### Example

* Bearer (JWT) Authentication (token-valid):
```python
from __future__ import print_function
import time
import agilicus_api
from agilicus_api.rest import ApiException
from pprint import pprint
configuration = agilicus_api.Configuration()
# Configure Bearer authorization (JWT): token-valid
configuration.access_token = 'YOUR_BEARER_TOKEN'

# Defining host is optional and default to https://api.agilicus.com
configuration.host = "https://api.agilicus.com"
# Enter a context with an instance of the API client
with agilicus_api.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = agilicus_api.OrganisationsApi(api_client)
    org_id = '1234' # str | Organisation Unique identifier
organisation = agilicus_api.Organisation() # Organisation | 

    try:
        # Create a sub organisation
        api_response = api_instance.post_sub_org(org_id, organisation)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling OrganisationsApi->post_sub_org: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **org_id** | **str**| Organisation Unique identifier | 
 **organisation** | [**Organisation**](Organisation.md)|  | 

### Return type

[**Organisation**](Organisation.md)

### Authorization

[token-valid](../README.md#token-valid)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**201** | New sub organisation created |  -  |
**409** | Organisation already exists |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **post_upgrade_orgs**
> post_upgrade_orgs()

utility to upgrade organisations

### Example

* Bearer (JWT) Authentication (token-valid):
```python
from __future__ import print_function
import time
import agilicus_api
from agilicus_api.rest import ApiException
from pprint import pprint
configuration = agilicus_api.Configuration()
# Configure Bearer authorization (JWT): token-valid
configuration.access_token = 'YOUR_BEARER_TOKEN'

# Defining host is optional and default to https://api.agilicus.com
configuration.host = "https://api.agilicus.com"
# Enter a context with an instance of the API client
with agilicus_api.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = agilicus_api.OrganisationsApi(api_client)
    
    try:
        # utility to upgrade organisations
        api_instance.post_upgrade_orgs()
    except ApiException as e:
        print("Exception when calling OrganisationsApi->post_upgrade_orgs: %s\n" % e)
```

### Parameters
This endpoint does not need any parameter.

### Return type

void (empty response body)

### Authorization

[token-valid](../README.md#token-valid)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: Not defined

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | organisations upgraded |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **put_org**
> object put_org(org_id, organisation=organisation)

Create or update an organisation

### Example

* Bearer (JWT) Authentication (token-valid):
```python
from __future__ import print_function
import time
import agilicus_api
from agilicus_api.rest import ApiException
from pprint import pprint
configuration = agilicus_api.Configuration()
# Configure Bearer authorization (JWT): token-valid
configuration.access_token = 'YOUR_BEARER_TOKEN'

# Defining host is optional and default to https://api.agilicus.com
configuration.host = "https://api.agilicus.com"
# Enter a context with an instance of the API client
with agilicus_api.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = agilicus_api.OrganisationsApi(api_client)
    org_id = '1234' # str | Organisation Unique identifier
organisation = agilicus_api.Organisation() # Organisation |  (optional)

    try:
        # Create or update an organisation
        api_response = api_instance.put_org(org_id, organisation=organisation)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling OrganisationsApi->put_org: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **org_id** | **str**| Organisation Unique identifier | 
 **organisation** | [**Organisation**](Organisation.md)|  | [optional] 

### Return type

**object**

### Authorization

[token-valid](../README.md#token-valid)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Organisation updated |  -  |
**404** | Organisation does not exist |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

