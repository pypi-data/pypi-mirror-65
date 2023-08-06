import os


class EnterDir:
    def __init__(self, go_to: str, create=False):
        self.back_to: str = os.getcwd()
        self.go_to: str = go_to
        self.create: bool = create

    def __enter__(self):
        if self.create and not os.path.isdir(self.go_to):
            os.mkdir(self.go_to)
        os.chdir(self.go_to)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        os.chdir(self.back_to)
