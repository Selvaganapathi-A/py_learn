import textwrap

import html2text
import markdown


def main():
    text = """
    <h1>Heading 1</h1>
    <p>Paragraph</p>
    <br />
    <img src="../busted.png" alt="land-fish"><hr/>
    <a href="https:/meow-meow.kitten/123">Kitten-Mitten</a>
    """
    markdown_content = html2text.html2text(text)
    print(markdown_content)
    print("=" * 80)
    print(markdown.markdown(markdown_content))
    print("=" * 80)
    print(textwrap.wrap(text))
    print("=" * 80)


if __name__ == "__main__":
    main()
