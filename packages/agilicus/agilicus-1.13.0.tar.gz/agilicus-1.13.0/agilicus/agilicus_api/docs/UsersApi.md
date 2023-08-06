# agilicus_api.UsersApi

All URIs are relative to *https://api.agilicus.com*

Method | HTTP request | Description
------------- | ------------- | -------------
[**create_user**](UsersApi.md#create_user) | **POST** /users | Create a user
[**delete_user**](UsersApi.md#delete_user) | **DELETE** /v1/orgs/{org_id}/users/{user_id} | Remove a user from an organisation
[**get_user**](UsersApi.md#get_user) | **GET** /users/{user_id} | Get a single user
[**list_all_user_orgs**](UsersApi.md#list_all_user_orgs) | **GET** /users/{user_id}/orgs | Return all organisations a user has been assigned to
[**list_all_user_roles**](UsersApi.md#list_all_user_roles) | **GET** /users/{user_id}/render_roles | Return all roles for a user
[**list_user_guids**](UsersApi.md#list_user_guids) | **GET** /users_ids | Get a list of all user GUIDs
[**list_user_permissions**](UsersApi.md#list_user_permissions) | **GET** /users/{user_id}/host_permissions | Return the user&#39;s host permissions
[**list_users**](UsersApi.md#list_users) | **GET** /users | Get all users
[**replace_user**](UsersApi.md#replace_user) | **PUT** /users/{user_id} | Create or update a user
[**replace_user_role**](UsersApi.md#replace_user_role) | **PUT** /users/{user_id}/roles | Create or update a user role


# **create_user**
> User create_user(user)

Create a user

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
    api_instance = agilicus_api.UsersApi(api_client)
    user = agilicus_api.User() # User | 

    try:
        # Create a user
        api_response = api_instance.create_user(user)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling UsersApi->create_user: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **user** | [**User**](User.md)|  | 

### Return type

[**User**](User.md)

### Authorization

[token-valid](../README.md#token-valid)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**201** | New User created |  -  |
**409** | User already exists |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **delete_user**
> delete_user(org_id, user_id)

Remove a user from an organisation

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
    api_instance = agilicus_api.UsersApi(api_client)
    org_id = '1234' # str | Organisation Unique identifier
user_id = '1234' # str | user_id path

    try:
        # Remove a user from an organisation
        api_instance.delete_user(org_id, user_id)
    except ApiException as e:
        print("Exception when calling UsersApi->delete_user: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **org_id** | **str**| Organisation Unique identifier | 
 **user_id** | **str**| user_id path | 

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
**204** | User was removed from organisation |  -  |
**404** | User does not exist |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_user**
> User get_user(user_id, org_id=org_id)

Get a single user

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
    api_instance = agilicus_api.UsersApi(api_client)
    user_id = '1234' # str | user_id path
org_id = '1234' # str | Organisation Unique identifier (optional)

    try:
        # Get a single user
        api_response = api_instance.get_user(user_id, org_id=org_id)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling UsersApi->get_user: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **user_id** | **str**| user_id path | 
 **org_id** | **str**| Organisation Unique identifier | [optional] 

### Return type

[**User**](User.md)

### Authorization

[token-valid](../README.md#token-valid)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Return user |  -  |
**404** | User does not exist |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **list_all_user_orgs**
> ListOrgsResponse list_all_user_orgs(user_id, issuer=issuer)

Return all organisations a user has been assigned to

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
    api_instance = agilicus_api.UsersApi(api_client)
    user_id = '1234' # str | user_id path
issuer = 'example.com' # str | Organisation issuer (optional)

    try:
        # Return all organisations a user has been assigned to
        api_response = api_instance.list_all_user_orgs(user_id, issuer=issuer)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling UsersApi->list_all_user_orgs: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **user_id** | **str**| user_id path | 
 **issuer** | **str**| Organisation issuer | [optional] 

### Return type

[**ListOrgsResponse**](ListOrgsResponse.md)

### Authorization

[token-valid](../README.md#token-valid)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | roles |  -  |
**404** | User does not exist |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **list_all_user_roles**
> Roles list_all_user_roles(user_id, org_id=org_id)

Return all roles for a user

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
    api_instance = agilicus_api.UsersApi(api_client)
    user_id = '1234' # str | user_id path
org_id = '1234' # str | Organisation Unique identifier (optional)

    try:
        # Return all roles for a user
        api_response = api_instance.list_all_user_roles(user_id, org_id=org_id)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling UsersApi->list_all_user_roles: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **user_id** | **str**| user_id path | 
 **org_id** | **str**| Organisation Unique identifier | [optional] 

### Return type

[**Roles**](Roles.md)

### Authorization

[token-valid](../README.md#token-valid)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | roles |  -  |
**404** | User does not exist |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **list_user_guids**
> ListUserGuidsResponse list_user_guids(updated_since=updated_since)

Get a list of all user GUIDs

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
    api_instance = agilicus_api.UsersApi(api_client)
    updated_since = '2015-07-07T15:49:51.230+02:00' # datetime | query since updated (optional)

    try:
        # Get a list of all user GUIDs
        api_response = api_instance.list_user_guids(updated_since=updated_since)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling UsersApi->list_user_guids: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **updated_since** | **datetime**| query since updated | [optional] 

### Return type

[**ListUserGuidsResponse**](ListUserGuidsResponse.md)

### Authorization

[token-valid](../README.md#token-valid)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | A list of user GUIDs |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **list_user_permissions**
> HostPermissions list_user_permissions(user_id, org_id=org_id)

Return the user's host permissions

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
    api_instance = agilicus_api.UsersApi(api_client)
    user_id = '1234' # str | user_id path
org_id = '1234' # str | Organisation Unique identifier (optional)

    try:
        # Return the user's host permissions
        api_response = api_instance.list_user_permissions(user_id, org_id=org_id)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling UsersApi->list_user_permissions: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **user_id** | **str**| user_id path | 
 **org_id** | **str**| Organisation Unique identifier | [optional] 

### Return type

[**HostPermissions**](HostPermissions.md)

### Authorization

[token-valid](../README.md#token-valid)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | roles |  -  |
**404** | User does not exist |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **list_users**
> ListUsersResponse list_users(email=email, provider=provider, org_id=org_id, issuer=issuer, limit=limit, type=type)

Get all users

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
    api_instance = agilicus_api.UsersApi(api_client)
    email = 'foo@example.com' # str | Query based on user email (optional)
provider = 'google.com' # str | Query based on identity provider (optional)
org_id = '1234' # str | Organisation Unique identifier (optional)
issuer = 'example.com' # str | Organisation issuer (optional)
limit = 500 # int | limit the number of rows in the response (optional) (default to 500)
type = '1234' # str | user type (optional)

    try:
        # Get all users
        api_response = api_instance.list_users(email=email, provider=provider, org_id=org_id, issuer=issuer, limit=limit, type=type)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling UsersApi->list_users: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **email** | **str**| Query based on user email | [optional] 
 **provider** | **str**| Query based on identity provider | [optional] 
 **org_id** | **str**| Organisation Unique identifier | [optional] 
 **issuer** | **str**| Organisation issuer | [optional] 
 **limit** | **int**| limit the number of rows in the response | [optional] [default to 500]
 **type** | **str**| user type | [optional] 

### Return type

[**ListUsersResponse**](ListUsersResponse.md)

### Authorization

[token-valid](../README.md#token-valid)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Return users |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **replace_user**
> replace_user(user_id, user=user)

Create or update a user

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
    api_instance = agilicus_api.UsersApi(api_client)
    user_id = '1234' # str | user_id path
user = agilicus_api.User() # User |  (optional)

    try:
        # Create or update a user
        api_instance.replace_user(user_id, user=user)
    except ApiException as e:
        print("Exception when calling UsersApi->replace_user: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **user_id** | **str**| user_id path | 
 **user** | [**User**](User.md)|  | [optional] 

### Return type

void (empty response body)

### Authorization

[token-valid](../README.md#token-valid)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: Not defined

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**204** | User updated |  -  |
**404** | User does not exists |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **replace_user_role**
> replace_user_role(user_id, org_id=org_id, replace_user_role_request=replace_user_role_request)

Create or update a user role

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
    api_instance = agilicus_api.UsersApi(api_client)
    user_id = '1234' # str | user_id path
org_id = '1234' # str | Organisation Unique identifier (optional)
replace_user_role_request = agilicus_api.ReplaceUserRoleRequest() # ReplaceUserRoleRequest |  (optional)

    try:
        # Create or update a user role
        api_instance.replace_user_role(user_id, org_id=org_id, replace_user_role_request=replace_user_role_request)
    except ApiException as e:
        print("Exception when calling UsersApi->replace_user_role: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **user_id** | **str**| user_id path | 
 **org_id** | **str**| Organisation Unique identifier | [optional] 
 **replace_user_role_request** | [**ReplaceUserRoleRequest**](ReplaceUserRoleRequest.md)|  | [optional] 

### Return type

void (empty response body)

### Authorization

[token-valid](../README.md#token-valid)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: Not defined

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**204** | User role updated |  -  |
**404** | User does not exists |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

