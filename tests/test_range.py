from .base_config_test import BaseConfigTest, fmod

# ============================================================================
class TestReplayRange(BaseConfigTest):
    @classmethod
    def setup_class(cls):
        super(TestReplayRange, cls).setup_class('config_test.yaml')

    def test_replay_range_start_end(self, fmod):
        headers = [('Range', 'bytes=0-200')]
        resp = self.get('/pywb/20140127171250{0}/http://example.com/', fmod, headers=headers)

        assert resp.status_int == 206
        assert resp.headers['Accept-Ranges'] == 'bytes'
        assert resp.headers['Content-Range'] == 'bytes 0-200/1270', resp.headers['Content-Range']
        assert resp.content_length == 201, resp.content_length

        assert 'wombat.js' not in resp.text

    def test_replay_range_start_end_2(self, fmod):
        headers = [('Range', 'bytes=10-200')]
        resp = self.get('/pywb/20140127171250{0}/http://example.com/', fmod, headers=headers)

        assert resp.status_int == 206
        assert resp.headers['Accept-Ranges'] == 'bytes'
        assert resp.headers['Content-Range'] == 'bytes 10-200/1270', resp.headers['Content-Range']
        assert resp.content_length == 191, resp.content_length

        assert 'wombat.js' not in resp.text

    def test_replay_range_start_only(self, fmod):
        headers = [('Range', 'bytes=0-')]
        resp = self.get('/pywb/20140127171250{0}/http://example.com/', fmod, headers=headers)

        assert resp.status_int == 206
        assert resp.headers['Accept-Ranges'] == 'bytes'
        assert resp.headers['Content-Range'] == 'bytes 0-1269/1270', resp.headers['Content-Range']
        assert resp.content_length == 1270, resp.content_length

        assert 'wombat.js' not in resp.text

    def test_replay_range_on_redirect(self, fmod):
        headers = [('Range', 'bytes=0-')]
        resp = self.get('/pywb/2014{0}/http://www.iana.org/domains/example', fmod, headers=headers)
        assert resp.headers['Location'].startswith('/pywb/2014{0}/'.format(fmod))
        assert resp.status_code == 302

    def test_error_range_out_of_bounds_1(self, fmod):
        headers = [('Range', 'bytes=10-2000')]
        resp = self.get('/pywb/20140127171251{0}/http://example.com/', fmod, headers=headers, status=416)

        assert resp.status_int == 416

    def test_error_range_out_of_bounds_2(self, fmod):
        headers = [('Range', 'bytes=2000-10')]
        resp = self.get('/pywb/20140127171251{0}/http://example.com/', fmod, headers=headers, status=416)

        assert resp.status_int == 416
