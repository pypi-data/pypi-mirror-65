# coding=utf-8
# --------------------------------------------------------------------------
# Code generated by Microsoft (R) AutoRest Code Generator.
# Changes may cause incorrect behavior and will be lost if the code is
# regenerated.
# --------------------------------------------------------------------------

from msrest.serialization import Model


class Desired(Model):
    """Desired.

    :param value: The desired value of the interface property to set in a
     digitalTwin.
    :type value: object
    """

    _attribute_map = {"value": {"key": "value", "type": "object"}}

    def __init__(self, *, value=None, **kwargs) -> None:
        super(Desired, self).__init__(**kwargs)
        self.value = value
