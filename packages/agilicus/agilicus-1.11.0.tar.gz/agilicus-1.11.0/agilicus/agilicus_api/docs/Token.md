# Token

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**sub** | **str** | Unique identifier | [optional] [readonly] 
**org** | **str** | Unique identifier | [optional] [readonly] 
**root_org** | **str** | Unique identifier | [optional] [readonly] 
**roles** | [**Roles**](Roles.md) |  | [optional] 
**jti** | **str** | Unique identifier | [optional] [readonly] 
**iat** | **str** | token issue date | [optional] [readonly] 
**exp** | **str** | token expiry date | [optional] [readonly] 
**hosts** | [**list[HostPermissions]**](HostPermissions.md) | array of valid hosts | [optional] 
**aud** | **list[str]** | token audience | [optional] [readonly] 
**session** | **str** | Unique identifier | [optional] [readonly] 

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


