# agilicus_api.MetricsApi

All URIs are relative to *https://api.agilicus.com*

Method | HTTP request | Description
------------- | ------------- | -------------
[**metrics_metrics_query_active**](MetricsApi.md#metrics_metrics_query_active) | **GET** /v1/metrics/{org_id}/users:active | 
[**metrics_metrics_query_top**](MetricsApi.md#metrics_metrics_query_top) | **GET** /v1/metrics/{org_id}/users:top | View top users


# **metrics_metrics_query_active**
> NumActiveUsers metrics_metrics_query_active(org_id, dt_from=dt_from, dt_to=dt_to, app_id=app_id, sub_org_id=sub_org_id, app_name=app_name, organisation=organisation, interval=interval)



View number of active users

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
    api_instance = agilicus_api.MetricsApi(api_client)
    org_id = '1234' # str | Organisation Unique identifier
dt_from = '' # str | Search criteria from when the query happened. * Inclusive. * In UTC. * Supports human-friendly values such as \"now\", \"today\", \"now-1day\".  (optional) (default to '')
dt_to = '' # str | Search criteria until when the query happened. * Exclusive. * In UTC. * Supports human-friendly values such as \"now\", \"today\", \"now-1day\".  (optional) (default to '')
app_id = 'app_id_example' # str | Application unique identifier (optional)
sub_org_id = '1234' # str | Sub Organisation Unique identifier (optional)
app_name = 'app_name_example' # str | Application Name (optional)
organisation = 'agilicus' # str | Organisation Name (optional)
interval = 60 # int | The size of the time intervals in seconds (optional) (default to 60)

    try:
        api_response = api_instance.metrics_metrics_query_active(org_id, dt_from=dt_from, dt_to=dt_to, app_id=app_id, sub_org_id=sub_org_id, app_name=app_name, organisation=organisation, interval=interval)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling MetricsApi->metrics_metrics_query_active: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **org_id** | **str**| Organisation Unique identifier | 
 **dt_from** | **str**| Search criteria from when the query happened. * Inclusive. * In UTC. * Supports human-friendly values such as \&quot;now\&quot;, \&quot;today\&quot;, \&quot;now-1day\&quot;.  | [optional] [default to &#39;&#39;]
 **dt_to** | **str**| Search criteria until when the query happened. * Exclusive. * In UTC. * Supports human-friendly values such as \&quot;now\&quot;, \&quot;today\&quot;, \&quot;now-1day\&quot;.  | [optional] [default to &#39;&#39;]
 **app_id** | **str**| Application unique identifier | [optional] 
 **sub_org_id** | **str**| Sub Organisation Unique identifier | [optional] 
 **app_name** | **str**| Application Name | [optional] 
 **organisation** | **str**| Organisation Name | [optional] 
 **interval** | **int**| The size of the time intervals in seconds | [optional] [default to 60]

### Return type

[**NumActiveUsers**](NumActiveUsers.md)

### Authorization

[token-valid](../README.md#token-valid)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | The query ran without error |  -  |
**400** | Query is invalid |  -  |
**403** | User does not have permissions to query |  -  |
**500** | Invalid database dialect |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **metrics_metrics_query_top**
> TopUsers metrics_metrics_query_top(org_id, dt_from=dt_from, dt_to=dt_to, app_id=app_id, sub_org_id=sub_org_id, app_name=app_name, organisation=organisation, interval=interval, limit=limit)

View top users

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
    api_instance = agilicus_api.MetricsApi(api_client)
    org_id = '1234' # str | Organisation Unique identifier
dt_from = '' # str | Search criteria from when the query happened. * Inclusive. * In UTC. * Supports human-friendly values such as \"now\", \"today\", \"now-1day\".  (optional) (default to '')
dt_to = '' # str | Search criteria until when the query happened. * Exclusive. * In UTC. * Supports human-friendly values such as \"now\", \"today\", \"now-1day\".  (optional) (default to '')
app_id = 'app_id_example' # str | Application unique identifier (optional)
sub_org_id = '1234' # str | Sub Organisation Unique identifier (optional)
app_name = 'app_name_example' # str | Application Name (optional)
organisation = 'agilicus' # str | Organisation Name (optional)
interval = 60 # int | The size of the time intervals in seconds (optional) (default to 60)
limit = 15 # int | limit the number of top users in the response (optional) (default to 15)

    try:
        # View top users
        api_response = api_instance.metrics_metrics_query_top(org_id, dt_from=dt_from, dt_to=dt_to, app_id=app_id, sub_org_id=sub_org_id, app_name=app_name, organisation=organisation, interval=interval, limit=limit)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling MetricsApi->metrics_metrics_query_top: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **org_id** | **str**| Organisation Unique identifier | 
 **dt_from** | **str**| Search criteria from when the query happened. * Inclusive. * In UTC. * Supports human-friendly values such as \&quot;now\&quot;, \&quot;today\&quot;, \&quot;now-1day\&quot;.  | [optional] [default to &#39;&#39;]
 **dt_to** | **str**| Search criteria until when the query happened. * Exclusive. * In UTC. * Supports human-friendly values such as \&quot;now\&quot;, \&quot;today\&quot;, \&quot;now-1day\&quot;.  | [optional] [default to &#39;&#39;]
 **app_id** | **str**| Application unique identifier | [optional] 
 **sub_org_id** | **str**| Sub Organisation Unique identifier | [optional] 
 **app_name** | **str**| Application Name | [optional] 
 **organisation** | **str**| Organisation Name | [optional] 
 **interval** | **int**| The size of the time intervals in seconds | [optional] [default to 60]
 **limit** | **int**| limit the number of top users in the response | [optional] [default to 15]

### Return type

[**TopUsers**](TopUsers.md)

### Authorization

[token-valid](../README.md#token-valid)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | The query ran without error |  -  |
**400** | Query is invalid |  -  |
**403** | User does not have permissions to query |  -  |
**500** | Invalid database dialect |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

