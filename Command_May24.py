"""
Command for CaesarCypherClient and RotatorServer, as well as RotatorForCommand
May 24 2024
"""

import unittest

class Command:
    COMMANDS = {
        "reset": 0b000,
        "increment": 0b001,
        "decrement": 0b010,
        "nTimes": 0b011,
        "getPosition": 0b100,
        "getCharacter": 0b101,
        "rotationCounter": 0b110,
        "close": 0b111
    }

    def __init__(self, op="reset", argv=None):
        if isinstance(op, str):
            op = self.COMMANDS[op]
        self.op = op
        self.argv = argv

    def _set(self, cmd, argv=None):
        if isinstance(cmd, str):
            cmd = self.COMMANDS[cmd]
        self.op = cmd
        self.argv = argv
        if self.argv is not None:
            shiftedArgv = self.argv << 3
            self.op = shiftedArgv | self.op
    
    def _set(self, cmd, argv=None):
        if isinstance(cmd, str):
            cmd = self.COMMANDS[cmd]
        self.op = cmd
        self.argv = argv
        # Can handle a max absolute argv value of 15
        if self.argv is not None:
            if abs(self.argv) > 15:
                raise ValueError("argv must be between -15 and 15")
            newValue = abs(self.argv) << 3
            # Set the sign bit
            if self.argv < 0:
                newValue = newValue | 0b10000000
            else:
                newValue = (newValue & 0b01111111) | self.op
            newValue += 3
            self.op = newValue
            

    def _get(self):
        return self.op
    
    def _getArgv(self):
        return self.argv

    def __str__(self):
        return f"Command(op={self.op}, argv={self.argv})"


class TestCommand(unittest.TestCase):
    def test_reset(self):
        cmd = Command("reset")
        self.assertEqual(cmd._get(), 0b000)

    def test_increment(self):
        cmd = Command("increment")
        self.assertEqual(cmd._get(), 0b001)

    def test_decrement(self):
        cmd = Command("decrement")
        self.assertEqual(cmd._get(), 0b010)

    def test_n_times(self):
        cmd = Command("nTimes", 2)
        self.assertEqual(cmd._get(), 0b011)

    def test_get_position(self):
        cmd = Command("getPosition")
        self.assertEqual(cmd._get(), 0b100)

    def test_get_character(self):
        cmd = Command("getCharacter")
        self.assertEqual(cmd._get(), 0b101)

    def test_rotation_counter(self):
        cmd = Command("rotationCounter")
        self.assertEqual(cmd._get(), 0b110)

if __name__ == '__main__':
    unittest.main()

