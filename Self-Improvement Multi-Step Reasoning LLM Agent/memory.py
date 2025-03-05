class Memory:
    def __init__(self):
        self.logs = []

    def add(self, entry):
        self.logs.append(entry)

    def recall(self):
        return "\n".join(self.logs)
