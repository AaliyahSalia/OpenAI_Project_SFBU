import json

# Function to convert the format of each JSON object
def convert_json_object(obj):
    return {
        "messages": [
            {"role": "system", "content": "Marv is a factual chatbot that is also sarcastic."},
            {"role": "user", "content": obj["prompt"]},
            {"role": "assistant", "content": obj["completion"]}
        ]
    }

def convert_file(input_file, output_file):
    with open(input_file, 'r') as infile:
        lines = infile.readlines()

    with open(output_file, 'w') as outfile:
        for line in lines:
            json_obj = json.loads(line)
            converted_obj = convert_json_object(json_obj)
            outfile.write(json.dumps(converted_obj) + "\n")

# Paths to the input and output files
input_file_path = 'lineByLine151.json'  # Replace with your input file path
output_file_path = 'data151_gpt.json'  # Replace with your output file path

# Convert the file
convert_file(input_file_path, output_file_path)
