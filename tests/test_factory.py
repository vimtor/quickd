from quickd import service, inject, factory


@service
class UserCreator:
    def __init__(self):
        pass

    def create(self):
        pass


class CreateUserCommandHandler:
    @inject
    def __init__(self, creator: UserCreator):
        self.creator = creator

    def __call__(self):
        self.creator.create()


class CommandBus:
    pass


class SyncCommandBus(CommandBus):
    pass


def test_factory_of_injectable():
    @factory
    def choose_bus() -> CommandBus:
        CreateUserCommandHandler()
        return SyncCommandBus()
