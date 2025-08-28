import random
from datetime import datetime, timedelta
from urllib import request
import os
from faker import Faker
import json
from flask import Flask, request, jsonify

faker = Faker()
Schema = Flask(__name__)

data = "/schema-generator/data/data.json"

suffix = [" FC", " United", " City"]
clubs = [faker.city() + random.choice(suffix) for _ in range(1000)]


def load_data():
    if not os.path.exists(data) or os.path.getsize(data) == 0:
        return {}
    with open(data, "r") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:

            return {}


@Schema.post("/schema")
def create_schema():
    schema_name = request.get_json().get("name")
    schema_data = request.get_json().get("schema")

    if not schema_name or not schema_data:
        return {"error": "Both 'name' and 'schema' fields are required."}, 400

    user_schemas = load_data()

    if schema_name in user_schemas:
        return {"error": f"Schema with name '{schema_name}' already exists."}, 400

    user_schemas[schema_name] = schema_data

    with open(data, "w") as f:
        json.dump(user_schemas, f, indent=2)

    return jsonify({"message": f"Schema '{schema_name}' saved successfully!"}), 200


@Schema.get("/schemas")
def view_schema():
    user_schemas = load_data()

    schema_names = list(user_schemas.keys())

    return jsonify(schema_names)


@Schema.delete("/schema")
def delete_schema():
    schema_name = request.args.get("name")
    if not schema_name:
        return {"error": f"Schema '{schema_name}' not found."}, 404

    user_schemas = load_data()

    if schema_name not in user_schemas:
        return {"error": f"Schema '{schema_name}' not found."}, 404

    del user_schemas[schema_name]
    with open(data, "w") as f:
        json.dump(user_schemas, f, indent=2)

    return jsonify({"message": "Schema deleted successfully!"})


@Schema.get("/schemas/schema")
def get_schema():
    schema_name = request.args.get("name")

    user_schemas = load_data()

    if schema_name not in user_schemas:
        return {"error": f"Schema '{schema_name}' not found."}, 404

    schema = user_schemas[schema_name]
    return jsonify(schema)


@Schema.get("/schemas/samples/")
def sampledata():
    print("testing if this shows in logs")
    return_type = request.headers.get('Accept', '')

    schema_name = request.args.get("name")
    count = request.args.get("count", type=int)

    user_schemas = load_data()

    if schema_name not in user_schemas:
        return {"error": f"Schema '{schema_name}' not found."}, 404
    schema = user_schemas[schema_name]

    if count <= 0:
        return {"error": "'count' must be a positive integer."}, 400

    json_data = display_documents(count, schema)

    if return_type == "application/x-ndjson":
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
    sample_data = {}

    for field, field_name in schema.items():

        field = field.lower()

        if field not in ("email", "fullname", "skill rating", "goals", "assists", "market_value"):
            sample_data[field] = sample(field, field_name)

    for field, field_name in schema.items():
        if field_name == "email":
            sample_data[field] = realistic_email(sample_data)

    for field, field_name in schema.items():
        field = field.lower()
        if field == "fullname":
            sample_data[field] = get_fullname(sample_data)

    for field, field_name in schema.items():
        field = field.lower()
        if field == "goals":
            sample_data[field] = generate_goals(sample_data.get("age"))

    for field, field_name in schema.items():
        field = field.lower()
        if field == "assists":
            sample_data[field] = generate_assists(sample_data.get("age"))

    for field, field_name in schema.items():
        field = field.lower()
        if field == "skill rating":
            skill = sample_data.get("goals") + sample_data.get("assists")
            sample_data[field] = skill

    for field, field_name in schema.items():
        field = field.lower()
        if field == "market_value":
            sample_data[field] = generate_market_value(sample_data.get("goals"), sample_data.get("assists"),
                                                       sample_data.get("nationality"))

    json_data = json.dumps(sample_data)

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
    user_schemas = load_data()
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


def sample(field, property_name):
    match property_name:
        case "string":
            return generate_string(field)
        case {"type": "integer", "min": minv, "max": maxv}:
            return random.randint(minv, maxv)
        case "integer":
            return generate_integer(field)
        case "float":
            return generate_float(field)
        case {"type": "float", "min": minv, "max": maxv}:
            return round(random.uniform(minv, maxv), 2)
        case {"type": "boolean", "true_probability": probability} if 0 <= probability <= 1:
            return random.random() < probability
        case "boolean":
            return random.choice([True, False])
        case "date":
            return generate_date(field)
        case "ip":
            return faker.ipv4()
        case "number":
            return faker.phone_number()

    return None


