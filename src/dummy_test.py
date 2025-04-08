from splitters import BlockType, heading_count

def cleaner(text, text_type):
    if text_type == BlockType.ORDERED_LIST:
        ls = []
        for l in text.split("\n"):
            if l != "":
                l = l.strip()
                l = "<li>" + l[3:] + "</li>"
                ls.append(l)
        return ("\n").join(ls)
    elif text_type == BlockType.UNORDERED_LIST:
        ls = []
        for l in text.split("\n"):
            if l != "":
                l = l.strip()
                l = "<li>" + l[2:] + "</li>"
                ls.append(l)
        return ("\n").join(ls)
    elif text_type == BlockType.QUOTE:
        ls = []
        for l in text.split("\n"):
            if l != "":
                l = l.strip()
                l = l[1:]
                ls.append(l)
        return ("\n").join(ls)
    elif text_type == BlockType.HEADING:
        return text[heading_count(text, text_type):]
    else:
        return text
    
block_1 = """
- This is a list    
   - Which is not ordered     
"""

print(cleaner(block_1, BlockType.UNORDERED_LIST))