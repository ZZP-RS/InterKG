import re
filename = "max_dict.txt"
j=1
with open("new", "w") as output_file:
    with open(filename, "r") as file:
        for line in file:
            results = []
            lists = re.findall(r"\[\[(.*?)\]\]", line)
            line_lists = []

            for i, lst in enumerate(lists):
                numbers = re.findall(r"\d+", lst)
                line_lists.append(numbers)
                output_file.write(f"{numbers} % {i + 1 + 8} % {i + j + 106388}\n")

            j = j + 36


with open('new', 'r') as file:
    lines = file.readlines()

    with open('new-kg.txt', 'w') as file:
        for line in lines:
            values = line.split(' %')
            nums = re.findall(r"\d+", values[0])
            for num in nums:
                output_line = f"{num}{values[1]}{values[2]}"
                file.write(output_line)