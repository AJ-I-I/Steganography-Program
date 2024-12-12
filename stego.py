import sys            # IMPORTS
from PIL import Image # Sys and PIL (Pillow)'s image


MAX_IMG_SIZE = 5242880   # set MAX_IMG_SIZE to be a total of 5242880 Bytes (in binary)
MAX_MESSAGE_LENGTH = 256 # set maximum length of characters message

# Embedding message method
def embed_message(input_image_path, output_image_path, message):
    # error checks: message length, characters of message, file type
    if len(message) > MAX_MESSAGE_LENGTH:
        print("ERROR: Message length exceeds maximm limit of 256 ASCII characters.")
        return

    # check if users message contains only ascii chars
    try:
        message.encode('ascii')
    except UnicodeEncodeError:
        print("ERROR: Message must contain ASCII characters only")
        return

    # check file type
    with Image.open(input_image_path) as img:
        if img.format != "BMP":
            print("ERROR: Image format must be a Bitmap file (.bmp).")
            return

    # check file size
    with open(input_image_path, 'rb') as f:
        InputSIZE = len(f.read())
        if InputSIZE > MAX_IMG_SIZE:
            print("ERROR: Image file exceeds 5 MB.")
            return

    img = Image.open(input_image_path)
    img = img.convert("RGB")
    pixels = img.load()


    # Convert the message into a binary string
    binary_message = ''.join([f"{ord(c):08b}" for c in message]) + '00000000' # append null byte to users message
    # Set up counters to track how many pixels and bits are affected by message being embedded
    BTCounter = 0
    PXCounter = 0


    # Embed the message into the LSB of each pixel
    idx = 0
    for y in range(img.height):
        for x in range(img.width):
            if idx < len(binary_message):
                r, g, b = pixels[x, y]
                OGPX = (r, g, b) # set var OGPX to store original amount of pixels
                r = (r & ~1) | int(binary_message[idx])
                if r != OGPX[0]: BTCounter += 1
                idx += 1
                if idx < len(binary_message):
                    g = (g & ~1) | int(binary_message[idx])
                    if g != OGPX[0]: BTCounter += 1
                    idx += 1
                if idx < len(binary_message):
                    b = (b & ~1) | int(binary_message[idx])
                    if b != OGPX[0]: BTCounter += 1
                    idx += 1
                if (r, g, b) != OGPX: # Update pixel amount if any change happened while embedding
                    pixels[x, y] = (r, g, b)
                    PXCounter += 1 # Increase Pixel counter by 1
            else:
                break
        if idx >= len(binary_message):
            break
    # Save the image with users message embedded
    img.save(output_image_path)


    with open(output_image_path, 'rb') as f:
        SIZE = len(f.read())
    Size_Difference = SIZE - InputSIZE


    print(".") # print out conformation of embedding process to user
    print("..")
    print("...")
    print("Message successfully embedded in selected image.")
    print("Number of bits changed:", BTCounter)
    print("Number of pixels changed:", PXCounter)
    print("The file size has changed: ", SIZE, "bytes")


# Exctact message method
def extract_message(input_image_path):
    # load in the image through the image path, check if size is too large
    with open(input_image_path, 'rb') as f:
        if len(f.read()) > MAX_IMG_SIZE:
            print("ERROR: Image file exceeds 5 MB.")
            return
    # check file type
    with Image.open(input_image_path) as img: # open image file, check file type
        if img.format != "BMP":
            print("ERROR: Image format must be a Bitmap file (.bmp).")
            return


    img = Image.open(input_image_path) # open image file to extract
    img = img.convert("RGB") # convert loaded image into RGB format
    pixels = img.load()


    # extract binary message from LSB of pixels
    binary_message = "" # set message to be blank, fills in with changed r, g, b values while going through pixels unless null byte delimiter is found
    for y in range(img.height):
        for x in range(img.width):
            r, g, b = pixels[x, y]
            binary_message += str(r & 1)
            binary_message += str(g & 1)
            binary_message += str(b & 1)


    # convert binary message back to ASCII characters
    chs = [binary_message[i:i+8] for i in range(0, len(binary_message), 8)]
    message = ""
    for char in chs:
        if char == "00000000":
            break
        message += chr(int(char,2))


    if message:
        print(".") # print out conformation that program ran to user
        print("..")
        print("...")
        print("Extracted message:", message) # print out user's original message now extracted from image
    else:
        print("ERROR: No message found in format")


# MAIN
if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("For usage:")
        print("To embed a message use form: embed_message <input_image> <output_image> <message>") # print what the required arguement format is to user
        print("To extract a message already embedded use form: extract_message <input_image>")     # for embedding and extracting
    else:
        command = sys.argv[1]
        if command == "embed_message" and len(sys.argv) == 5:
            _, _, input_image, output_image, message = sys.argv
            embed_message(input_image, output_image, message)
        elif command == "extract_message" and len(sys.argv) == 3:
            _, _, input_image = sys.argv
            extract_message(input_image)
        else:
            print("ERROR: Invalid command.")