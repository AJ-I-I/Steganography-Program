# Stenography
READ.ME
INSTRUCTIONS
-Install imports-
To ensure this program runs you must have the Pillow and sys libraries in Python.
To do this, run this line in the terminal to install using pip
	pip install Pillow

-To run the embedding program-
Navigate to the directory where the program.
To do this...
	1.) Open the terminal 
	2.) use the following line in the terminal:
    		cd C:\Users\<file folder location>

Next, to embed your message run the following line:
    python steg.py embed_message "<file path to input_image>" output_image.bmp "<your message>"

This will embed the message into your image and create a new bit map file called output_image.bmp

-To run the extraction program-
To extract the message run the following line: 
    python. steg.py extract_message “<file path to output_image.bmp>"
