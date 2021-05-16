
def padding_text_by_block_size(text, block_size=16):
    amount_of_padding = block_size - len(text) % block_size
    text += "{"*amount_of_padding
    return text, amount_of_padding
