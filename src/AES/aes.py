from src.padding import *
import func_aes


class AES:

    def __init__(self, key):
        self.key = (func_aes.break_in_grids_of_16(key))[0]
        self.rounds = 10

    def _encrypt_block(self, block):

        func_aes.add_round_key(block, self.key)

        for i in range(self.rounds):
            func_aes.sub_bytes(block)
            func_aes.shift_rows(block)
            if i != (self.rounds - 1):
                func_aes.mix_columns(block)
            func_aes.add_round_key(block, self.key)

        return block

    def encrypt_text(self, plain_text):
        plain_text = plain_text.encode('utf-8')
        plain_text = pad_text(plain_text)
        blocks = func_aes.break_in_grids_of_16(plain_text)

        for i in range(len(blocks)):
            blocks[i] = self._encrypt_block(blocks[i])

        # Just need to recriate the data into a single stream before returning
        int_stream = []

        for grid in blocks:
            for column in range(4):
                for row in range(4):
                    int_stream.append(grid[row][column])

        print(int_stream)
        return bytes(int_stream)


if __name__ == '__main__':
    aes_new = AES(('2b7e151628aed2a6abf7158809cf4f3c').encode('utf-8'))
    print(aes_new.encrypt_text("30c81c46a35ce411e5fbc1191a0a52ef"))
