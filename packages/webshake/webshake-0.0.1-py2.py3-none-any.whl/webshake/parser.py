from enum import Enum


class TokenType(Enum):
    webshake = 1
    NOT_webshake = 2


class Parser:
    def __init__(self, open_symbol="{", close_symbol="}", allow_escape=True):
        self.open_symbol = open_symbol
        self.close_symbol = close_symbol
        self.allow_escape = allow_escape

    def tokenize(self, text):
        resulting_tokens = []
        last_char = None
        token = ""
        token_type = TokenType.NOT_webshake
        open_count = 0
        for i, char in enumerate(text):
            if char == self.open_symbol:
                if self.allow_escape and last_char == "\\":
                    token = token[:-1] + self.open_symbol
                    last_char = None
                    continue
                open_count += 1
                if open_count == 1:  # Found the first open symbol
                    if token:
                        resulting_tokens.append((token_type, i - len(token), token))
                    token = ""
                    token_type = TokenType.webshake
                    continue
            if char == self.close_symbol:
                if self.allow_escape and last_char == "\\":
                    token = token[:-1] + self.close_symbol
                    last_char = None
                    continue
                open_count -= 1
                if open_count == 0:  # Found the last close symbol
                    if token:
                        resulting_tokens.append((token_type, i - len(token), token))
                    token = ""
                    token_type = TokenType.NOT_webshake
                    continue
            token += char
            last_char = char
        if token_type == TokenType.NOT_webshake and token:
            resulting_tokens.append((token_type, i - len(token) + 1, token))
        if open_count != 0:
            raise ValueError("Unbalanced closing symbols on: " + text)
        return resulting_tokens
