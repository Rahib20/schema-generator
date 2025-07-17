import random
from datetime import datetime, timedelta
from urllib import request

from faker import Faker
import json
from flask import Flask, request, jsonify

faker = Faker()
Schema = Flask(__name__)

user_schemas = {}


@Schema.post("/schema")
def create_schema():
    schema_name = request.get_json().get("name")  # added
    schema_data = request.get_json().get("schema")  # modified

    if not schema_name or not schema_data:
        return {"error": "Both 'name' and 'schema' fields are required."}, 400  # Improved validation

    if schema_name in user_schemas:
        return {"error": f"Schema with name '{schema_name}' already exists."}, 400  # Prevent overwriting

    # Store the new schema in the global storage dictionary
    user_schemas[schema_name] = schema_data  # Save schema under its name

    print(user_schemas)

    return jsonify({"message": f"Schema '{schema_name}' saved successfully!"}), 200  # Success response


@Schema.get("/schemas")
def view_schema():
    global user_schemas
    schema_names = list(user_schemas.keys())

    return jsonify(schema_names)


@Schema.get("/schemas/<string:schema_name>")
def get_schema(schema_name):
    global user_schemas

    # Check if schema exists
    if schema_name not in user_schemas:
        return {"error": f"Schema '{schema_name}' not found."}, 404

    schema = user_schemas[schema_name]  # Get the schema
    return jsonify(schema)


@Schema.get("/schemas/<string:schema_name>/samples/<int:count>")
def sampledata(schema_name, count):
    global user_schemas
    json_data = []

    schema = user_schemas[schema_name]

    # Check if the specified schema exists
    if schema_name not in user_schemas:
        return {"error": f"Schema '{schema_name}' not found."}, 404

    if count <= 0:
        return {"error": "'count' must be a positive integer."}, 400

    for i in range(count):
        sample_data = {}
        for field, field_name in schema.items():
            sample_data[field] = sample(field_name)
        json_data.append(sample_data)

    print(json.dumps(json_data, indent=2))

    return jsonify(json_data)


def main():
    variable_option = {
        'A': 'string',
        'B': 'integer',
        'C': 'float',
        'D': 'boolean',
        'E': 'date',
        'F': 'ip',
    }
    while True:
        try:
            property_count = int(input("How many properties do you require? "))
            break
        except ValueError:
            print("Please enter a valid number.")

    while True:
        try:
            record_count = int(input("How many records do you want to generate? "))
            break
        except ValueError:
            print("Please enter a valid number.")

    schema = {}

    for i in range(property_count):
        print()
        print("Field:" + str(i + 1))
        for k, v in variable_option.items():
            print(f"{k}: {v}")

        while True:
            letter = input("Select type letter: ").strip().upper()
            if letter in variable_option:
                break
            print("Invalid letter. Try again.")
        property_name = input("Enter field name: ").strip()
        schema[property_name] = variable_option[letter]

    for i in range(record_count):
        sample_data = {}
        for field, field_name in schema.items():
            sample_data[field] = sample(field_name)
        json_data = json.dumps(sample_data)
        print(json_data)


def sample(property_name):
    match property_name:
        case "string":
            return faker.first_name()
        case "integer":
            return random.randint(1, 100)
        case "float":
            return round(random.uniform(0, 100), 2)
        case "boolean":
            return random.choice([True, False])
        case "date":
            from_date = datetime.now() - timedelta(days=365 * 50)
            random_day = random.randint(0, 365 * 50)
            random_date = from_date + timedelta(days=random_day)
            return random_date.strftime("%d/%m/%Y")
        case "ip":
            return faker.ipv4()
    return None


if __name__ == "__main__":
    Schema.run()
    # main()
