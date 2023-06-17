# an example of hard to test code. 
CUSTOMERS_DB = [
    {"name": "Jennifer Love Hewitt", "age": 55},
    {"name": "Anthony Hopkins", "age": 34},
    {"name": "Martin Godzilla", "age": 67},
    {"name": "Tony Jabroney", "age": 21}
]


def create_customer_file():
    customers = CUSTOMERS_DB

    with open('../output/customers_over_50_report.txt', 'w') as writer:
        filtered_customers = list(filter((lambda customer: customer['age'] > 50), customers))

        for customer in filtered_customers:
            writer.write(f'{customer["name"]}, { customer["age"]}\n')

# An approach to unit testsing the above code!
import os

def validate_customer_over_50_file_exists():
    path = '../output/customers_over_50_report.txt'
    assert os.path.isfile(path), "Path should exist"

def validate_customer_over_50_file():
    with open('../output/customers_over_50_report.txt', 'r') as reader:
        line = reader.readline()
        while line != '':
            record = line.split(',')
            record = [v.strip() for v in record]
            assert int(record[1]) > 50, "Customer should be over 50"

            line=reader.readline()

# refactoring our code

# stores and returns data
class CustomerRepository:
    def __init__(self):
        pass

    def get_customers(self):
        return [
            {"name": "Jennifer Love Hewitt", "age": 55},
            {"name": "Anthony Hopkins", "age": 34},
            {"name": "Martin Godzilla", "age": 67},
            {"name": "Tony Jabroney", "age": 21}
        ]

# data interactions
class CustomerService:
    def __init__(self):
        pass

    def filter_customers(self, customers):
        return list(filter((lambda customer: customer['age'] > 50), customers))

    def get_customer_record_format(self, customer):
        return f'{customer["name"]}, { customer["age"]}'

# writes to files
class FileWriter():
    def __init__(self):
        pass

    def write_file(self, file_name, contents):
        with open(file_name, 'w') as writer:
            for line in contents:
                writer.write(line + '\n')

def main(customer_repository, customer_service, file_writer):
    customers = customer_repository.get_customers()
    customers_over_50 = customer_service.filter_customers(customers)
    formatted_customers_over_50 = [customer_service.get_customer_record_format(customer) for customer in customers_over_50]
    file_writer.write_file("../output/customers_over_50_report.txt", formatted_customers_over_50)

main(CustomerRepository(), CustomerService(), FileWriter())
validate_customer_over_50_file_exists()
validate_customer_over_50_file()



def test_customer_repository(customer_repository):
    customers = customer_repository.get_customers()

    for customer in customers:
        assert customer["name"] != None and customer["age"] != None


def test_customer_service_filter(customer_service):
    customers = [
        {"name": "Jennifer Love Hewitt", "age": 55},
        {"name": "Anthony Hopkins", "age": 34},
    ]

    filtered_customers = customer_service.filter_customers(customers)

    assert len(filtered_customers) == 1

    for customer in filtered_customers:
        assert customer["age"] > 50


def test_customer_service_record_format(customer_service):
    customers = {"name": "Jennifer Love Hewitt", "age": 55}

    formatted_customer = customer_service.get_customer_record_format(customers)

    assert formatted_customer == "Jennifer Love Hewitt, 55", f"Should be like a CSV, but instead is {formatted_customer}"


test_customer_repository(CustomerRepository())
test_customer_service_filter(CustomerService())
test_customer_service_record_format(CustomerService())

from unittest.mock import patch, mock_open

def test_file_writer():
    file_writer = FileWriter()
    open_mock = mock_open()

    with patch("__main__.open", open_mock, create=True):
        file_writer.write_file("../output/test.txt", ["my-data"])

    open_mock.assert_called_once_with("../output/test.txt", "w")
    open_mock.return_value.write.assert_called_once_with("my-data\n")

test_file_writer()



