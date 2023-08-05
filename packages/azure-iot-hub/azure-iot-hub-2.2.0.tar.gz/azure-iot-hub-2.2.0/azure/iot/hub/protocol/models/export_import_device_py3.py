# coding=utf-8
# --------------------------------------------------------------------------
# Code generated by Microsoft (R) AutoRest Code Generator.
# Changes may cause incorrect behavior and will be lost if the code is
# regenerated.
# --------------------------------------------------------------------------

from msrest.serialization import Model


class ExportImportDevice(Model):
    """ExportImportDevice.

    :param id: Device Id is always required
    :type id: str
    :param module_id: ModuleId is applicable to modules only
    :type module_id: str
    :param e_tag: ETag parameter is only used for pre-conditioning the update
     when importMode is updateIfMatchETag
    :type e_tag: str
    :param import_mode: Possible values include: 'create', 'update',
     'updateIfMatchETag', 'delete', 'deleteIfMatchETag', 'updateTwin',
     'updateTwinIfMatchETag'
    :type import_mode: str or ~protocol.models.enum
    :param status: Status is optional and defaults to enabled. Possible values
     include: 'enabled', 'disabled'
    :type status: str or ~protocol.models.enum
    :param status_reason:
    :type status_reason: str
    :param authentication: Authentication parameter is optional and defaults
     to SAS if not provided. In that case, we auto-generate primary/secondary
     access keys
    :type authentication: ~protocol.models.AuthenticationMechanism
    :param twin_etag: twinETag parameter is only used for pre-conditioning the
     update when importMode is updateTwinIfMatchETag
    :type twin_etag: str
    :param tags:
    :type tags: dict[str, object]
    :param properties: Properties are optional and defaults to empty object
    :type properties: ~protocol.models.PropertyContainer
    :param capabilities: Capabilities param is optional and defaults to no
     capability
    :type capabilities: ~protocol.models.DeviceCapabilities
    :param device_scope:
    :type device_scope: str
    """

    _attribute_map = {
        "id": {"key": "id", "type": "str"},
        "module_id": {"key": "moduleId", "type": "str"},
        "e_tag": {"key": "eTag", "type": "str"},
        "import_mode": {"key": "importMode", "type": "str"},
        "status": {"key": "status", "type": "str"},
        "status_reason": {"key": "statusReason", "type": "str"},
        "authentication": {"key": "authentication", "type": "AuthenticationMechanism"},
        "twin_etag": {"key": "twinETag", "type": "str"},
        "tags": {"key": "tags", "type": "{object}"},
        "properties": {"key": "properties", "type": "PropertyContainer"},
        "capabilities": {"key": "capabilities", "type": "DeviceCapabilities"},
        "device_scope": {"key": "deviceScope", "type": "str"},
    }

    def __init__(
        self,
        *,
        id: str = None,
        module_id: str = None,
        e_tag: str = None,
        import_mode=None,
        status=None,
        status_reason: str = None,
        authentication=None,
        twin_etag: str = None,
        tags=None,
        properties=None,
        capabilities=None,
        device_scope: str = None,
        **kwargs
    ) -> None:
        super(ExportImportDevice, self).__init__(**kwargs)
        self.id = id
        self.module_id = module_id
        self.e_tag = e_tag
        self.import_mode = import_mode
        self.status = status
        self.status_reason = status_reason
        self.authentication = authentication
        self.twin_etag = twin_etag
        self.tags = tags
        self.properties = properties
        self.capabilities = capabilities
        self.device_scope = device_scope
