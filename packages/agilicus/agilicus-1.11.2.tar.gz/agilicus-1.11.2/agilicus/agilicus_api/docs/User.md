# User

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**member_of** | [**list[UserIdentity]**](UserIdentity.md) |  | [optional] 
**id** | **str** | Unique identifier | [optional] [readonly] 
**external_id** | **str** | External unique identifier | [optional] 
**enabled** | **bool** | Enable/Disable a user | [optional] 
**first_name** | **str** | User&#39;s first name | [optional] 
**last_name** | **str** | User&#39;s last name | [optional] 
**email** | **str** | User&#39;s email-addr | [optional] 
**provider** | **str** | Upstream IdP name | [optional] 
**roles** | **dict(str, list[str])** |  | [optional] 
**org_id** | **str** | Unique identifier | [optional] 
**type** | **str** |  | [optional] [readonly] 
**created** | **datetime** | Creation time | [optional] [readonly] 
**updated** | **datetime** | Update time | [optional] [readonly] 

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


