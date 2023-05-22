import wave
import array
import hashbrown
import enkrisisturrr

def sign_audio(audio_file, key):
    print("\n ///SIGNED AUDIO EMBEDDING/// \n")
    # Open the audio file
    print("opening audio file...")
    audio = wave.open(audio_file, 'rb')

    # Read the audio file parameters
    num_channels = audio.getnchannels()
    sample_width = audio.getsampwidth()
    frame_rate = audio.getframerate()
    num_frames = audio.getnframes()
    total_samples = num_frames * num_channels

    # Read the audio samples & hashing modified samples
    samples = array.array('h', audio.readframes(num_frames))
    modified_LSB_samples = [set_lsb_to_zero(sample) for sample in samples]
    print("hashing...")
    hash_value = hashbrown.calculate_array_hash(modified_LSB_samples)

    print("creating signature...")
    signature = enkrisisturrr.sign(hash_value, key)

    # Convert the signature bytes into binary & insert the length of the signature at the beginning
    binary_signature = bin(int.from_bytes(signature, byteorder='big'))[2:]
    lenght = format(len(binary_signature),"016b")
    binary_message = lenght + binary_signature

    # Ensure the audio file is long enough to hold the secret message
    if len(binary_message) > total_samples:
        raise ValueError("Secret message is too long to embed in the audio file.")

    # Embed the secret message into the audio samples
    for i in range(len(binary_message)):
        # Get the current sample
        sample = samples[i]

        # Modify the least significant bit of the sample to embed a bit of the secret message
        modified_sample = sample & 0xFFFE  # Clear the least significant bit
        modified_sample |= int(binary_message[i])  # Set the least significant bit to the secret message bit

        # print("modified sample:",modified_sample)

        # Update the sample with the modified value
        samples[i] = modified_sample

    output_file = audio_file[:-4] + "(signed).wav"

    # Create a new wave file to write the modified samples
    output = wave.open(output_file, 'wb')

    # Set the audio file parameters for the output file
    output.setnchannels(num_channels)
    output.setsampwidth(sample_width)
    output.setframerate(frame_rate)

    # Write the modified samples to the output file
    output.writeframes(samples.tobytes())

    # Close the files
    audio.close()
    output.close()

    print("Audio signed successfully!")
    print("signed audio saved at:",output_file)

def verify_audio(audio_file, key):
    print("\n ///SIGNED AUDIO VERIFICATION/// \n")
    
    # Open the audio file
    print("opening audio file...")
    audio = wave.open(audio_file, 'rb')

    # Read the audio file parameters
    num_channels = audio.getnchannels()
    num_frames = audio.getnframes()

    # Calculate the total number of samples in the audio file
    total_samples = num_frames * num_channels

    # Read the audio samples
    samples = array.array('h', audio.readframes(num_frames))

    # Extract signature length
    bitlength = ''
    for i in range(0, 16):
        sample = samples[i]
        bitlength += str(sample & 1)
    length = int(bitlength,2)

    # Extract the signature from the audio samples
    print("extracting signature...")
    binary_signature = ''
    for i in range(16, length+16):
        sample = samples[i]
        binary_signature += str(sample & 1)
    signature = int(binary_signature,2).to_bytes((len(binary_signature) + 7) // 8, byteorder='big')

    # Hash audio file
    print("hashing...")
    modified_LSB_samples = [set_lsb_to_zero(sample) for sample in samples]
    hash_value = hashbrown.calculate_array_hash(modified_LSB_samples)
    
    if (enkrisisturrr.verify(hash_value, signature, key)):
        print("Signature verified!")
    else:
        print("Signature not verified!")


def set_lsb_to_zero(sample):
    # Set the LSB of the sample to zero
    return sample & 0xFFFE

