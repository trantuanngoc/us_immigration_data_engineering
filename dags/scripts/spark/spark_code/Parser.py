from pyspark.sql.types import StructType, StructField, StringType, IntegerType, BooleanType, FloatType

class SchemaParser:
    type_mapping = {
        "string": StringType(),
        "integer": IntegerType(),
        "boolean": BooleanType(),
        "float": FloatType(),
    }

    def __init__(self, schema_json):
        self.schema_json = schema_json

    def parse_field(self, field):
        field_name = field['name']
        field_type = field['type'].lower()

        if field_type not in self.type_mapping:
            raise ValueError(f"Unsupported field type: {field_type}")

        return StructField(field_name, self.type_mapping[field_type], field['nullable'])

    def parse_schema(self):
        fields = [self.parse_field(field) for field in self.schema_json['fields']]
        return StructType(fields)