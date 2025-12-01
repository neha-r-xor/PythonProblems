class Bug:
    def __init__(self, bug_id, title, description, severity):
        self.bug_id = bug_id
        self.title = title
        self.description = description
        self.severity = severity
    
    
    def validate_report(self):
        missing = []
        if not self.title:
            missing.append("'title'")
        if not self.description:
            missing.append("'description'")
        if not self.severity:
            missing.append("'severity'")
        if missing:
            return f"Error: The bug report is missing data in the following field(s): {', '.join(missing)}."
        return "VALID"



def read_bug_data(file_path):
    try:
        data_list = []
        with open(file_path, 'r') as file:
            for line in file:
                data_list.append(tuple(line.split(',')))
        return data_list
    except FileNotFoundError:
        raise FileNotFoundError(f"File not found: {file_path}")

def process_and_save_report(data_list, output_file):
    try:
        output_data_list = []
        for line in data_list:
            bug = bug = Bug(line[0].strip(), line[1].strip(), line[2].strip(), line[3].strip())
            result = bug.validate_report()
            output_line = f'Bug ID {line[0]} : ' + result
            output_data_list.append(output_line)
        
        with open(output_file, 'w') as file:
            for line in output_data_list:
                file.write(line + "\n")

    except FileNotFoundError:
         raise FileNotFoundError(f"File not found: {output_file}")    


def main():
    input_path = "input_third.txt"
    output_path = "output_third.txt"
    
    data_list = read_bug_data(input_path)
    process_and_save_report(data_list, output_path)



if __name__ == "__main__":
    main()


            