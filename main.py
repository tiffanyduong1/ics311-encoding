import numpy as np

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
    

# ---------------- MAIN -----------------

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

# compress message using FFT
fft_2 = fft_compress(message, compression_ratio=0.2, sender="Alice", receiver="Bob")
print(fft_2["metadata"]["compressed_message_length"])
print(fft_reconstruct(fft_2))

fft_5 = fft_compress(message, compression_ratio=0.5, sender="Alice", receiver="Bob")
print(fft_5["metadata"]["compressed_message_length"])
print(fft_reconstruct(fft_5))

fft_8 = fft_compress(message, compression_ratio=0.8, sender="Alice", receiver="Bob")
print(fft_8["metadata"]["compressed_message_length"])
print(fft_reconstruct(fft_8))


