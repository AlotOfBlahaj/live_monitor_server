from unittest import TestCase

from daemon import VideoDaemon


class TestDaemon(TestCase):
    def test_live_status(self):
        class TestLive(VideoDaemon):
            def check(self) -> None:
                pass

        t = TestLive({'target_id': '1'})
        video_dict = {'Title': 'test',
                      'Target': 'test',
                      'Provide': 'test'}
        self.assertEqual(t.current_live, False)
        t.send_to_sub(video_dict)
        self.assertNotEqual(t.current_live, False)
        t.set_no_live()
        self.assertEqual(t.current_live, False)
