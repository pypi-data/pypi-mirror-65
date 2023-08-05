# TokenRequest

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**sub** | **str** | Unique identifier | 
**org** | **str** | Unique identifier | 
**roles** | **dict(str, str)** |  | [optional] 
**audiences** | **list[str]** |  | 
**time_validity** | [**TimeValidity**](TimeValidity.md) |  | 
**hosts** | [**list[HostPermissions]**](HostPermissions.md) | array of valid hosts | [optional] 
**token_validity** | [**TokenValidity**](TokenValidity.md) |  | [optional] 
**session** | **str** | Unique identifier | [optional] 

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


