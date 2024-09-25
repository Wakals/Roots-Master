import json

def convert_txt_to_json(txt_file, json_file):
    roots_data = []
    with open(txt_file, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    i = 0
    while i < len(lines):
        root_info = {}
        
        # Extract root and definition
        root = lines[i].strip()
        definition = lines[i + 1].strip()
        
        # Extract examples
        examples = []
        j = i + 2
        while j+2 < len(lines) and lines[j+2].strip() != "DONE":
            if j + 3 < len(lines):
                example_word = lines[j].strip()
                example_meaning = lines[j + 1].strip()
                examples.append({"word": example_word, "meaning_cn": example_meaning})
                j += 2
            else:
                break
        
        # Extract first letter and page number
        print('j:', j)
        print(f'len of lines: {len(lines)}')
        first_letter = lines[j].strip()
        page_number = lines[j+1].strip()

        print(f'first_letter: {first_letter}')
        print(f'page_number: {page_number}')
        
        # Store the data
        root_info["root"] = root
        root_info["meaning"] = definition
        root_info["examples"] = examples
        root_info["letter"] = first_letter
        root_info["page"] = page_number
        
        roots_data.append(root_info)

        json_data = {"roots": roots_data}
        
        # Move to the next section
        i = j + 3  # Skip the DONE line

    # Write to JSON file
    with open(json_file, 'w', encoding='utf-8') as json_out:
        json.dump(json_data, json_out, ensure_ascii=False, indent=4)

# Example usage
convert_txt_to_json('./data/raw_roots.txt', './data/roots_data.json')
