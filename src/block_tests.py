import imp
import unittest
from block import Block
from color import Color


class TestBlock(unittest.TestCase):
    def test_BlockConstructor1(self):
        block = Block(x=32,
                      y=16,
                      block_size=16,
                      num_blocks_x=8,
                      color=Color.BLACK)

        self.assertEqual(block.block_id, 10)


if __name__ == '__main__':
    unittest.main()
