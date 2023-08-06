import copy

from dos import prop


class Fields:

    def __init__(self, base_schema):
        self.base_schema = base_schema

    def all(self):
        return self.specialize()

    def specialize(self, overrides=None, only=None, exclude=None):

        cloned = copy.deepcopy(self.base_schema)

        if overrides:
            for override_name, override_values in overrides.items():

                overridden_prop = cloned[override_name]

                for override_attr, override_value in override_values.items():
                    setattr(overridden_prop, override_attr, override_value)

        if only:

            trimmed = {}

            for field_name in only:
                trimmed[field_name] = cloned[field_name]

            cloned = trimmed

        if exclude:
            for name in exclude:
                if name in cloned:
                    del cloned[name]

        return cloned


class SuccessFields(Fields):
    base_schema = {
        "message": prop.String("The success message.")
    }

    def __init__(self):
        super().__init__(self.base_schema)


class ErrorFields(Fields):
    base_schema = {
        "message": prop.String("The error message.", required=True, nullable=False)
    }

    def __init__(self, validated_fields=None):
        if validated_fields is not None:
            fields = {}

            for field in validated_fields:
                fields[field] = prop.String(f"A error message specific to the {field} field.")

            self.base_schema["field_error_messages"] = prop.Object(structure=fields, required=False, nullable=True)

        super().__init__(self.base_schema)
