import enkrisisturrr
import steganosaurus

if __name__ == '__main__':
    audio_file = 'Ethel Cain - American Teenager (Official Video).wav'
    output_file = audio_file[:-4] + "(signed).wav"
    public_key, private_key = enkrisisturrr.loadKeys()

    steganosaurus.sign_audio(audio_file, private_key)
    steganosaurus.verify_audio(output_file, public_key)