# agilicus_api.ApplicationsApi

All URIs are relative to *https://api.agilicus.com*

Method | HTTP request | Description
------------- | ------------- | -------------
[**delete_application**](ApplicationsApi.md#delete_application) | **DELETE** /v2/applications/{app_id} | Remove an application
[**env_config_delete**](ApplicationsApi.md#env_config_delete) | **DELETE** /v2/applications/{app_id}/environments/{env_name}/configs/{env_config_id} | Remove an environment configuration
[**env_config_get**](ApplicationsApi.md#env_config_get) | **GET** /v2/applications/{app_id}/environments/{env_name}/configs/{env_config_id} | Get environment configuration
[**env_config_get_all**](ApplicationsApi.md#env_config_get_all) | **GET** /v2/applications/{app_id}/environments/{env_name}/configs | Get all environment configuration
[**env_config_post**](ApplicationsApi.md#env_config_post) | **POST** /v2/applications/{app_id}/environments/{env_name}/configs | Add an environment configuration row
[**env_config_put**](ApplicationsApi.md#env_config_put) | **PUT** /v2/applications/{app_id}/environments/{env_name}/configs/{env_config_id} | Update environment configuration
[**get_application**](ApplicationsApi.md#get_application) | **GET** /v2/applications/{app_id} | Get a application
[**get_applications**](ApplicationsApi.md#get_applications) | **GET** /v2/applications | Get applications
[**get_environment**](ApplicationsApi.md#get_environment) | **GET** /v2/applications/{app_id}/environments/{env_name} | Get an environment
[**list_environment_configs_all_apps**](ApplicationsApi.md#list_environment_configs_all_apps) | **GET** /v2/environment_configs | Get all environment configuration for a given organisation.
[**post_application**](ApplicationsApi.md#post_application) | **POST** /v2/applications | Create an application
[**put_application**](ApplicationsApi.md#put_application) | **PUT** /v2/applications/{app_id} | Create or update an application
[**put_environment**](ApplicationsApi.md#put_environment) | **PUT** /v2/applications/{app_id}/environments/{env_name} | Update an environment


# **delete_application**
> delete_application(app_id, org_id=org_id)

Remove an application

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
    api_instance = agilicus_api.ApplicationsApi(api_client)
    app_id = 'app_id_example' # str | Application unique identifier
org_id = '1234' # str | Organisation Unique identifier (optional)

    try:
        # Remove an application
        api_instance.delete_application(app_id, org_id=org_id)
    except ApiException as e:
        print("Exception when calling ApplicationsApi->delete_application: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **app_id** | **str**| Application unique identifier | 
 **org_id** | **str**| Organisation Unique identifier | [optional] 

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
**204** | Application was deleted |  -  |
**404** | Application does not exist |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **env_config_delete**
> env_config_delete(app_id, env_name, env_config_id, maintenance_org_id)

Remove an environment configuration

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
    api_instance = agilicus_api.ApplicationsApi(api_client)
    app_id = 'app_id_example' # str | Application unique identifier
env_name = 'env_name_example' # str | The name of an Environment
env_config_id = 'env_config_id_example' # str | environment configuration id
maintenance_org_id = 'maintenance_org_id_example' # str | Organisation unique identifier for an object being maintained by an organisation different than it. 

    try:
        # Remove an environment configuration
        api_instance.env_config_delete(app_id, env_name, env_config_id, maintenance_org_id)
    except ApiException as e:
        print("Exception when calling ApplicationsApi->env_config_delete: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **app_id** | **str**| Application unique identifier | 
 **env_name** | **str**| The name of an Environment | 
 **env_config_id** | **str**| environment configuration id | 
 **maintenance_org_id** | **str**| Organisation unique identifier for an object being maintained by an organisation different than it.  | 

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
**204** | Environment configuration was deleted |  -  |
**404** | Environment configuration does not exist |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **env_config_get**
> EnvironmentConfig env_config_get(app_id, env_name, env_config_id, maintenance_org_id)

Get environment configuration

Retrieve environment configuration 

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
    api_instance = agilicus_api.ApplicationsApi(api_client)
    app_id = 'app_id_example' # str | Application unique identifier
env_name = 'env_name_example' # str | The name of an Environment
env_config_id = 'env_config_id_example' # str | environment configuration id
maintenance_org_id = 'maintenance_org_id_example' # str | Organisation unique identifier for an object being maintained by an organisation different than it. 

    try:
        # Get environment configuration
        api_response = api_instance.env_config_get(app_id, env_name, env_config_id, maintenance_org_id)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling ApplicationsApi->env_config_get: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **app_id** | **str**| Application unique identifier | 
 **env_name** | **str**| The name of an Environment | 
 **env_config_id** | **str**| environment configuration id | 
 **maintenance_org_id** | **str**| Organisation unique identifier for an object being maintained by an organisation different than it.  | 

### Return type

[**EnvironmentConfig**](EnvironmentConfig.md)

### Authorization

[token-valid](../README.md#token-valid)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Environment configuration successfully retrieved. |  -  |
**403** | Reading this environment is not permitted. This could happen due to insufficient permissions within your organisation.  |  -  |
**404** | The Environment configuration does not exist. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **env_config_get_all**
> list[EnvironmentConfig] env_config_get_all(app_id, env_name, maintenance_org_id)

Get all environment configuration

Retrieve all environment configuration 

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
    api_instance = agilicus_api.ApplicationsApi(api_client)
    app_id = 'app_id_example' # str | Application unique identifier
env_name = 'env_name_example' # str | The name of an Environment
maintenance_org_id = 'maintenance_org_id_example' # str | Organisation unique identifier for an object being maintained by an organisation different than it. 

    try:
        # Get all environment configuration
        api_response = api_instance.env_config_get_all(app_id, env_name, maintenance_org_id)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling ApplicationsApi->env_config_get_all: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **app_id** | **str**| Application unique identifier | 
 **env_name** | **str**| The name of an Environment | 
 **maintenance_org_id** | **str**| Organisation unique identifier for an object being maintained by an organisation different than it.  | 

### Return type

[**list[EnvironmentConfig]**](EnvironmentConfig.md)

### Authorization

[token-valid](../README.md#token-valid)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Environment configuration successfully retrieved. |  -  |
**403** | Reading this environment is not permitted. This could happen due to insufficient permissions within your organisation.  |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **env_config_post**
> EnvironmentConfig env_config_post(app_id, env_name, environment_config)

Add an environment configuration row

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
    api_instance = agilicus_api.ApplicationsApi(api_client)
    app_id = 'app_id_example' # str | Application unique identifier
env_name = 'env_name_example' # str | The name of an Environment
environment_config = agilicus_api.EnvironmentConfig() # EnvironmentConfig | 

    try:
        # Add an environment configuration row
        api_response = api_instance.env_config_post(app_id, env_name, environment_config)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling ApplicationsApi->env_config_post: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **app_id** | **str**| Application unique identifier | 
 **env_name** | **str**| The name of an Environment | 
 **environment_config** | [**EnvironmentConfig**](EnvironmentConfig.md)|  | 

### Return type

[**EnvironmentConfig**](EnvironmentConfig.md)

### Authorization

[token-valid](../README.md#token-valid)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**201** | New environment config row created |  -  |
**409** | Environment configuration requested already exists |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **env_config_put**
> EnvironmentConfig env_config_put(app_id, env_name, env_config_id, environment_config)

Update environment configuration

Update environment configuration 

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
    api_instance = agilicus_api.ApplicationsApi(api_client)
    app_id = 'app_id_example' # str | Application unique identifier
env_name = 'env_name_example' # str | The name of an Environment
env_config_id = 'env_config_id_example' # str | environment configuration id
environment_config = agilicus_api.EnvironmentConfig() # EnvironmentConfig | 

    try:
        # Update environment configuration
        api_response = api_instance.env_config_put(app_id, env_name, env_config_id, environment_config)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling ApplicationsApi->env_config_put: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **app_id** | **str**| Application unique identifier | 
 **env_name** | **str**| The name of an Environment | 
 **env_config_id** | **str**| environment configuration id | 
 **environment_config** | [**EnvironmentConfig**](EnvironmentConfig.md)|  | 

### Return type

[**EnvironmentConfig**](EnvironmentConfig.md)

### Authorization

[token-valid](../README.md#token-valid)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | The Environment configuration was successfully updated |  -  |
**403** | Reading this environment is not permitted. This could happen due to insufficient permissions within your organisation.  |  -  |
**404** | The Environment configuration does not exist. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_application**
> Application get_application(app_id, org_id=org_id, assigned_org_id=assigned_org_id)

Get a application

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
    api_instance = agilicus_api.ApplicationsApi(api_client)
    app_id = 'app_id_example' # str | Application unique identifier
org_id = '1234' # str | Organisation Unique identifier (optional)
assigned_org_id = 'assigned_org_id_example' # str | Organisation unique identifier for an assigned object (optional)

    try:
        # Get a application
        api_response = api_instance.get_application(app_id, org_id=org_id, assigned_org_id=assigned_org_id)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling ApplicationsApi->get_application: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **app_id** | **str**| Application unique identifier | 
 **org_id** | **str**| Organisation Unique identifier | [optional] 
 **assigned_org_id** | **str**| Organisation unique identifier for an assigned object | [optional] 

### Return type

[**Application**](Application.md)

### Authorization

[token-valid](../README.md#token-valid)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Return Application |  -  |
**404** | Application does not exist |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_applications**
> list[Application] get_applications(org_id=org_id, assigned_org_id=assigned_org_id, maintained=maintained, assigned=assigned, owned=owned, updated_since=updated_since)

Get applications

Retrieves all applications related to the org_id. Different types of relationship may be queried by setting the appropriate flags:   - assigned: Has an Environment assigned to the organisation.   - owned: Owned by the organisation.   - maintained: Has an Environment maintained by the organisation. Any combination of the relationship flags may be set. Note that if the organisation does not own the Application, but maintains or is assigned an environment only those assignments and environments for the querying organisation will be shown. 

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
    api_instance = agilicus_api.ApplicationsApi(api_client)
    org_id = '1234' # str | Organisation Unique identifier (optional)
assigned_org_id = 'assigned_org_id_example' # str | Organisation unique identifier for an assigned object (optional)
maintained = True # bool | Query for Applications maintained by the `org_id`. These are Applications which have an Environment whose `maintenance_org_id` is the `org_id`.  (optional)
assigned = True # bool | Query for Applications assigned to the `org_id`. These are Applications with at least one Environment assigned to the `org_id`.  (optional)
owned = True # bool | Query for Applications owned by the `org_id`. (optional)
updated_since = '2015-07-07T15:49:51.230+02:00' # datetime | query since updated (optional)

    try:
        # Get applications
        api_response = api_instance.get_applications(org_id=org_id, assigned_org_id=assigned_org_id, maintained=maintained, assigned=assigned, owned=owned, updated_since=updated_since)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling ApplicationsApi->get_applications: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **org_id** | **str**| Organisation Unique identifier | [optional] 
 **assigned_org_id** | **str**| Organisation unique identifier for an assigned object | [optional] 
 **maintained** | **bool**| Query for Applications maintained by the &#x60;org_id&#x60;. These are Applications which have an Environment whose &#x60;maintenance_org_id&#x60; is the &#x60;org_id&#x60;.  | [optional] 
 **assigned** | **bool**| Query for Applications assigned to the &#x60;org_id&#x60;. These are Applications with at least one Environment assigned to the &#x60;org_id&#x60;.  | [optional] 
 **owned** | **bool**| Query for Applications owned by the &#x60;org_id&#x60;. | [optional] 
 **updated_since** | **datetime**| query since updated | [optional] 

### Return type

[**list[Application]**](Application.md)

### Authorization

[token-valid](../README.md#token-valid)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Return applications |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_environment**
> Environment get_environment(app_id, env_name, org_id)

Get an environment

This allows an environment maintainer to get an environment they maintain. 

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
    api_instance = agilicus_api.ApplicationsApi(api_client)
    app_id = 'app_id_example' # str | Application unique identifier
env_name = 'env_name_example' # str | The name of an Environment
org_id = 'org_id_example' # str | Organisation unique identifier

    try:
        # Get an environment
        api_response = api_instance.get_environment(app_id, env_name, org_id)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling ApplicationsApi->get_environment: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **app_id** | **str**| Application unique identifier | 
 **env_name** | **str**| The name of an Environment | 
 **org_id** | **str**| Organisation unique identifier | 

### Return type

[**Environment**](Environment.md)

### Authorization

[token-valid](../README.md#token-valid)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Environment successfully retrieved. |  -  |
**403** | Reading this environment is not permitted. This could happen due to insufficient permissions within your organisation.  |  -  |
**404** | Environment does not exist |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **list_environment_configs_all_apps**
> InlineResponse200 list_environment_configs_all_apps(maintenance_org_id, limit=limit)

Get all environment configuration for a given organisation.

Retrieve all environment configuration for a organisation. 

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
    api_instance = agilicus_api.ApplicationsApi(api_client)
    maintenance_org_id = 'maintenance_org_id_example' # str | Organisation unique identifier for an object being maintained by an organisation different than it. 
limit = 500 # int | limit the number of rows in the response (optional) (default to 500)

    try:
        # Get all environment configuration for a given organisation.
        api_response = api_instance.list_environment_configs_all_apps(maintenance_org_id, limit=limit)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling ApplicationsApi->list_environment_configs_all_apps: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **maintenance_org_id** | **str**| Organisation unique identifier for an object being maintained by an organisation different than it.  | 
 **limit** | **int**| limit the number of rows in the response | [optional] [default to 500]

### Return type

[**InlineResponse200**](InlineResponse200.md)

### Authorization

[token-valid](../README.md#token-valid)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Environment configuration successfully retrieved. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **post_application**
> Application post_application(application)

Create an application

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
    api_instance = agilicus_api.ApplicationsApi(api_client)
    application = agilicus_api.Application() # Application | 

    try:
        # Create an application
        api_response = api_instance.post_application(application)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling ApplicationsApi->post_application: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **application** | [**Application**](Application.md)|  | 

### Return type

[**Application**](Application.md)

### Authorization

[token-valid](../README.md#token-valid)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**201** | New application created |  -  |
**409** | Application already exists |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **put_application**
> object put_application(app_id, application=application)

Create or update an application

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
    api_instance = agilicus_api.ApplicationsApi(api_client)
    app_id = 'app_id_example' # str | Application unique identifier
application = agilicus_api.Application() # Application |  (optional)

    try:
        # Create or update an application
        api_response = api_instance.put_application(app_id, application=application)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling ApplicationsApi->put_application: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **app_id** | **str**| Application unique identifier | 
 **application** | [**Application**](Application.md)|  | [optional] 

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
**200** | Application updated |  -  |
**404** | Application does not exists |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **put_environment**
> object put_environment(app_id, env_name, environment=environment)

Update an environment

This allows an environment maintainer to update the environment. Note that the maintenence_organisation in the body must match the existing one. 

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
    api_instance = agilicus_api.ApplicationsApi(api_client)
    app_id = 'app_id_example' # str | Application unique identifier
env_name = 'env_name_example' # str | The name of an Environment
environment = agilicus_api.Environment() # Environment |  (optional)

    try:
        # Update an environment
        api_response = api_instance.put_environment(app_id, env_name, environment=environment)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling ApplicationsApi->put_environment: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **app_id** | **str**| Application unique identifier | 
 **env_name** | **str**| The name of an Environment | 
 **environment** | [**Environment**](Environment.md)|  | [optional] 

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
**200** | Environment updated |  -  |
**403** | Modifying this environment is not permitted. This could happen due to insufficient permissions within your organisation, or because you tried to change the maintenence organisation of an environment.  |  -  |
**404** | The Environment does not exist. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

