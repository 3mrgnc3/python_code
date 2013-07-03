#!/usr/bin/env python

import sys, os

# If the character in the string is the same as the key or null don't XOR that key
# Common way malware will implement XOR to make it less obvious
def null_xor(input_char, key_char):
        if (input_char == key_char or input_char ==(0x00)):
                return input_char
        else:
                return chr(ord(input_char) ^ ord(key_char))

def main():
        input_str = sys.argv[1]
        key_char = sys.argv[2]

        xor_str = ''
        for str in input_str:
                s = null_xor(str, key_char)
                xor_str = xor_str + s
        print xor_str
                



if __name__ == "__main__":
        main()
