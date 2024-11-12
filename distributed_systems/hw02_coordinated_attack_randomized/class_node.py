from random import randint

class Node:
    def __init__(self, node_id, initial_value, r, number_of_nodes):
        self.id = node_id
        self.initial_value = initial_value
        self.r = r
        self.number_of_nodes = number_of_nodes

        self.key = None
        self.choose_key()  # choose the key value

        self.value = [None] * self.number_of_nodes # values
        self.value[node_id] = initial_value # set initial value
        self.level = [-1] * self.number_of_nodes # levels
        self.level[self.id] = 0 # set initial level

    def choose_key(self):
        self.key = randint(1, self.r) if self.id == 0 else None

    def receive_message(self, message):
        message_value = message["value"]
        message_level = message["information_level"]
        self.key = message["key"] if self.key is None else self.key # updating key; if my key is none then
                                                                    # i should update my key
        self.update_value(message_value) # updating the value vector
        self.update_level(message_level) # updating the information level vector


    def update_level(self, message_level):
        for i in range(self.number_of_nodes):
            if i != self.id:
                self.level[i] =max(self.level[i], message_level[i])
        min_value = min([value for i, value in enumerate(self.level) if i != self.id])
        self.level[self.id] = min_value + 1

    def update_value(self, message_value):
        for i in range(self.number_of_nodes):
            if self.value[i] is None and message_value[i] is None:
                continue
            if self.value[i] is None and message_value[i] is not None:
                self.value[i] = message_value[i]
            if self.value[i] is not None and message_value[i] is None:
                continue
            if self.value[i] is not None and message_value[i] is not None:
                self.value[i] = max(message_value[i], self.value[i])

    def generate_message(self):
        message = {"information_level": self.level,
                   "value": self.value,
                   "key": self.key}
        return message

    def decision_making(self, round):
        if self.r == round:
            if (self.key is not None) and all(v == 1 for v in self.value) and (self.level[self.id] >= self.key):
                return 1
            else:
                return 0




    def __repr__(self):
        return f"{"value = ", self.value} {"information level = ", self.level} {"key = ", self.key}"