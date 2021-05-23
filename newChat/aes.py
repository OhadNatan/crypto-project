import padding
import func_aes


class AES:

    def __init__(self, key):
        self.key = (func_aes.break_in_grids_of_16(key))[0]
        self.rounds = 10

    def _encrypt_block(self, block):

        func_aes.add_round_key(block, self.key)

        for i in range(self.rounds):
            print("block before index {} -\n{}\n".format(i, block)) #TODO: delete
            func_aes.sub_bytes(block)
            func_aes.shift_rows(block)
            if i != (self.rounds - 1):
                func_aes.mix_columns(block)
            func_aes.add_round_key(block, self.key)
            print("block after index {} -\n{}\n".format(i, block))  # TODO: delete

        return block

    def encrypt_text(self, plain_text):
        plain_text = plain_text.encode('utf-8')
        plain_text = padding.pad_text(plain_text)
        blocks = func_aes.break_in_grids_of_16(plain_text)

        for i in range(len(blocks)):
            blocks[i] = self._encrypt_block(blocks[i])

        return blocks

if __name__ == '__main__':
    aes_new = AES(('a'*16).encode('utf-8'))
    print(aes_new.encrypt_text("ohad"*4))
