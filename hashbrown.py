import hashlib
import struct

def calculate_array_hash(array):
    # Create a SHA-256 hash object
    sha256_hash = hashlib.sha256()
    
    # Convert the array of short values to bytes in chunks
    for i in range(0, len(array), 4096):
        chunk = array[i:i+4096]
        byte_data = bytearray()
        for value in chunk:
            byte_data.extend(struct.pack('H', value))
        
        # Update the hash object with the chunk
        sha256_hash.update(byte_data)
    
    # Get the hexadecimal representation of the hash
    array_hash = sha256_hash.digest()
    
    return array_hash

# # Example array of unsigned short values
# audio_data = [32767, 0, 16384, 8192, 4096]

# # Calculate the hash of the array
# hash_value = calculate_array_hash(audio_data)

# # Print the hash value
# print("SHA-256 hash of the array:")
# print(hash_value)