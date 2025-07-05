import os


def get_data():
    data = {
        "DB_HOST": input("Enter the database host: "),
        "DB_PORT": input("Enter the database port: "),
        "DB_USER": input("Enter the database user: "),
        "DB_PASS": input("Enter the database password: "),
        "DB_NAME": input("Enter the database name: "),
        #
        "TEST_DB_HOST": input("Enter the test database host: "),
        "TEST_DB_PORT": input("Enter the test database port: "),
        "TEST_DB_USER": input("Enter the test database user: "),
        "TEST_DB_PASS": input("Enter the test database password: "),
        "TEST_DB_NAME": input("Enter the test database name: "),
    }
    return data


def generate_env_file(data, filename=".env_local"):
    with open(filename, "w") as f:
        for key, value in data.items():
            f.write(f"{key}={value}\n")
    print(f"{filename} file has been created successfully.")


if __name__ == "__main__":
    data = get_data()
    generate_env_file(data)
