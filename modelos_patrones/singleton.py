def singleton(cls):
    instances = dict()

    def wrap(*args, **kwargs):
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)
        return instances[cls]
    return wrap

@singleton
class User(object):
    def __init__(self, username):
        self.username = username

@singleton
class Admin():
    pass

if __name__ == '__main__':

    user1 = User('admin')
    user2 = User('estudiante1')

    admin1 = Admin()
    admin2 = Admin()

    print(user1 is user2)
    print(admin1 is admin2)