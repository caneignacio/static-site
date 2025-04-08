from nodes import TextNode

def main():
    dummy = TextNode("This is some anchor text", "link", "https://www.boot.dev")

    print(dummy.__repr__())

main()
