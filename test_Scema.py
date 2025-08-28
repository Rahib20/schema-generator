from Scema import sample, create_schema, generate_document, display_documents, load_data


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
