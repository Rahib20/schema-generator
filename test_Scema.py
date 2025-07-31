from Scema import sample, create_schema, generate_document, display_documents


def test_sample_string():
    value = sample("string")
    assert type(value) == str


def test_sample_email():
    value = sample("email")
    assert type(value) == str


def test_sample_integer():
    value = sample("integer")
    assert type(value) == int


def test_sample_float():
    value = sample("float")
    assert 0 < value < 100


def test_random_country_code():
    value = sample("country code")
    assert type(value) == str


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
