class MemoryStore:
    def __init__(self):
        self.chat_history = []

    def add_message(self, role, content):
        self.chat_history.append({"role": role, "content": content})
        if len(self.chat_history) > 20:  # Limit memory
            self.chat_history.pop(0)

    def get_history(self):
        return self.chat_history
