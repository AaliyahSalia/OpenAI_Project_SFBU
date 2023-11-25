import json

def convert_to_line_by_line(input_file, output_file):
    with open(input_file, 'r') as file:
        data = json.load(file)

    with open(output_file, 'w') as file:
        for item in data:
            json.dump(item, file)
            file.write('\n')  # Write each JSON object on a new line

# Replace with your file paths
input_file = '/home/sharoncao0802/CS589_Projects/SFBU_Main/SFBU_OpenAI_Project/DataFineTune/DataCollected/data56.json'  # Your current file with JSON array
output_file = './LineByLineData/lineByLine56.json'  # Output file for line-by-line format

convert_to_line_by_line(input_file, output_file)
