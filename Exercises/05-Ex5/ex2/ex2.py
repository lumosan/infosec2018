import wave
import binascii

# Define strings before and after token
str1 = 'COM402{'
str2 = '}'

# Get the binary representation of strings before and after token
b1 = str(bin(int(binascii.hexlify(bytes(str1, 'utf-8')), 16)))[2:]
b2 = str(bin(int(binascii.hexlify(bytes(str2, 'utf-8')), 16)))[2:]

w = wave.open("lucia.monterosanchis@epfl.ch.wav")
print("Number of frames: ", w.getnframes())
print("Number of channels: ", w.getnchannels())
print("Sample width: ", w.getsampwidth())


# Generate 'string', containing the LSB for each frame's second byte
string = ''
for nf in range(w.getnframes()):
    f_hex = binascii.b2a_hex(w.readframes(1))
    f_bin_s = str(bin(int(f_hex, 16)))[2:]
    f_bin_s = '0'*(32-len(f_bin_s)) + f_bin_s

    # a. select each LSB from each byte
    # (only finds b2)
    #string += f_bin_s[7] + f_bin_s[15] + f_bin_s[23] + f_bin_s[31]

    # b. select each LSB from each frame
    # (only finds b2)
    #string += f_bin_s[31]

    # c. select each LSB from each every two bytes, for first sample
    # (only finds b2)
    #string += f_bin_s[15] + f_bin_s[31]

    # d. select each LSB from each every two bytes, for second sample
    # (finds b1 AND b2 :D)
    string += f_bin_s[7] + f_bin_s[23]


# Find start and end positions of token in 'string'
start = string.find(b1)
end = string.find(b2)

token = bytes.fromhex(str(hex(int(string[start:end+len(b2)], 2)))[2:]).decode('utf-8')

print(token)