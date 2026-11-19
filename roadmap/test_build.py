"""Check the published files through the same builder used for a roadmap update."""
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
from xml.etree import ElementTree

import build


class RoadmapPublicationTest(unittest.TestCase):
    def test_root_and_permalink_match_a_fresh_build(self):
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory)
            with patch.object(build, 'ROOT', output):
                build.build()
            for path in ('index.html', 'v1.8/index.html', 'jira-milestones.svg', 'v1.8/jira-milestones.svg'):
                self.assertEqual((output / path).read_bytes(), (build.ROOT / path).read_bytes(), path)
            for folder, archive in [(output, 'v1.5'), (output / 'v1.8', '../v1.5')]:
                page = (folder / 'index.html').read_text()
                self.assertIn(f'href="{archive}/index.html"', page)
                self.assertNotIn('{{', page)
                self.assertEqual(page.count('<th scope="row">'), 19)
                self.assertIn('AU feedback intake and weekly triage', (folder / 'jira-milestones.svg').read_text())
                for ticket in build.read_rows('tickets.tsv'):
                    self.assertIn(f'#{ticket["ticket"]} ', page)
                    self.assertIn(ticket['status'], page)
                chart = ElementTree.parse(folder / 'jira-milestones.svg')
                self.assertLess(page.index('id="timeline"'), page.index('id="milestones"'))
                self.assertIn('Parked for review with Joe and Yi', page)
                bars = chart.findall('{http://www.w3.org/2000/svg}g[@class="feature"]')
                self.assertEqual(len(chart.findall('{http://www.w3.org/2000/svg}g[@class="checkpoint"]')), 5)
                self.assertEqual(len(bars), 67)
                for bar in bars:
                    title = bar.findtext('{http://www.w3.org/2000/svg}title')
                    self.assertIsNotNone(title)
                    self.assertIn(f'id="{str(title).split()[0]}"', page)
