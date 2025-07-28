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
    schema_name = request.get_json().get("name")
    schema_data = request.get_json().get("schema")

    if not schema_name or not schema_data:
        return {"error": "Both 'name' and 'schema' fields are required."}, 400

    if schema_name in user_schemas:
        return {"error": f"Schema with name '{schema_name}' already exists."}, 400

    user_schemas[schema_name] = schema_data

    print(user_schemas)

    return jsonify({"message": f"Schema '{schema_name}' saved successfully!"}), 200
    #print("unreachable")


@Schema.get("/schemas")
def view_schema():
    global user_schemas
    schema_names = list(user_schemas.keys())
    print("success")

    return jsonify(schema_names)


@Schema.delete("/schema")
def delete_schema():
    schema_name = request.args.get("name")
    if not schema_name:
        return {"error": f"Schema '{schema_name}' not found."}, 404

    del user_schemas[schema_name]

    return jsonify({"message": "Schema deleted successfully!"})


@Schema.get("/schemas/schema")
def get_schema():
    global user_schemas

    schema_name = request.args.get("name")

    if schema_name not in user_schemas:
        return {"error": f"Schema '{schema_name}' not found."}, 404

    schema = user_schemas[schema_name]
    return jsonify(schema)


@Schema.get("/schemas/samples/")
def sampledata():
    global user_schemas

    return_type = request.headers.get('Accept', '')

    schema_name = request.args.get("name")
    count = request.args.get("count", type=int)

    if schema_name not in user_schemas:
        return {"error": f"Schema '{schema_name}' not found."}, 404
    schema = user_schemas[schema_name]

    if count <= 0:
        return {"error": "'count' must be a positive integer."}, 400

    json_data = display_documents(count, schema)

    if return_type == "application/x-ndjson":
        print(json.dumps(json_data, indent=2))
        ndjson = "\n".join([json.dumps(item) for item in json_data])
        return ndjson

    return json.dumps(json_data, indent=4)


def display_documents(count, schema):
    records = []

    for i in range(count):
        generator = generate_document(schema)
        records.append(generator)

    return records


def generate_document(schema):
    print(schema)
    sample_data = {}
    for field, field_name in schema.items():
        sample_data[field] = sample(field_name)
    json_data = json.dumps(sample_data)
    print(json_data)
    return sample_data


def main():
    variable_option = {
        'A': 'string',
        'B': 'integer',
        'C': 'float',
        'D': 'boolean',
        'E': 'date',
        'F': 'ip',
        'G': 'email',
        'H': 'country code',
    }
    while True:
        try:
            property_count = int(input("How many properties do you require?"))
            break
        except ValueError:
            print("Please enter a valid number")

    while True:
        try:
            record_count = int(input("How many records do you want to generate? "))
            break
        except ValueError:
            print("Please enter a valid number")

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
        user_schemas[property_name] = variable_option[letter]

        display_documents(record_count, user_schemas)


def sample(property_name):
    match property_name:
        case "string":
            return faker.first_name()
        case "integer":
            return 50
            #return random.randint(1, 100)
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
        case "job":
            return faker.job()
        case "country code":
            return faker.country_code()
        case "number":
            return faker.phone_number()
        case "email":
            return faker.email()

    return None


if __name__ == "__main__":
    Schema.run()
# main()
