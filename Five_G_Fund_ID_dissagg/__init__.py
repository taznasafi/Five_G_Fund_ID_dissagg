import os



# create initial Data folder for input and output
if not os.path.exists(r'./data'):
    os.mkdir(r'./data')

input_path = r'./data/input'
output_path = r'./data/output'

if not os.path.exists(input_path):
    os.mkdir(input_path)


if not os.path.exists(output_path):
    os.mkdir(output_path)