def generate_market_value(goals, assists, nation):
    base_value = 5

    performance_score = goals * 0.6 + assists * 0.2
    base_value += performance_score

    high_value_nations = ["BR", "GB", "FR", "DE", "ES", "IT", "PT", "AR", "NL"]
    if nation in high_value_nations:
        base_value *= 1.8
    else:
        base_value *= 1.1

    base_value *= random.uniform(0.9, 1.2)

    return int(base_value * 1_000_000)


def generate_goals(age):
    if 18 <= age < 20:
        return random.randint(10, 13)
    elif 21 <= age <= 23:
        return random.randint(14, 18)
    elif 24 <= age <= 25:
        return random.randint(18, 24)
    elif 26 <= age <= 30:
        return random.randint(24, 40)
    elif 31 <= age < 35:
        return random.randint(10, 15)
    elif 35 <= age <= 40:
        return random.randint(5, 10)
    else:
        return random.randint(5, 15)


def generate_assists(age):
    if 18 <= age < 20:
        return random.randint(0, 3)
    elif 21 <= age <= 23:
        return random.randint(3, 7)
    elif 24 <= age <= 25:
        return random.randint(7, 10)
    elif 26 <= age <= 30:
        return random.randint(10, 20)
    elif 31 <= age < 35:
        return random.randint(5, 10)
    elif 35 <= age <= 40:
        return random.randint(0, 4)
    else:
        return random.randint(5, 15)


def generate_date(field):
    contract_start = faker.date_between(start_date="-10y", end_date="now")
    ran_year = random.randint(1, 10)

    if "contract_start" in field:
        return contract_start.strftime("%d/%m/%Y")
    elif "contract_end" in field:
        contract_end = contract_start + timedelta(days=365 * ran_year)
        if contract_end < datetime.today().date():
            contract_end = contract_end + timedelta(days=365 * 5)
        return contract_end.strftime("%d/%m/%Y")

    from_date = datetime.now() - timedelta(days=365 * 50)
    random_day = random.randint(0, 365 * 50)
    random_date = from_date + timedelta(days=random_day)
    return random_date.strftime("%d/%m/%Y")


def generate_integer(field):
    if "wage" in field:
        return random.randint(1000, 250000)
    elif "age" in field:
        return random.randint(18, 36)
    elif "assists" in field:
        return random.randint(0, 20)

    return random.randint(1, 100)


def generate_float(field):
    if "value" in field:
        return round(random.uniform(10000000.0, 100000000.0), 2)
    return round(random.uniform(0, 100), 2)


def generate_string(field):
    field = field.lower()
    if "first" in field:
        return "jeremy"
    elif "last" in field:
        return faker.last_name()

    elif "position" in field:
        positions = ["GK", "CB", "LB", "RB", "MF", "LW", "RW", "ST"]
        weights = [0.05, 0.15, 0.1, 0.1, 0.25, 0.1, 0.1, 0.15]
        return random.choices(positions, weights=weights)[0]
    elif "nationality" in field:
        country = ["GB", "DE", "FR", "ES", "IT", faker.country_code(), "BR", "AR", "PT", "NL"]
        weights = [0.05, 0.1, 0.08, 0.08, 0.12, 0.2, 0.1, 0.09, 0.09, 0.09]
        return random.choices(country, weights=weights)[0]
    elif "job" in field:
        return faker.job()
    elif "club" in field:
        return random.choice(clubs)
    return faker.word()


def realistic_email(sample_data):
    first = (
            sample_data.get("first_name")
            or sample_data.get("name")
            or faker.first_name()
    )
    last = sample_data.get("last_name") or faker.last_name()
    domain = faker.free_email_domain()

    return f"{first.lower()}_{last.lower()}@{domain}"


def get_fullname(sample_data):
    first = (
            sample_data.get("first_name")
            or sample_data.get("name")
            or faker.first_name()
    )
    last = sample_data.get("last_name") or faker.last_name()

    return f"{first} {last}"


if __name__ == "__main__":
    Schema.run()
# main()
