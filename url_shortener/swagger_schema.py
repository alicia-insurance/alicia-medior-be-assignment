from drf_yasg.inspectors import SwaggerAutoSchema

class NoAuthSwaggerAutoSchema(SwaggerAutoSchema):
    def get_security(self):
        """No security for the endpoints"""
        return []

    def get_security_definitions(self):
        """No security definitions to show"""
        return {}