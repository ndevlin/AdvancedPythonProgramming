"""
Command for CaesarCypherClient and RotatorServer, as well as RotatorForCommand
May 24 2024
"""

import unittest

from RotatorForCommand_May24 import Rotor

class Command:
    def __init__(self, op, argv):
        self.op = op
        self.argv = argv

    def _set(self, cmd):
        self.op, self.argv = cmd

    def _get(self):
        return self.op, self.argv

    def __str__(self):
        return f"Command(op={self.op}, argv={self.argv})"

    def execute(self, rotor):
        if self.op == 0b000:
            rotor.reset()
        elif self.op == 0b001:
            rotor.increment()
            return rotor.__str__()
        elif self.op == 0b010:
            rotor.decrement()
            return rotor.__str__()
        elif self.op == 0b011:
            for _ in range(abs(self.argv)):
                if self.argv > 0:
                    rotor.increment()
                else:
                    rotor.decrement()
            return rotor.__str__()
        elif self.op == 0b100:
            return rotor.position
        elif self.op == 0b101:
            return rotor.__str__()
        elif self.op == 0b110:
            rotor.increment()
            rotor.rotationCounter += 1
        elif self.op == 0b111:
            pass  # TBD
        else:
            raise ValueError(f"Invalid opcode: {self.op}")

class TestCommand(unittest.TestCase):
    def setUp(self):
        self.rotor = Rotor('A', 1, 0x20, 0x80)

    def test_reset(self):
        cmd = Command(0b000, None)
        cmd.execute(self.rotor)
        self.assertEqual(self.rotor.__str__(), 'A')

    def test_increment(self):
        cmd = Command(0b001, None)
        cmd.execute(self.rotor)
        self.assertEqual(self.rotor.__str__(), 'B')

    def test_decrement(self):
        self.rotor.position = ord('B')
        cmd = Command(0b010, None)
        cmd.execute(self.rotor)
        self.assertEqual(self.rotor.__str__(), 'A')

    def test_n_times(self):
        cmd = Command(0b011, 2)
        cmd.execute(self.rotor)
        self.assertEqual(self.rotor.__str__(), 'C')

    def test_get_position(self):
        cmd = Command(0b100, None)
        position = cmd.execute(self.rotor)
        self.assertEqual(position, ord('A'))

    def test_get_character(self):
        cmd = Command(0b101, None)
        character = cmd.execute(self.rotor)
        self.assertEqual(character, 'A')

    def test_rotation_counter(self):
        self.rotor.rotationCounter = 0
        cmd = Command(0b110, None)
        cmd.execute(self.rotor)
        self.assertEqual(self.rotor.rotationCounter, 1)

    def test_invalid_opcode(self):
        cmd = Command(0b1000, None)
        with self.assertRaises(ValueError):
            cmd.execute(self.rotor)

if __name__ == '__main__':
    unittest.main()