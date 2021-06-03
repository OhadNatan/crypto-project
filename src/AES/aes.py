from src.padding import *
from src.AES import func_aes
from AES_web import AES as aes_web

class AES:

    def __init__(self, key):
        assert len(key) % 16 == 0
        self.key = (func_aes.break_in_grids_of_16(key.encode('utf-8')))[0]
        self.rounds = 10
        self.expended_key = func_aes.expand_key(key.encode('utf-8'), self.rounds + 1)


    def get_round_key(self, round):
        return [row[round*4: round*4 + 4] for row in self.expended_key]

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
        round_key = self.get_round_key(10)

        # Undo the last step we did at encrypt
        func_aes.add_round_key(block, round_key)
        func_aes.inv_shift_rows(block)
        func_aes.sub_bytes(block, inv=True)

        # Undo the 9 round we did at encrypt
        for i in range(9, 0, -1):
            round_key = self.get_round_key(i)
            func_aes.add_round_key(block, round_key)
            # Doing the mix columns three times is equal to using the reverse matrix
            for _ in range(3):
                func_aes.mix_columns(block)
            func_aes.inv_shift_rows(block)
            func_aes.sub_bytes(block, inv=True)

        # Undo the first step we did at encrypt
        round_key = self.get_round_key(0)
        func_aes.add_round_key(block, round_key)

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

        # str_encrypt = ''.join(chr(i) for i in int_stream)
        # print(str_encrypt)
        return bytes(int_stream)

    def decrypt_text(self, plain_text):
        blocks = func_aes.break_in_grids_of_16(plain_text)

        for i in range(len(blocks)):
            blocks[i] = self._decrypt_block(blocks[i])

        # Just need to recreate the data into a single stream before returning
        int_stream = []

        for grid in blocks:
            for column in range(4):
                for row in range(4):
                    int_stream.append(grid[row][column])

        stream_unpad = unpadding_text(bytes(int_stream))

        return stream_unpad.decode('utf-8')


if __name__ == '__main__':
    import base64
    aes_new = AES('a'*16)
    x = aes_new.encrypt_text("ohad"*4)

    print(x)
    base64_bytes = base64.b64encode(x)
    base64_message = base64_bytes.decode('ascii')
    print(base64_message)
    y = aes_new.decrypt_text(x)

    print(y)
