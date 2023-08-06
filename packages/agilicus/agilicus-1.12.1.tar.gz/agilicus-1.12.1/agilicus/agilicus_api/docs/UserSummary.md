# UserSummary

A per-organisation view of a user. This will contain properties associated with a user that are specific to the organisation with which they are interacting. Note that many of the properties are inherited from the UserIdentity of the user. These may not be modified. 
## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **str** | Unique identifier | [optional] [readonly] 
**external_id** | **str** | External unique identifier | [optional] 
**enabled** | **bool** | Enable/Disable a user | [optional] 
**first_name** | **str** | User&#39;s first name | [optional] 
**last_name** | **str** | User&#39;s last name | [optional] 
**email** | **str** | User&#39;s email-addr | [optional] 
**provider** | **str** | Upstream IdP name | [optional] 
**roles** | [**Roles**](Roles.md) |  | [optional] 
**org_id** | **str** | Unique identifier | [optional] 
**type** | **str** | Type of user | [optional] [readonly] 
**created** | **datetime** | Creation time | [optional] [readonly] 
**updated** | **datetime** | Update time | [optional] [readonly] 

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


