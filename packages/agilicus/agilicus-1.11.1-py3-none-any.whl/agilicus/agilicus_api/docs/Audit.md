# Audit

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**user_id** | **str** | The id of the user performing the action | [optional] [readonly] 
**org_id** | **str** | The organization of the user performing the action | [optional] [readonly] 
**time** | **datetime** | the time at which the log was generated | [optional] [readonly] 
**action** | **str** | The type of action performed on the target | [optional] 
**source_ip** | **str** | The IP address of the host initating the action | [optional] [readonly] 
**target_id** | **str** | The id of the resource affected by the action | [optional] [readonly] 
**token_id** | **str** | The id of the bearer token used to authenticate when performing the action | [optional] [readonly] 
**trace_id** | **str** | A correlation ID associated with requests related to this action | [optional] [readonly] 

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


