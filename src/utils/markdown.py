
def markdown_title(title: str, h=1):
    key = "#" * h
    return key + " " + title + "\n"


def markdown_list_item(item: str):
    return "-" + item + "\n"


def markdown_code(code: str):
    return "`" + code + "`"