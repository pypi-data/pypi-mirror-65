# coding=utf-8
# --------------------------------------------------------------------------
# Code generated by Microsoft (R) AutoRest Code Generator.
# Changes may cause incorrect behavior and will be lost if the code is
# regenerated.
# --------------------------------------------------------------------------

from msrest.serialization import Model


class DigitalTwinInterfacesPatch(Model):
    """DigitalTwinInterfacesPatch.

    :param interfaces: Interface(s) data to patch in the digital twin.
    :type interfaces: dict[str,
     ~protocol.models.DigitalTwinInterfacesPatchInterfacesValue]
    """

    _attribute_map = {
        "interfaces": {"key": "interfaces", "type": "{DigitalTwinInterfacesPatchInterfacesValue}"}
    }

    def __init__(self, **kwargs):
        super(DigitalTwinInterfacesPatch, self).__init__(**kwargs)
        self.interfaces = kwargs.get("interfaces", None)
