import importlib.util
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest

ROOT=Path(__file__).resolve().parents[1]


class PortableSkills(unittest.TestCase):
    def test_standalone_handoff_cli_without_repository(self):
        with tempfile.TemporaryDirectory() as tmp:
            skill=Path(tmp)/'installed'
            shutil.copytree(ROOT/'skills/build-video-handoff',skill,ignore=shutil.ignore_patterns('__pycache__'))
            out=Path(tmp)/'handoff'
            result=subprocess.run([sys.executable,str(skill/'scripts/build_packet.py'),str(skill/'assets/example-brief.json'),'--out',str(out)],cwd=tmp,capture_output=True,text=True,check=True)
            self.assertEqual(json.loads(result.stdout)['duration_seconds'],24)
            self.assertEqual(len(json.loads((out/'short.json').read_text())['scenes']),3)

    def test_generated_squad_handoffs_and_collision_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            skill=Path(tmp)/'installed'
            shutil.copytree(ROOT/'skills/workflow-to-aiox-squad',skill,ignore=shutil.ignore_patterns('__pycache__'))
            out=Path(tmp)/'squad'
            command=[sys.executable,str(skill/'scripts/scaffold_squad.py'),str(skill/'assets/workflow.json'),'--out',str(out)]
            result=subprocess.run(command,cwd=tmp,capture_output=True,text=True,check=True)
            receipt=json.loads(result.stdout)
            self.assertEqual(receipt['steps'],['evidence-check','demo-plan','claim-review'])
            self.assertFalse(receipt['host_execution_tested'])
            self.assertTrue((out/'tasks/claim-review.md').is_file())
            self.assertNotEqual(subprocess.run(command,cwd=tmp,capture_output=True).returncode,0)
            data=json.loads((skill/'assets/workflow.json').read_text())
            data['steps'].append(data['steps'][0])
            (skill/'assets/duplicate.json').write_text(json.dumps(data))
            bad=Path(tmp)/'bad'
            result=subprocess.run([sys.executable,str(skill/'scripts/scaffold_squad.py'),str(skill/'assets/duplicate.json'),'--out',str(bad)],cwd=tmp,capture_output=True)
            self.assertNotEqual(result.returncode,0)
            self.assertFalse(bad.exists())
