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

# test run
message = "AAAABBBCCDAA"
encoded_message_body = run_length_encode(message)

# dictionary for test
message_dict = {
    "sender": "Alice",
    "receiver": "Bob",
    "metadata": {"encoding": "run-length"},
    "message_body": encoded_message_body
}

# print dictionary
print(message_dict)
