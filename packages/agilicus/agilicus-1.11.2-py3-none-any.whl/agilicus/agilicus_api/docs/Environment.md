# Environment

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**name** | **str** | Environment name | 
**maintenance_org_id** | **str** | The Organisation which is responsibile for maintaining this Environment. Often this will be the same Organisation as the owning Application. However, sometimes it makes sense to delegate this responsibility to another Organisation. To do so, set this field to that Organisation&#39;s identifier. Users with sufficient permissions in that organisation will be able to modify this Environment. If the maintenance_org_id is not provided, it will populaed with that of the parent application&#39;s organisation.  | [optional] 
**version_tag** | **str** | version tag | 
**config_mount_path** | **str** | config_as_mount file path | [optional] 
**config_as_mount** | **str** | A json object of config applied as file mounted | [optional] 
**config_as_env** | **str** | A json object of config applied as environment | [optional] 
**secrets_mount_path** | **str** | secret_as_mount file path | [optional] 
**secrets_as_mount** | **str** | A json object of secrets applied as file mounted | [optional] 
**secrets_as_env** | **str** | A json object of secrets applied as environment | [optional] 
**application_services** | [**list[ApplicationService]**](ApplicationService.md) | The services used by the application for this environment. Note that in order to add a service to the environment, this environment must be added to the list of assignments for that service in the ApplicationService collection for the organisation.  | [optional] [readonly] 
**serverless_image** | **str** | serverless image path | [optional] 

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


