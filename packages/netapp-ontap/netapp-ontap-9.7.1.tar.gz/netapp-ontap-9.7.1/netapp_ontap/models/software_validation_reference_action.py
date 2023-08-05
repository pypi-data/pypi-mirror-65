# pylint: disable=trailing-newlines
# pylint: disable=line-too-long
# pylint: disable=too-many-lines
# pylint: disable=unused-import
# pylint: disable=invalid-name

r"""
Copyright &copy; 2020 NetApp Inc.
All rights reserved.


"""

from marshmallow import EXCLUDE, fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema


__all__ = ["SoftwareValidationReferenceAction", "SoftwareValidationReferenceActionSchema"]
__pdoc__ = {
    "SoftwareValidationReferenceActionSchema.resource": False,
    "SoftwareValidationReferenceAction": False,
}


class SoftwareValidationReferenceActionSchema(ResourceSchema):
    """The fields of the SoftwareValidationReferenceAction object"""

    message = fields.Str(data_key="message")
    r""" Specifies the corrective action to be taken to resolve a validation error """

    @property
    def resource(self):
        return SoftwareValidationReferenceAction

    @property
    def patchable_fields(self):
        return [
            "message",
        ]

    @property
    def postable_fields(self):
        return [
            "message",
        ]


class SoftwareValidationReferenceAction(Resource):  # pylint: disable=missing-docstring

    _schema = SoftwareValidationReferenceActionSchema
