<div align="center">
   <h1>quickd</h1>
   <p>Decorator type based dependency injection</p>
   <p align="center">
    <img alt="GitHub branch checks state" src="https://img.shields.io/github/checks-status/vimtor/quickd/main">
    <img alt="GitHub release (latest by date)" src="https://img.shields.io/github/v/release/vimtor/quickd">
    <img alt="GitHub" src="https://img.shields.io/github/license/vimtor/quickd">
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
- Is mandatory to annotate the function with the return type of the class to later inject
- It is **not** dynamic, so the implementation can only be chosen once

```python
from quickd import factory


@factory
def choose_database() -> Database:
    return PostgreSQL()
```

### `@inject`

- Injects dependencies to a function by matching its arguments types with what has been registered.
- As you can see below, it can work with constructors too

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
class FakeUserRepository(UserRepository):
    def __init__(self):
        self.users = {}

    def save(self, user):
        self.users[user.id] = user

    def search(self, id):
        return self.users[id]


repository = FakeUserRepository()
user_creator = UserCreator(repository)

fake_user = {'id': 1, 'name': 'Tom'}
user_creator.create(fake_user)

assert repository.search(fake_user['id']) == fake_user
```

## 🧠 Motivation

Dependency injection provides a great way to decouple your classes in order to improve testability and maintainability.

Frameworks like [Spring](https://spring.io/) or [Symfony](https://symfony.com/) are loved by the community by how easy
they make this process for the developer.

> I will just add a parameter to the constructor and Spring will fill with a global instance of the class

These frameworks rely heavy on the type system, to know which class should go where.

From Python 3.5 we have the [typing](https://docs.python.org/3/library/typing.html) package, which allows us to have the
simple framework to inject dependencies that Python deserves.

