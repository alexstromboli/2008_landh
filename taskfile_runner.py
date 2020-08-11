# here:
# implement task running

class TaskFileRunner():
    def __init__(self, filepath):
        self.filepath = filepath

    def Run(self):
        return f'Running {self.filepath}'
