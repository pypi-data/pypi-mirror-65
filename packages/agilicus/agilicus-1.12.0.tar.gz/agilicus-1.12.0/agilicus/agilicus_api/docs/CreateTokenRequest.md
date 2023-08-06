# CreateTokenRequest

Request object to create a token
## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**sub** | **str** | Unique identifier | 
**org** | **str** | Unique identifier | 
**roles** | **dict(str, str)** | associative mapping of an application to a role | [optional] 
**audiences** | **list[str]** | array of audiences | 
**time_validity** | [**TimeValidity**](TimeValidity.md) |  | 
**hosts** | [**list[HostPermissions]**](HostPermissions.md) | array of valid hosts | [optional] 
**token_validity** | [**TokenValidity**](TokenValidity.md) |  | [optional] 
**session** | **str** | Unique identifier | [optional] 

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


