"""
Command for CaesarCypherClient and RotatorServer, as well as RotatorForCommand
May 24 2024
"""

import unittest

from RotatorForCommand_May24 import Rotor

class Command:
    COMMANDS = {
        "reset": 0b000,
        "increment": 0b001,
        "decrement": 0b010,
        "nTimes": 0b011,
        "getPosition": 0b100,
        "getCharacter": 0b101,
        "rotationCounter": 0b110,
        "TBD": 0b111
    }

    def __init__(self, op, argv=None):
        if isinstance(op, str):
            op = self.COMMANDS[op]
        self.op = op
        self.argv = argv

    def _set(self, cmd, argv=None):
        if isinstance(cmd, str):
            cmd = self.COMMANDS[cmd]
        self.op = cmd
        self.argv = argv

    def _get(self):
        return self.op, self.argv

    def __str__(self):
        return f"Command(op={self.op}, argv={self.argv})"


class TestCommand(unittest.TestCase):
    def test_reset(self):
        cmd = Command("reset")
        self.assertEqual(cmd._get(), (0b000, None))

    def test_increment(self):
        cmd = Command("increment")
        self.assertEqual(cmd._get(), (0b001, None))

    def test_decrement(self):
        cmd = Command("decrement")
        self.assertEqual(cmd._get(), (0b010, None))

    def test_n_times(self):
        cmd = Command("nTimes", 2)
        self.assertEqual(cmd._get(), (0b011, 2))

    def test_get_position(self):
        cmd = Command("getPosition")
        self.assertEqual(cmd._get(), (0b100, None))

    def test_get_character(self):
        cmd = Command("getCharacter")
        self.assertEqual(cmd._get(), (0b101, None))

    def test_rotation_counter(self):
        cmd = Command("rotationCounter")
        self.assertEqual(cmd._get(), (0b110, None))

if __name__ == '__main__':
    unittest.main()