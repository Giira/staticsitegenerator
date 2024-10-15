def markdown_to_blocks(markdown):
    text_list = [item.strip() for item in markdown.split("\n\n")]
    output_list = []
    for item in text_list:
        if item != "":
            output_list.append(item)
    return output_list


def block_to_block_type(block):
    line_list = block.split("\n")
    if block[0] == "#":
        hash_counter = 0
        for letter in block:
            if letter == "#":
                hash_counter += 1
                if hash_counter > 6:
                    return "paragraph"
                else:
                    continue
            if letter != " ":
                return "paragraph"
            elif letter == " ":
                return "heading"
    elif block[0:3] == "```" and len(block) >6 and block[-3:] == "```":
        return "code"
    elif block[0] == ">":
        for line in line_list:
            if line[0] != ">":
                return "paragraph"
        return "quote"
    elif block[0:2] == "* " or block[0:2] == "- ":
        for line in line_list:
            if line[:2] != "* " and line[:2] != "- ":
                return "paragraph"
        return "unordered_list"
    elif block[0].isnumeric() and block[1:3] == ". ":
        counter = 1
        for line in line_list:
            if int(line[0]) != counter or line[1:3] != ". ":
                return "paragraph"
            counter += 1
        return "ordered_list"
    else:
        return "paragraph"