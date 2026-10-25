import copy
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('packet', ROOT/'packet.py')
packet = importlib.util.module_from_spec(spec)
spec.loader.exec_module(packet)


class PacketTests(unittest.TestCase):
    def setUp(self):
        self.data = json.loads((ROOT/'examples/file-hash.json').read_text())

    def test_real_handoff_and_no_replay(self):
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp)/'output'
            receipt = packet.build(ROOT/'examples/file-hash.json', out)
            self.assertEqual(receipt['duration_seconds'], 24)
            self.assertEqual(len(json.loads((out/'short.json').read_text())['scenes']), 3)
            self.assertFalse(receipt['published'])
            with self.assertRaises(FileExistsError):
                packet.build(ROOT/'examples/file-hash.json', out)

    def test_bad_reference_rejected(self):
        self.data['scenes'][0]['sources'] = ['invented']
        with self.assertRaises(ValueError): packet.validate(self.data)

    def test_duplicate_source_rejected(self):
        self.data['sources'] *= 2
        with self.assertRaises(ValueError): packet.validate(self.data)

    def test_invalid_durations_rejected(self):
        for value in (-1, float('nan'), True, 1000):
            data = copy.deepcopy(self.data)
            data['scenes'][0]['seconds'] = value
            with self.assertRaises(ValueError): packet.validate(data)

    def test_visual_basis_required(self):
        del self.data['scenes'][0]['visual_basis']
        with self.assertRaises(ValueError): packet.validate(self.data)
