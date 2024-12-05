import numpy as np
import rsa
import hashlib

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

# ---------------- FFT Transformation -----------------
def fft_compress(message, compression_ratio=0.1, sender="Alice", receiver="Bob"):
    message_result = { 
      "sender": sender, 
      "receiver": receiver,
      "metadata": {
        "encoding": "fft",
        "compression_ratio": compression_ratio,
        "message_length": len(message),
        "compressed_message_length": -1,
        "real_frequencies": None,
        "imaginary_frequencies": None,
        },
      "message_body": ""
    }
    
    numeric_message = np.array([ord(char) for char in message], dtype=float)
        
    f_transform = np.fft.fft(numeric_message)
    shift_f_transform = np.fft.fftshift(f_transform)
    magnitude = np.abs(shift_f_transform)
    
    threshold = np.quantile(magnitude, 1 - compression_ratio)
    compressed_freq = np.where(magnitude > threshold, shift_f_transform, 0)
    
    message_result["message_body"] = compressed_freq
    message_result["metadata"]["compressed_message_length"] = np.count_nonzero(compressed_freq)
    message_result["metadata"]["real_frequencies"] = compressed_freq.real.tolist()
    message_result["metadata"]["imaginary_frequencies"] = compressed_freq.imag.tolist()
    
    return message_result

def fft_reconstruct(message_dict):
    metadata = message_dict["metadata"]
    
    compressed_freq = np.array(metadata["real_frequencies"], dtype=float) + (np.array(metadata["imaginary_frequencies"], dtype=float) * 1j)
    
    unshift_f_transform = np.fft.ifftshift(compressed_freq)
    reconstruct = np.fft.ifft(unshift_f_transform).real
    
    msg = (chr(int(round(num))) for num in reconstruct)
    
    return ''.join(msg)

# ---------------- CLASSES FOR PERSON, MESSAGE, AND GRAPH -----------------
class Person:
    def __init__(self, id_number, name):
        self.id_number = id_number
        self.name = name
        self.connections = []  # List to hold friends
        (self.public_key, self.private_key) = rsa.newkeys(512)  # Generate RSA keys

    def add_connection(self, friend):
        self.connections.append(friend)
        print(f"{self.name} is now connected to {friend.name}")

class Message:
    def __init__(self, sender_id, receiver_id, details, content, signature=None):
        self.sender_id = sender_id
        self.receiver_id = receiver_id
        self.details = details
        self.content = content
        self.signature = signature  # Signature is optional

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

# ---------------- SIGNED MESSAGES -----------------
def sign_message(sender, message_body):
    message_hash = hashlib.sha256(message_body.encode()).digest()
    signature = rsa.encrypt(message_hash, sender.private_key)
    return signature

def verify_signature(receiver, message_body, signature, sender_public_key):
    message_hash = hashlib.sha256(message_body.encode()).digest()
    decrypted_hash = rsa.decrypt(signature, sender_public_key)
    return message_hash == decrypted_hash

def send_signed_message(sender, receiver, message_body):
    signature = sign_message(sender, message_body)
    message = Message(sender_id=sender.id_number, receiver_id=receiver.id_number, details="signed message", content=message_body, signature=signature)
    print(f"Signed message sent from {sender.name} to {receiver.name}: {message_body}")
    return message

def verify_received_message(receiver, message):
    is_valid = verify_signature(receiver, message.content, message.signature, receiver.public_key)
    return is_valid

# ---------------- MAIN -----------------
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

    # Test the run-length encoding function
    message = "AAAABBBCCDAA"
    encoded_message_body = run_length_encode(message)
    message_dict = {
        "sender": "Alice",
        "receiver": "Bob",
        "metadata": {"encoding": "run-length"},
        "message_body": encoded_message_body
    }
    print(message_dict)

    # Compress message using FFT
    fft_2 = fft_compress(message, compression_ratio=0.2, sender="Alice", receiver="Bob")
    print(fft_2["metadata"]["compressed_message_length"])
    print(fft_reconstruct(fft_2))

    fft_5 = fft_compress(message, compression_ratio=0.5, sender="Alice", receiver="Bob")
    print(fft_5["metadata"]["compressed_message_length"])
    print(fft_reconstruct(fft_5))

    fft_8 = fft_compress(message, compression_ratio=0.8, sender="Alice", receiver="Bob")
    print(fft_8["metadata"]["compressed_message_length"])
    print(fft_reconstruct(fft_8))

    # Example of sending a signed message from Alice to Mike
    original_message = "Hi Mike, this is Alice."
    signed_message = send_signed_message(alice, mike, original_message)
    print(signed_message)

    # Verifying the received signed message
    is_valid = verify_received_message(mike, signed_message)
    print(f"Message verification result: {is_valid}")

if __name__ == "__main__":
    main()
