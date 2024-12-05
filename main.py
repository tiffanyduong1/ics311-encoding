# ---------------- RUN LENGTH ENCODING -----------------
def run_length_encode(message):
    n = len(message)
    i = 0
    encoded_message = ""
    while i < n:
        count = 1
        while (i < n - 1 and message[i] == message[i + 1]):
            count += 1
            i += 1
        encoded_message += str(count) + message[i]
        i += 1
    return encoded_message

# ---------------- FFT COMPRESSION -----------------
import numpy as np

def fft_compress_message(data, loss_factor):
    data_array = np.frombuffer(data.encode(), dtype=np.int8)
    fft_result = np.fft.fft(data_array)
    cutoff_index = int(len(fft_result) * loss_factor)
    fft_result[cutoff_index:] = 0
    compressed_data = np.fft.ifft(fft_result).real.astype(np.int8).tobytes()
    return compressed_data.decode(errors='ignore')

# ---------------- CLASSES FOR PERSON, MESSAGE, AND GRAPH -----------------
class Person:
    def __init__(self, id_number, name):
        self.id_number = id_number
        self.name = name
        self.connections = []  # List to hold friends

    def add_connection(self, friend):
        self.connections.append(friend)
        print(f"{self.name} is now connected to {friend.name}")

class Message:
    def __init__(self, sender_id, receiver_id, details, content):
        self.sender_id = sender_id
        self.receiver_id = receiver_id
        self.details = details
        self.content = content

    def __str__(self):
        return f"From {self.sender_id} to {self.receiver_id}: {self.content} [{self.details}]"

class SocialGraph:
    def __init__(self):
        self.members = {}

    def add_member(self, person):
        self.members[person.id_number] = person
        print(f"{person.name} has joined the network.")

    def connect_members(self, person1, person2):
        self.members[person1.id_number].add_connection(person2)
        self.members[person2.id_number].add_connection(person1)

    def find_member(self, person_id):
        return self.members.get(person_id)

# ---------------- MAIN FUNCTION TO TEST COMMUNICATION -----------------
def main():
    # Initialize the social network graph
    network = SocialGraph()

    # Create person instances
    alice = Person(id_number=1, name='Alice')
    mike = Person(id_number=2, name='Mike')
    tina = Person(id_number=3, name='Tina')

    # Add members to the network
    network.add_member(alice)
    network.add_member(mike)
    network.add_member(tina)

    # Establish connections (friendships)
    network.connect_members(alice, mike)
    network.connect_members(mike, tina)

    # Sending a run-length encoded message
    original_message = "Hellooooo Mike!"
    encoded_message_body = run_length_encode(original_message)
    message_dict = {
        "sender": "Alice",
        "receiver": "Mike",
        "metadata": {"encoding": "run-length"},
        "message_body": encoded_message_body
    }
    print(message_dict)

    # Sending an FFT compressed message
    original_message_fft = "Hello Tina!"
    compressed_message_body_fft = fft_compress_message(original_message_fft, loss_factor=0.3)
    message_dict_fft = {
        "sender": "Alice",
        "receiver": "Tina",
        "metadata": {"encoding": "FFT", "original_length": len(original_message_fft)},
        "message_body": compressed_message_body_fft
    }
    print(message_dict_fft)

if __name__ == "__main__":
    main()
