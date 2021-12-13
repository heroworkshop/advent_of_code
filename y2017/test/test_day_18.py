import unittest

from y2017.day_09 import unescape, remove_garbage, make_tree
from y2017.sound_chip import SoundChip, ConnectedChip


class TestSoundChip(unittest.TestCase):
    def test_play_sound_withValue_playsValue(self):
        program = "snd 54"
        chip = SoundChip(program)
        chip.run()
        self.assertEqual(54, chip.last_sound)

    def test_set_withValue_setsRegisterToValue(self):
        program = "set a 54"
        chip = SoundChip(program)
        chip.run()
        self.assertEqual(54, chip.registers["a"])

    def test_play_sound_withRegister_playsRegisterValue(self):
        program = ("set a 54\n"
                   "snd a")
        chip = SoundChip(program)
        chip.run()
        self.assertEqual(54, chip.last_sound)

    def test_add_withValue_addsValueToRegister(self):
        program = ("set a 54\n"
                   "add a 10")
        chip = SoundChip(program)
        chip.run()
        self.assertEqual(64, chip.registers["a"])

    def test_add_withRegister_addsRegisterValueToRegister(self):
        program = ("set a 54\n"
                   "set b 10\n"
                   "add a b")
        chip = SoundChip(program)
        chip.run()
        self.assertEqual(64, chip.registers["a"])

    def test_mul_withValue_multipliesValueByRegister(self):
        program = ("set a 54\n"
                   "mul a 10")
        chip = SoundChip(program)
        chip.run()
        self.assertEqual(540, chip.registers["a"])

    def test_mul_withRegister_multipliesRegisterValueByRegister(self):
        program = ("set a 54\n"
                   "set b 10\n"
                   "mul a b")
        chip = SoundChip(program)
        chip.run()
        self.assertEqual(540, chip.registers["a"])

    def test_mod_withValue_ModsRegisterByValue(self):
        program = ("set a 54\n"
                   "mod a 10")
        chip = SoundChip(program)
        chip.run()
        self.assertEqual(4, chip.registers["a"])

    def test_mul_withRegister_modsRegisterByRegisterValue(self):
        program = ("set a 54\n"
                   "set b 10\n"
                   "mod a b")
        chip = SoundChip(program)
        chip.run()
        self.assertEqual(4, chip.registers["a"])

    def test_rcv_withZeroInRegister_doesNothing(self):
        program = "rcv a"
        recovered = []

        def on_recover(chp):
            recovered.append(1)

        chip = SoundChip(program, on_recover=on_recover)
        chip.run()
        self.assertFalse(recovered)

    def test_rcv_withNonZeroInRegister_callsOnRecover(self):
        program = ("set a 1\n"
                   "rcv a")

        recovered = []

        def on_recover(chp):
            recovered.append(1)

        chip = SoundChip(program, on_recover=on_recover)
        chip.run()
        self.assertEqual(1, len(recovered))

    def test_jgz_withZeroInRegister_doesNothing(self):
        program = ("jgz a 2\n"
                   "set x 10\n"
                   "set y 5"
                   )

        chip = SoundChip(program)
        chip.run()
        self.assertEqual(10, chip.registers["x"])

    def test_jgz_withOneInRegister_jumpsByParam2(self):
        program = ("set a 1\n"
                   "jgz a 2\n"
                   "set x 10\n"
                   "set y 5"
                   )

        chip = SoundChip(program)
        chip.run()
        self.assertEqual(0, chip.registers.get("x", 0))
        self.assertEqual(5, chip.registers["y"])

class TestSoundChip(unittest.TestCase):
    def test_snd_withConnectedChip_isReceivedByConnectedChip(self):
        program1 = ("snd 10")
        program2 = ("rcv a")
        chip1 = ConnectedChip(program1)
        chip2 = ConnectedChip(program2)
        chip1.connect(chip2)
        chip2.connect(chip1)
        chip1.run()
        chip2.run()
        self.assertEqual(10, chip2.registers["a"])
