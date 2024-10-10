def markdown_to_blocks(markdown):
    text_list = [item.strip() for item in markdown.split("\n\n")]
    output_list = []
    for item in text_list:
        if item != "":
            output_list.append(item)
    return output_list