# agilicus_api.IssuersApi

All URIs are relative to *https://api.agilicus.com*

Method | HTTP request | Description
------------- | ------------- | -------------
[**clients_delete**](IssuersApi.md#clients_delete) | **DELETE** /v1/clients/{client_id} | Delete a client
[**clients_get**](IssuersApi.md#clients_get) | **GET** /v1/clients/{client_id} | Get client
[**clients_post**](IssuersApi.md#clients_post) | **POST** /v1/clients | Create a client
[**clients_put**](IssuersApi.md#clients_put) | **PUT** /v1/clients/{client_id} | Update a client
[**clients_query**](IssuersApi.md#clients_query) | **GET** /v1/clients | Query Clients
[**issuers_get**](IssuersApi.md#issuers_get) | **GET** /v1/issuers/extensions/{issuer_id} | Get issuer
[**issuers_put**](IssuersApi.md#issuers_put) | **PUT** /v1/issuers/extensions/{issuer_id} | Update an issuer
[**issuers_query**](IssuersApi.md#issuers_query) | **GET** /v1/issuers/extensions | Query Issuers
[**issuers_root_delete**](IssuersApi.md#issuers_root_delete) | **DELETE** /v1/issuers/root/{issuer_id} | Delete an Issuer
[**issuers_root_get**](IssuersApi.md#issuers_root_get) | **GET** /v1/issuers/root/{issuer_id} | Get issuer
[**issuers_root_post**](IssuersApi.md#issuers_root_post) | **POST** /v1/issuers/root | Create an issuer
[**issuers_root_put**](IssuersApi.md#issuers_root_put) | **PUT** /v1/issuers/root/{issuer_id} | Update an issuer
[**issuers_root_query**](IssuersApi.md#issuers_root_query) | **GET** /v1/issuers/root | Query Issuers


# **clients_delete**
> clients_delete(client_id, org_id=org_id)

Delete a client

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
    api_instance = agilicus_api.IssuersApi(api_client)
    client_id = '1234' # str | client_id path
org_id = '1234' # str | Organisation Unique identifier (optional)

    try:
        # Delete a client
        api_instance.clients_delete(client_id, org_id=org_id)
    except ApiException as e:
        print("Exception when calling IssuersApi->clients_delete: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **client_id** | **str**| client_id path | 
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
**204** | Client was deleted |  -  |
**404** | Issuer/Client does not exist |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **clients_get**
> IssuerClient clients_get(client_id, org_id=org_id)

Get client

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
    api_instance = agilicus_api.IssuersApi(api_client)
    client_id = '1234' # str | client_id path
org_id = '1234' # str | Organisation Unique identifier (optional)

    try:
        # Get client
        api_response = api_instance.clients_get(client_id, org_id=org_id)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling IssuersApi->clients_get: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **client_id** | **str**| client_id path | 
 **org_id** | **str**| Organisation Unique identifier | [optional] 

### Return type

[**IssuerClient**](IssuerClient.md)

### Authorization

[token-valid](../README.md#token-valid)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Return client by id |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **clients_post**
> IssuerClient clients_post(issuer_client)

Create a client

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
    api_instance = agilicus_api.IssuersApi(api_client)
    issuer_client = agilicus_api.IssuerClient() # IssuerClient | IssuerClient

    try:
        # Create a client
        api_response = api_instance.clients_post(issuer_client)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling IssuersApi->clients_post: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **issuer_client** | [**IssuerClient**](IssuerClient.md)| IssuerClient | 

### Return type

[**IssuerClient**](IssuerClient.md)

### Authorization

[token-valid](../README.md#token-valid)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**201** | Successfully created client |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **clients_put**
> IssuerClient clients_put(client_id, issuer_client)

Update a client

Update a client

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
    api_instance = agilicus_api.IssuersApi(api_client)
    client_id = '1234' # str | client_id path
issuer_client = agilicus_api.IssuerClient() # IssuerClient | Issuer client

    try:
        # Update a client
        api_response = api_instance.clients_put(client_id, issuer_client)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling IssuersApi->clients_put: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **client_id** | **str**| client_id path | 
 **issuer_client** | [**IssuerClient**](IssuerClient.md)| Issuer client | 

### Return type

[**IssuerClient**](IssuerClient.md)

### Authorization

[token-valid](../README.md#token-valid)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Client was updated |  -  |
**404** | Issuer/Client does not exist |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **clients_query**
> ListIssuerClientsResponse clients_query(limit=limit, org_id=org_id)

Query Clients

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
    api_instance = agilicus_api.IssuersApi(api_client)
    limit = 500 # int | limit the number of rows in the response (optional) (default to 500)
org_id = '1234' # str | Organisation Unique identifier (optional)

    try:
        # Query Clients
        api_response = api_instance.clients_query(limit=limit, org_id=org_id)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling IssuersApi->clients_query: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **limit** | **int**| limit the number of rows in the response | [optional] [default to 500]
 **org_id** | **str**| Organisation Unique identifier | [optional] 

### Return type

[**ListIssuerClientsResponse**](ListIssuerClientsResponse.md)

### Authorization

[token-valid](../README.md#token-valid)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Return clients list |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **issuers_get**
> Issuer issuers_get(issuer_id, org_id=org_id)

Get issuer

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
    api_instance = agilicus_api.IssuersApi(api_client)
    issuer_id = '1234' # str | issuer_id path
org_id = '1234' # str | Organisation Unique identifier (optional)

    try:
        # Get issuer
        api_response = api_instance.issuers_get(issuer_id, org_id=org_id)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling IssuersApi->issuers_get: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **issuer_id** | **str**| issuer_id path | 
 **org_id** | **str**| Organisation Unique identifier | [optional] 

### Return type

[**Issuer**](Issuer.md)

### Authorization

[token-valid](../README.md#token-valid)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Return issuer by id |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **issuers_put**
> Issuer issuers_put(issuer_id, issuer)

Update an issuer

Update an issuer

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
    api_instance = agilicus_api.IssuersApi(api_client)
    issuer_id = '1234' # str | issuer_id path
issuer = agilicus_api.Issuer() # Issuer | Issuer

    try:
        # Update an issuer
        api_response = api_instance.issuers_put(issuer_id, issuer)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling IssuersApi->issuers_put: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **issuer_id** | **str**| issuer_id path | 
 **issuer** | [**Issuer**](Issuer.md)| Issuer | 

### Return type

[**Issuer**](Issuer.md)

### Authorization

[token-valid](../README.md#token-valid)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Issuer was updated |  -  |
**404** | Issuer does not exist |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **issuers_query**
> ListIssuersRootResponse issuers_query(limit=limit, issuer=issuer, org_id=org_id)

Query Issuers

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
    api_instance = agilicus_api.IssuersApi(api_client)
    limit = 500 # int | limit the number of rows in the response (optional) (default to 500)
issuer = 'example.com' # str | Organisation issuer (optional)
org_id = '1234' # str | Organisation Unique identifier (optional)

    try:
        # Query Issuers
        api_response = api_instance.issuers_query(limit=limit, issuer=issuer, org_id=org_id)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling IssuersApi->issuers_query: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **limit** | **int**| limit the number of rows in the response | [optional] [default to 500]
 **issuer** | **str**| Organisation issuer | [optional] 
 **org_id** | **str**| Organisation Unique identifier | [optional] 

### Return type

[**ListIssuersRootResponse**](ListIssuersRootResponse.md)

### Authorization

[token-valid](../README.md#token-valid)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Return issuers list |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **issuers_root_delete**
> issuers_root_delete(issuer_id)

Delete an Issuer

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
    api_instance = agilicus_api.IssuersApi(api_client)
    issuer_id = '1234' # str | issuer_id path

    try:
        # Delete an Issuer
        api_instance.issuers_root_delete(issuer_id)
    except ApiException as e:
        print("Exception when calling IssuersApi->issuers_root_delete: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **issuer_id** | **str**| issuer_id path | 

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
**204** | Issuer was deleted |  -  |
**404** | Issuer does not exist |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **issuers_root_get**
> Issuer issuers_root_get(issuer_id)

Get issuer

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
    api_instance = agilicus_api.IssuersApi(api_client)
    issuer_id = '1234' # str | issuer_id path

    try:
        # Get issuer
        api_response = api_instance.issuers_root_get(issuer_id)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling IssuersApi->issuers_root_get: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **issuer_id** | **str**| issuer_id path | 

### Return type

[**Issuer**](Issuer.md)

### Authorization

[token-valid](../README.md#token-valid)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Return issuer by id |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **issuers_root_post**
> Issuer issuers_root_post(issuer)

Create an issuer

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
    api_instance = agilicus_api.IssuersApi(api_client)
    issuer = agilicus_api.Issuer() # Issuer | Issuer

    try:
        # Create an issuer
        api_response = api_instance.issuers_root_post(issuer)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling IssuersApi->issuers_root_post: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **issuer** | [**Issuer**](Issuer.md)| Issuer | 

### Return type

[**Issuer**](Issuer.md)

### Authorization

[token-valid](../README.md#token-valid)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**201** | Successfully created issuer |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **issuers_root_put**
> Issuer issuers_root_put(issuer_id, issuer)

Update an issuer

Update an issuer

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
    api_instance = agilicus_api.IssuersApi(api_client)
    issuer_id = '1234' # str | issuer_id path
issuer = agilicus_api.Issuer() # Issuer | Issuer

    try:
        # Update an issuer
        api_response = api_instance.issuers_root_put(issuer_id, issuer)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling IssuersApi->issuers_root_put: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **issuer_id** | **str**| issuer_id path | 
 **issuer** | [**Issuer**](Issuer.md)| Issuer | 

### Return type

[**Issuer**](Issuer.md)

### Authorization

[token-valid](../README.md#token-valid)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Issuer was updated |  -  |
**404** | Issuer does not exist |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **issuers_root_query**
> ListIssuersRootResponse issuers_root_query(limit=limit, issuer=issuer)

Query Issuers

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
    api_instance = agilicus_api.IssuersApi(api_client)
    limit = 500 # int | limit the number of rows in the response (optional) (default to 500)
issuer = 'example.com' # str | Organisation issuer (optional)

    try:
        # Query Issuers
        api_response = api_instance.issuers_root_query(limit=limit, issuer=issuer)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling IssuersApi->issuers_root_query: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **limit** | **int**| limit the number of rows in the response | [optional] [default to 500]
 **issuer** | **str**| Organisation issuer | [optional] 

### Return type

[**ListIssuersRootResponse**](ListIssuersRootResponse.md)

### Authorization

[token-valid](../README.md#token-valid)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Return issuers list |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

