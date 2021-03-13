<div align="center">
   <h1 align="center">quickd</h1>
   <p align="center">Decorator type-based dependency injection for Python</p>
   <p align="center">
    <img alt="GitHub Workflow Status" src="https://img.shields.io/github/workflow/status/vimtor/quickd/Test">
    <img alt="GitHub release (latest by date)" src="https://img.shields.io/github/v/release/vimtor/quickd">
    <img alt="GitHub" src="https://img.shields.io/github/license/vimtor/quickd">
    <img alt="PyPI - Downloads" src="https://img.shields.io/pypi/dw/quickd">
   </p>
</div>

## 📦 Installation

The package `quickd` supports Python >= 3.5. You can install it by doing:

```shell
$ pip install quickd
```

## 📜 Example

Here is a quick example:

```python
from quickd import inject, factory


class Database:
    pass


class PostgreSQL(Database):
    def __str__(self):
        return 'PostgreSQL'


class MySQL(Database):
    def __str__(self):
        return 'MySQL'


@inject
def print_database(database: Database):
    return print(database)


@factory
def choose_database() -> Database:
    return PostgreSQL()


print_database()  # Prints: PostgreSQL
print_database(MySQL())  # Prints: MySQL
```

## 🚀 Usage

There are only 3 decorators that compose the whole framework

### `@factory`

- Registers an instance for a specific type for later use with `@inject`
- Is mandatory to annotate the function with the return type of the class that you want to inject later
- It is **not** dynamic, so the implementation can only be chosen once

```python
from quickd import factory


@factory
def choose_database() -> Database:
    return PostgreSQL()
```

### `@inject`

- Injects dependencies to a function by matching its arguments types with what has been registered
- As you can see below, it also works with constructors

```python
from quickd import inject


@inject
def print_database(database: Database):
    return print(database)


class UserService:
    @inject
    def __init__(self, database: Database): pass
```

### `@service`

- Registers a class to be later injectable without using `@factory`
- It also applies `@inject` to its constructor

```python
from quickd import service, inject


@service
class UserService:
    def __init__(self):
        self.users = ['Bob', 'Tom']

    def all(self):
        return self.users

    def add(self, user):
        self.users.append(user)


@inject
def get_users(service: UserService):
    return service.all()


@inject
def add_user(service: UserService):
    return service.add("Pol")


get_users()  # ['Bob', 'Tom']
add_user()
get_users()  # ['Bob', 'Tom', 'Pol']
```

## 👨‍🍳 Recipes

Here are some common solutions to scenarios you will face.

### Interfaces

```python
from abc import abstractmethod
from quickd import inject, factory


class UserRepository:
    @abstractmethod
    def save(self, user):
        pass

    @abstractmethod
    def search(self, id):
        pass


class UserCreator:
    @inject
    def __int__(self, repository: UserRepository):
        self.repository = repository

    def create(self, user):
        self.repository.save(user)


class MySQLUserRepository(UserRepository):
    def __int__(self, host, password):
        self.sql = MySQLConnection(host, password)

    def save(self, user):
        self.sql.execute('INSERT ...')

    def search(self, id):
        self.sql.execute('SELECT ...')


@factory
def choose_user_repository() -> UserRepository:  # Notice super class is being used
    return MySQLUserRepository('user', '123')
```

### Testing

Following the above example we can create a unit test mocking the persistance, which will make our tests easier and
faster.

```python
fake_user = {'id': 1, 'name': 'Tom'}


class FakeUserRepository(UserRepository):
    def save(self, user):
        assert user == fake_user


repository = FakeUserRepository()
user_creator = UserCreator(repository)

user_creator.create(fake_user)
```

### Configuration

There are multiple ways to configure your classes. A simple approach is to use environment variables on your factory
annotated methods.

```python
import os
from quickd import factory


@factory
def choose_database() -> Database:
    username = os.environ.get("POSTGRES_USER")
    password = os.environ.get("POSTGRES_PASS")
    return PostgreSQL(username, password)
```

## 🧠 Motivation

Dependency injection provides a great way to decouple your classes in order to improve testability and maintainability.

Frameworks like [Spring](https://spring.io/) or [Symfony](https://symfony.com/) are loved by the community.

> I will just add a parameter to the constructor and Spring will fill with a global instance of the class

These frameworks rely heavy on the type system, to know which class should go where.

From Python 3.5 we have the [typing](https://docs.python.org/3/library/typing.html) package. This addition allows us to
have the dependency injection framework that Python deserves.

