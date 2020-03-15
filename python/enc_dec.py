from itertools import cycle
import string
import vim

# Get all printables except special chars
PRINTABLES = [
    x for x in string.printable
    if x not in ['\b', '\t', '\n', '\r', '\x0b', '\x0c']
]
MODULUS = len(PRINTABLES)
PRINTABLES_MAP = {x: i for i, x in enumerate(PRINTABLES)}
PRINTABLES_MAP_REV = {v: k for k, v in PRINTABLES_MAP.items()}

# The ENCRYPT DELIMETER will separate the lines that are encrypted or not
# This will be the starting of the line that is encrypted
ENCRYPT_DELIMETER = '$$$'


def get_secret() -> str:
    """This gets secret value stored in vim's buffer variable 'secret'"""
    try:
        secret = vim.eval('b:secret')
        if not secret:
            raise Exception
        return secret
    except Exception:
        # TODO: check for vim/nvim specific errors
        raise Exception('No secret set. And it cannot be empty')


def set_border_line_number(file_content: str) -> None:
    """Sets b border_line_number the line number below which is the encrypted
    text(inclusive)"""
    lines = file_content.split('\n')
    border_line = 0
    for i, line in enumerate(lines):
        if line[:3] != '$$$':
            break
        border_line = i + 1
    vim.command(f"let b:border_line_number = {border_line}")


def get_encrypted_and_unencrypted_lines(file_content: str) -> (str, str):
    """
    The .sec file consists of initial zero or more lines starting with $$$
    which are encrypted followed by the ones not starting with $$$ which are
    decrypted.
    Returns: ([<encrypted lines>], [<unencrypted_lines>])
    """
    lines = file_content.split('\n')
    line_num = None
    # Check for the first line that is not encrypted
    for i, line in enumerate(lines):
        if line[:3] != '$$$':
            line_num = i
            break
    if line_num is None:
        # This means every line is encrypted
        return lines, []
    return lines[:line_num], lines[line_num:]


def encrypt_buffer(file_content: str):
    """This function gets the unencrypted content of the buffer, and encrypts them.
    The encrypted content will start from $$$
    """
    secret = get_secret()
    encrypted, unencrypted = get_encrypted_and_unencrypted_lines(file_content)
    content = '\n'.join([
        *encrypted,
        *[ENCRYPT_DELIMETER+encrypt(x, secret) for x in unencrypted]
    ])
    with open('/tmp/_vim_secret', 'w') as f:
        f.write(content)


def decrypt_buffer(file_content: str):
    """This function gets the encrypted content of the buffer, and decrypts them.
    The decrypted content will have the starting $$$ removed
    """
    secret = get_secret()
    encrypted, unencrypted = get_encrypted_and_unencrypted_lines(file_content)
    content = '\n'.join([
        *[decrypt(x[3:], secret) for x in encrypted],
        *unencrypted,
    ])
    with open('/tmp/_vim_secret', 'w') as f:
        f.write(content)


def encrypt(text: str, secret: str):
    """Encrypt the text using secret. Caesar Cypher will be used.
    And This won't be too bad because the secret can have any length.
    """
    pairs = zip(cycle(secret), text)
    return ''.join(caesar(PRINTABLES_MAP[k], v) for k, v in pairs)


def decrypt(text: str, secret: str):
    """Decrypts the text. Similar to encrypt, just uses negative of key"""
    pairs = zip(cycle(secret), text)
    return ''.join(caesar(-PRINTABLES_MAP[k], v) for k, v in pairs)


def caesar(shift_len: int, char: str):
    """
    Shifts the char by shift_len.
    """
    if char in PRINTABLES_MAP:
        return PRINTABLES_MAP_REV[(PRINTABLES_MAP[char] + shift_len) % MODULUS]
    return char
