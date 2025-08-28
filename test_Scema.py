from Scema import (sample, create_schema, generate_document,
                   display_documents, load_data, generate_market_value,
                   generate_goals,
                   generate_assists,
                   generate_date,
                   generate_integer,
                   generate_float,
                   generate_string,
                   realistic_email,
                   get_fullname)


def test_sample_string():
    value = sample("field", "string")
    assert type(value) == str


def test_sample_number():
    value = sample("field", "number")
    assert type(value) == str


def test_sample_integer():
    value = sample("field", "integer")
    assert type(value) == int


def test_sample_float():
    value = sample("field", "float")
    assert 0 < value < 100


def test_sample_boolean():
    value = sample("field", "boolean")
    assert type(value) == bool


def test_sample_date():
    value = sample("field", "date")
    assert type(value) == str


def test_sample_ip():
    value = sample("field", "ip")
    assert type(value) == str


def test_load_data_returns_dict():
    result = load_data()
    assert type(result) == dict


def test_load_data_not_none():
    result = load_data()
    assert result is not None


def test_generate_document():
    schema = {'name': 'string', 'age': 'integer', 'email': 'email'}

    result = generate_document(schema)

    assert type(result['name']) == str
    assert type(result['age']) == int
    assert type(result['email']) == str


def test_display_documents():
    schema = {'name': 'string', 'age': 'integer', 'email': 'email'}
    # result = generate_document(schema)
    expected_count = 5
    documents = display_documents(5, schema)

    for doc in documents:
        assert len(doc) == 3
        #print(len(doc))
        assert 'name' in doc
        assert 'age' in doc
        assert 'email' in doc
    assert len(documents) == expected_count


def test_generate_market_value():
    value = generate_market_value(10, 5, "BR")
    assert isinstance(value, int)


def test_generate_goals_teen():
    v = generate_goals(18)
    assert 10 <= v <= 13


def test_generate_goals_young():
    v = generate_goals(22)
    assert 14 <= v <= 18


def test_generate_goals_mid20s():
    v = generate_goals(25)
    assert 18 <= v <= 24


def test_generate_goals_peak():
    v = generate_goals(28)
    assert 24 <= v <= 40


def test_generate_goals_early30s():
    v = generate_goals(32)
    assert 10 <= v <= 15


def test_generate_goals_late30s():
    v = generate_goals(37)
    assert 5 <= v <= 10


def test_generate_goals_other():
    v = generate_goals(10)
    assert 5 <= v <= 15


def test_generate_assists():
    value = generate_assists(25)
    assert isinstance(value, int)


def test_generate_date_contract_start():
    value = generate_date("contract_start")
    assert isinstance(value, str)


def test_generate_date_contract_end():
    value = generate_date("contract_end")
    assert isinstance(value, str)


def test_generate_date_random():
    value = generate_date("random_field")
    assert isinstance(value, str)


def test_generate_integer_wage():
    value = generate_integer("wage")
    assert isinstance(value, int)


def test_generate_integer_age():
    value = generate_integer("age")
    assert isinstance(value, int)


def test_generate_integer_default():
    value = generate_integer("other")
    assert isinstance(value, int)


def test_generate_float_value():
    value = generate_float("value")
    assert isinstance(value, float)


def test_generate_float_other():
    value = generate_float("other")
    assert isinstance(value, float)


def test_generate_string_first():
    value = generate_string("first_name")
    assert isinstance(value, str)


def test_generate_string_position():
    value = generate_string("position")
    assert isinstance(value, str)


def test_generate_string_nationality():
    value = generate_string("nationality")
    assert isinstance(value, str)


def test_generate_string_job():
    value = generate_string("job")
    assert isinstance(value, str)


def test_realistic_email():
    data = {"first_name": "John", "last_name": "Smith"}
    value = realistic_email(data)
    assert "@" in value


def test_get_fullname():
    data = {"first_name": "John", "last_name": "Smith"}
    value = get_fullname(data)
    assert "John" in value
