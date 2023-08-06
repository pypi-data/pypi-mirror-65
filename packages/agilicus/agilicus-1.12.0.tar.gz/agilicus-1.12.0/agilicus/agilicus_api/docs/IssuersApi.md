# agilicus_api.IssuersApi

All URIs are relative to *https://api.agilicus.com*

Method | HTTP request | Description
------------- | ------------- | -------------
[**create_client**](IssuersApi.md#create_client) | **POST** /v1/clients | Create a client
[**create_issuer**](IssuersApi.md#create_issuer) | **POST** /v1/issuers/issuer_roots | Create an issuer
[**delete_client**](IssuersApi.md#delete_client) | **DELETE** /v1/clients/{client_id} | Delete a client
[**delete_root**](IssuersApi.md#delete_root) | **DELETE** /v1/issuers/issuer_roots/{issuer_id} | Delete an Issuer
[**get_client**](IssuersApi.md#get_client) | **GET** /v1/clients/{client_id} | Get client
[**get_issuer**](IssuersApi.md#get_issuer) | **GET** /v1/issuers/issuer_extensions/{issuer_id} | Get issuer
[**get_root**](IssuersApi.md#get_root) | **GET** /v1/issuers/issuer_roots/{issuer_id} | Get issuer
[**list_clients**](IssuersApi.md#list_clients) | **GET** /v1/clients | Query Clients
[**list_issuer_roots**](IssuersApi.md#list_issuer_roots) | **GET** /v1/issuers/issuer_roots | Query Issuers
[**list_issuers**](IssuersApi.md#list_issuers) | **GET** /v1/issuers/issuer_extensions | Query Issuers
[**replace_client**](IssuersApi.md#replace_client) | **PUT** /v1/clients/{client_id} | Update a client
[**replace_issuer**](IssuersApi.md#replace_issuer) | **PUT** /v1/issuers/issuer_extensions/{issuer_id} | Update an issuer
[**replace_root**](IssuersApi.md#replace_root) | **PUT** /v1/issuers/issuer_roots/{issuer_id} | Update an issuer


# **create_client**
> IssuerClient create_client(issuer_client)

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
        api_response = api_instance.create_client(issuer_client)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling IssuersApi->create_client: %s\n" % e)
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

# **create_issuer**
> Issuer create_issuer(issuer)

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
        api_response = api_instance.create_issuer(issuer)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling IssuersApi->create_issuer: %s\n" % e)
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

# **delete_client**
> delete_client(client_id, org_id=org_id)

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
        api_instance.delete_client(client_id, org_id=org_id)
    except ApiException as e:
        print("Exception when calling IssuersApi->delete_client: %s\n" % e)
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

# **delete_root**
> delete_root(issuer_id)

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
        api_instance.delete_root(issuer_id)
    except ApiException as e:
        print("Exception when calling IssuersApi->delete_root: %s\n" % e)
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

# **get_client**
> IssuerClient get_client(client_id, org_id=org_id)

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
        api_response = api_instance.get_client(client_id, org_id=org_id)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling IssuersApi->get_client: %s\n" % e)
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

# **get_issuer**
> Issuer get_issuer(issuer_id, org_id=org_id)

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
        api_response = api_instance.get_issuer(issuer_id, org_id=org_id)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling IssuersApi->get_issuer: %s\n" % e)
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

# **get_root**
> Issuer get_root(issuer_id)

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
        api_response = api_instance.get_root(issuer_id)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling IssuersApi->get_root: %s\n" % e)
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

# **list_clients**
> ListIssuerClientsResponse list_clients(limit=limit, org_id=org_id)

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
        api_response = api_instance.list_clients(limit=limit, org_id=org_id)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling IssuersApi->list_clients: %s\n" % e)
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

# **list_issuer_roots**
> ListIssuerRootsResponse list_issuer_roots(limit=limit, issuer=issuer)

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
        api_response = api_instance.list_issuer_roots(limit=limit, issuer=issuer)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling IssuersApi->list_issuer_roots: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **limit** | **int**| limit the number of rows in the response | [optional] [default to 500]
 **issuer** | **str**| Organisation issuer | [optional] 

### Return type

[**ListIssuerRootsResponse**](ListIssuerRootsResponse.md)

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

# **list_issuers**
> ListIssuerExtensionsResponse list_issuers(limit=limit, issuer=issuer, org_id=org_id)

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
        api_response = api_instance.list_issuers(limit=limit, issuer=issuer, org_id=org_id)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling IssuersApi->list_issuers: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **limit** | **int**| limit the number of rows in the response | [optional] [default to 500]
 **issuer** | **str**| Organisation issuer | [optional] 
 **org_id** | **str**| Organisation Unique identifier | [optional] 

### Return type

[**ListIssuerExtensionsResponse**](ListIssuerExtensionsResponse.md)

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

# **replace_client**
> IssuerClient replace_client(client_id, issuer_client)

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
        api_response = api_instance.replace_client(client_id, issuer_client)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling IssuersApi->replace_client: %s\n" % e)
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

# **replace_issuer**
> Issuer replace_issuer(issuer_id, issuer)

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
        api_response = api_instance.replace_issuer(issuer_id, issuer)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling IssuersApi->replace_issuer: %s\n" % e)
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

# **replace_root**
> Issuer replace_root(issuer_id, issuer)

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
        api_response = api_instance.replace_root(issuer_id, issuer)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling IssuersApi->replace_root: %s\n" % e)
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

