from src.padding import *
import func_aes


class AES:

    def __init__(self, key):
        self.key = (func_aes.break_in_grids_of_16(key.encode('utf-8')))[0]
        self.expended_key = func_aes.key_expansion(self.key)
        self.rounds = 10

    def get_round_key(self, round_index):
        key = [[1,2,3,4], [1,2,3,4], [1,2,3,4], [1,2,3,4]]

        start_index = 4*round_index

        for i in range(start_index, start_index + 4):
            func_aes.set_column(key, self.expended_key[i], i - start_index)

        return key

    def _encrypt_block(self, block):

        func_aes.add_round_key(block, self.get_round_key(0))

        for i in range(self.rounds):
            func_aes.sub_bytes(block)
            func_aes.shift_rows(block)
            if i != (self.rounds - 1):
                func_aes.mix_columns(block)
            func_aes.add_round_key(block, self.get_round_key(i + 1))

        return block

    def _decrypt_block(self, block):
        func_aes.add_round_key(block, self.get_round_key(10))

        for i in range(self.rounds):
            func_aes.inv_shift_rows(block)
            func_aes.sub_bytes(block, inv=True)
            func_aes.add_round_key(block, self.get_round_key(9-i))
            if i != (self.rounds - 1):
                func_aes.mix_columns(block)

        return block

    def encrypt_text(self, plain_text):
        plain_text = plain_text.encode('utf-8')
        plain_text = pad_text(plain_text)
        blocks = func_aes.break_in_grids_of_16(plain_text)

        for i in range(len(blocks)):
            blocks[i] = self._encrypt_block(blocks[i])

        # Just need to recreate the data into a single stream before returning
        int_stream = []

        for grid in blocks:
            for column in range(4):
                for row in range(4):
                    int_stream.append(grid[row][column])

        str_encrypt = ''.join(chr(i) for i in int_stream)
        return str_encrypt

    def decrypt_text(self, plain_text):
        blocks = func_aes.break_in_grids_of_16(plain_text.encode('utf-8'))

        for i in range(len(blocks)):
            blocks[i] = self._decrypt_block(blocks[i])

        # Just need to recreate the data into a single stream before returning
        int_stream = []

        for grid in blocks:
            for column in range(4):
                for row in range(4):
                    int_stream.append(grid[row][column])

        str_deccrypt = ''.join(chr(i) for i in int_stream)
        return str_deccrypt


if __name__ == '__main__':
    aes_new = AES(('aaaaaaaaaaaaaaaa'))
    x = aes_new.encrypt_text("ohadohadohadohad")

    print(x)

    y = aes_new.decrypt_text(x)

    print(y)
