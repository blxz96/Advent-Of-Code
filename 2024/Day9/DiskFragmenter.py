from collections import defaultdict

import Utils


class DiskFragmenter:
    def __init__(self):
        self.disk_map = []

    def read_file(self, filename) -> list[int]:
        with open(filename, 'r') as f:
            input_str = f.read().strip()
            disk_map_str = list(input_str)
            self.disk_map = [int(i) for i in disk_map_str]
        return self.disk_map

    def find_part_1_ans(self) -> int:
        # block file and free space alternate
        # need a function to read block file and free space
        # block file is represented as ID number starting from 0
        # free space is represented as .
        # need a function to convert them to block representation
        # need a function to move file block to leftmost
        # need a function to update filesystem checksum
        block_representation = self.generate_block_representation(self.disk_map)
        compressed_block_representation = self.compress_block_representation(block_representation)
        return self.generate_file_system_checksum(compressed_block_representation)

    @staticmethod
    def generate_block_representation(disk_map: list) -> list:
        block_representation = []
        for i, element in enumerate(disk_map):
            if i % 2 == 0:
                # note: block_id don't need to be single digit
                block_id = i // 2
                block_representation.extend(element * [block_id])
            else:
                block_representation.extend(list(element * '.'))
        # We should not use str to join, imagine '13','13' -> join '1313' -> cannot differentiate id
        return block_representation

    @staticmethod
    def compress_block_representation(block_representation: list) -> list:
        left = 0
        right = len(block_representation) - 1
        while left < right:
            if block_representation[left] != '.':
                left += 1
            if block_representation[right] == '.':
                right -= 1
            if block_representation[left] == '.' and block_representation[right] != '.':
                block_representation[left], block_representation[right] = block_representation[right], \
                    block_representation[left]
                left += 1
                right -= 1
        return block_representation

    @staticmethod
    def generate_file_system_checksum(compressed_block_representation: list) -> int:
        checksum = 0
        for position in range(len(compressed_block_representation)):
            if compressed_block_representation[position] == '.':
                break
            else:
                checksum += compressed_block_representation[position] * position
        return checksum

    def find_part_2_ans(self) -> int:
        block_representation = self.generate_block_representation(self.disk_map)
        compressed_block_representation = self.compress_block_representation_2(block_representation)
        return self.generate_file_system_checksum_2(compressed_block_representation)

    @staticmethod
    def compress_block_representation_2(block_representation: list) -> list:
        # find index of file ID and frequency -> store in map
        # need a function get index of all the contiguous free space that is before the index of current file ID
        # if there exist one where len(contiguous free space) >= len contiguous(current file ID), fill up
        blockId_positions = defaultdict(list)
        for position, element in enumerate(block_representation):
            if element != '.':
                blockId_positions[element].append(position)
        blockId_descending = sorted(blockId_positions.keys(), reverse=True)
        for blockId in blockId_descending:
            file_id_first_index = blockId_positions[blockId][0]
            file_id_block_size = len(blockId_positions[blockId])
            block_representation = DiskFragmenter.move_file(block_representation, file_id_first_index,
                                                            file_id_block_size)
        return block_representation

    @staticmethod
    def move_file(block_representation: list, file_id_first_index: int, file_id_block_size: int) -> list:
        empty_space_first_index = -1
        empty_space_length = 0
        is_contiguous = False
        # iterate only up to before file_id_first_index
        for i in range(file_id_first_index):
            if block_representation[i] == '.':
                if not is_contiguous:
                    empty_space_first_index = i
                    empty_space_length = 1
                    is_contiguous = True
                else:
                    empty_space_length += 1
            else:
                is_contiguous = False
                empty_space_first_index = -1
                empty_space_length = 0
            if empty_space_length >= file_id_block_size:
                for i in range(file_id_block_size):
                    block_representation[empty_space_first_index + i], block_representation[file_id_first_index + i] \
                        = block_representation[file_id_first_index + i], block_representation[
                        empty_space_first_index + i]
                break
        return block_representation

    @staticmethod
    def generate_file_system_checksum_2(compressed_block_representation: list) -> int:
        checksum = 0
        for position in range(len(compressed_block_representation)):
            if compressed_block_representation[position] != '.':
                checksum += compressed_block_representation[position] * position
        return checksum


if __name__ == '__main__':
    p = DiskFragmenter()
    p.read_file('input9.txt')
    Utils.eval_and_time_function(p.find_part_1_ans)
    Utils.eval_and_time_function(p.find_part_2_ans)
