# agilicus_api.ApplicationServicesApi

All URIs are relative to *https://api.agilicus.com*

Method | HTTP request | Description
------------- | ------------- | -------------
[**delete_application_service**](ApplicationServicesApi.md#delete_application_service) | **DELETE** /v2/application_services/{app_service_id} | Remove an ApplicationService
[**get_application_service**](ApplicationServicesApi.md#get_application_service) | **GET** /v2/application_services/{app_service_id} | Get a single ApplicationService
[**get_application_services**](ApplicationServicesApi.md#get_application_services) | **GET** /v2/application_services | Get a subset of the ApplicationServices
[**post_application_service**](ApplicationServicesApi.md#post_application_service) | **POST** /v2/application_services | Create an ApplicationService
[**put_application_service**](ApplicationServicesApi.md#put_application_service) | **PUT** /v2/application_services/{app_service_id} | Create or update an Application Service.


# **delete_application_service**
> delete_application_service(app_service_id, org_id)

Remove an ApplicationService

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
    api_instance = agilicus_api.ApplicationServicesApi(api_client)
    app_service_id = 'app_service_id_example' # str | Application Service unique identifier
org_id = 'org_id_example' # str | Organisation unique identifier

    try:
        # Remove an ApplicationService
        api_instance.delete_application_service(app_service_id, org_id)
    except ApiException as e:
        print("Exception when calling ApplicationServicesApi->delete_application_service: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **app_service_id** | **str**| Application Service unique identifier | 
 **org_id** | **str**| Organisation unique identifier | 

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
**204** | Application Service was deleted |  -  |
**404** | Application Service does not exist |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_application_service**
> ApplicationService get_application_service(app_service_id, org_id)

Get a single ApplicationService

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
    api_instance = agilicus_api.ApplicationServicesApi(api_client)
    app_service_id = 'app_service_id_example' # str | Application Service unique identifier
org_id = 'org_id_example' # str | Organisation unique identifier

    try:
        # Get a single ApplicationService
        api_response = api_instance.get_application_service(app_service_id, org_id)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling ApplicationServicesApi->get_application_service: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **app_service_id** | **str**| Application Service unique identifier | 
 **org_id** | **str**| Organisation unique identifier | 

### Return type

[**ApplicationService**](ApplicationService.md)

### Authorization

[token-valid](../README.md#token-valid)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | The ApplicationService was found. |  -  |
**404** | The ApplicationService does not exist. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_application_services**
> list[ApplicationService] get_application_services(org_id)

Get a subset of the ApplicationServices

Retrieves all ApplicationServices owned by the Organisation.

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
    api_instance = agilicus_api.ApplicationServicesApi(api_client)
    org_id = 'org_id_example' # str | Organisation unique identifier

    try:
        # Get a subset of the ApplicationServices
        api_response = api_instance.get_application_services(org_id)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling ApplicationServicesApi->get_application_services: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **org_id** | **str**| Organisation unique identifier | 

### Return type

[**list[ApplicationService]**](ApplicationService.md)

### Authorization

[token-valid](../README.md#token-valid)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | The list of retrieved ApplicationServices |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **post_application_service**
> ApplicationService post_application_service(application_service)

Create an ApplicationService

It is expected that owners for an organisation will provide connectivity to an ApplicationService by defining one here, then adding a reference to an Application's Environment in the ApplicationService's `assignments` list. To see the list of ApplicationServices for which a given Application Environment has access, see that Environment's read only `applications_services` list. 

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
    api_instance = agilicus_api.ApplicationServicesApi(api_client)
    application_service = agilicus_api.ApplicationService() # ApplicationService | 

    try:
        # Create an ApplicationService
        api_response = api_instance.post_application_service(application_service)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling ApplicationServicesApi->post_application_service: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **application_service** | [**ApplicationService**](ApplicationService.md)|  | 

### Return type

[**ApplicationService**](ApplicationService.md)

### Authorization

[token-valid](../README.md#token-valid)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**201** | New ApplicationService created |  -  |
**409** | An ApplicationService with the same name already exists for this organisation. The existing ApplicationService is returned.  |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **put_application_service**
> object put_application_service(app_service_id, application_service=application_service)

Create or update an Application Service.

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
    api_instance = agilicus_api.ApplicationServicesApi(api_client)
    app_service_id = 'app_service_id_example' # str | Application Service unique identifier
application_service = agilicus_api.ApplicationService() # ApplicationService |  (optional)

    try:
        # Create or update an Application Service.
        api_response = api_instance.put_application_service(app_service_id, application_service=application_service)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling ApplicationServicesApi->put_application_service: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **app_service_id** | **str**| Application Service unique identifier | 
 **application_service** | [**ApplicationService**](ApplicationService.md)|  | [optional] 

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
**200** | Application Service updated |  -  |
**404** | Application Service does not exist. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

