# Organisation

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **str** | Unique identifier | [optional] [readonly] 
**all_users_group_id** | **str** | group id of group containing this organisations all users | [optional] 
**all_users_all_suborgs_group_id** | **str** | group id of group containing this organisations all users including all sub organisations | [optional] 
**all_users_direct_suborgs_group_id** | **str** | group id of group containing this organisations all users including only direct sub organisations | [optional] 
**external_id** | **str** | External unique identifier | [optional] 
**organisation** | **str** | organisation name | [optional] 
**issuer** | **str** | connect id issuer | [optional] 
**issuer_id** | **str** | Unique identifier | [optional] 
**subdomain** | **str** | Organisations subdomain | [optional] 
**created** | **datetime** | Creation time | [optional] [readonly] 
**updated** | **datetime** | Update time | [optional] [readonly] 
**contact_id** | **str** | GUID of the organisation admin | [optional] 
**parent_id** | **str** | parent organisation id | [optional] 
**root_org_id** | **str** | The id of the organisation at the root of this organisation hierarchy. For example, if A is the parent of B, and B is the parent of C, then A would be the root organisation of A, B and C. Note that this field will be ignored if changed.  | [optional] 
**auto_create** | **bool** | Auto-creates a user | [optional] [default to True]

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


