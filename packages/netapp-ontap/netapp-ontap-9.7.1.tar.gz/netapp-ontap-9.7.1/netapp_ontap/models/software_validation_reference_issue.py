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


__all__ = ["SoftwareValidationReferenceIssue", "SoftwareValidationReferenceIssueSchema"]
__pdoc__ = {
    "SoftwareValidationReferenceIssueSchema.resource": False,
    "SoftwareValidationReferenceIssue": False,
}


class SoftwareValidationReferenceIssueSchema(ResourceSchema):
    """The fields of the SoftwareValidationReferenceIssue object"""

    message = fields.Str(data_key="message")
    r""" Details of the error or warning encountered by the update checks

Example: Validation error: Cluster HA is not configured in the cluster """

    @property
    def resource(self):
        return SoftwareValidationReferenceIssue

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


class SoftwareValidationReferenceIssue(Resource):  # pylint: disable=missing-docstring

    _schema = SoftwareValidationReferenceIssueSchema
