from quickd import service, inject


@service
class UserRepository:
    def __init__(self):
        self.users = ['Bob', 'Tom', 'Ana']

    def all(self):
        return self.users


def test_service():
    class UserService:
        @inject
        def __init__(self, repository: UserRepository):
            self.repository = repository

        def all(self):
            return self.repository.all()

    user_service = UserService()
    users = user_service.all()
    assert users == ['Bob', 'Tom', 'Ana']


def test_service_with_functions():
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

    assert get_users() == ['Bob', 'Tom']
    add_user()
    assert get_users() == ['Bob', 'Tom', 'Pol']
