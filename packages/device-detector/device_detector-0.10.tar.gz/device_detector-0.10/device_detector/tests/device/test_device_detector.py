from ..base import DetectorBaseTest
from ...device_detector import DeviceDetector


class TestNormalized(DetectorBaseTest):

    fixture_files = [
        'tests/fixtures/local/normalize.yml',
    ]

    def test_parsing(self):
        return

    def test_normalized(self):

        for fixture in self.load_fixtures():
            self.user_agent = fixture.pop('user_agent')
            device = DeviceDetector(self.user_agent)
            device.parse()

            self.assertEqual(device.pretty_name(), fixture['normalized'])


class TestAppNames(DetectorBaseTest):
    """
    Get expected App Names. Should take precedence over upstream regexes
    """

    fixture_files = [
        'tests/fixtures/local/app_names.yml',
    ]

    def test_parsing(self):
        return

    def test_client_details(self):

        for fixture in self.load_fixtures():
            self.user_agent = fixture.pop('user_agent')
            parsed = DeviceDetector(self.user_agent).parse()

            # Client properties
            self.confirm_client_name(fixture, parsed_name=parsed.preferred_client_name())
            self.confirm_client_type(fixture, parsed_value=parsed.preferred_client_type())
            self.confirm_version(fixture, parsed_value=parsed.preferred_client_version())


class TestDetectBot(DetectorBaseTest):

    fixture_files = [
        'tests/fixtures/upstream/bots.yml',
    ]

    def test_parsing(self):

        for fixture in self.load_fixtures():
            self.user_agent = fixture.pop('user_agent')
            bot = DeviceDetector(self.user_agent).parse()

            expected_values = fixture['bot']
            parsed_values = bot.all_details['bot']

            for field in ('name', 'url', 'category'):
                expected = expected_values.get(field, 'N/A')
                parsed = parsed_values.get(field, 'N/A')
                self.assertEqual(
                    parsed, expected,
                    msg=f'Parsed "{parsed}" != Expected "{expected}" on {self.user_agent}',
                )


class TestDetectCamera(DetectorBaseTest):

    fixture_files = [
        'tests/fixtures/upstream/camera.yml',
    ]


class TestDetectCarBrowser(DetectorBaseTest):

    fixture_files = [
        'tests/fixtures/upstream/car_browser.yml',
    ]


class TestDetectConsole(DetectorBaseTest):

    fixture_files = [
        'tests/fixtures/upstream/console.yml',
    ]


class TestDetectDesktop(DetectorBaseTest):

    fixture_files = [
        'tests/fixtures/upstream/desktop.yml',
    ]


class TestDetectFeedReader(DetectorBaseTest):

    fixture_files = [
        'tests/fixtures/upstream/feed_reader.yml',
    ]


class TestDetectFeaturePhone(DetectorBaseTest):

    fixture_files = [
        'tests/fixtures/upstream/feature_phone.yml',
    ]


class TestDetectMediaPlayer(DetectorBaseTest):

    fixture_files = [
        'tests/fixtures/upstream/mediaplayer.yml',
    ]


class TestDetectMobileApps(DetectorBaseTest):

    fixture_files = [
        'tests/fixtures/upstream/mobile_apps.yml',
    ]


class TestDetectSmartPhone(DetectorBaseTest):

    fixture_files = [
        'tests/fixtures/upstream/smartphone.yml',
    ]


class TestDetectSmartPhone1(DetectorBaseTest):

    fixture_files = [
        'tests/fixtures/upstream/smartphone-1.yml',
    ]


class TestDetectSmartPhone2(DetectorBaseTest):

    fixture_files = [
        'tests/fixtures/upstream/smartphone-2.yml',
    ]


class TestDetectSmartPhone3(DetectorBaseTest):

    fixture_files = [
        'tests/fixtures/upstream/smartphone-3.yml',
    ]


class TestDetectSmartPhone4(DetectorBaseTest):

    fixture_files = [
        'tests/fixtures/upstream/smartphone-4.yml',
    ]


class TestDetectSmartPhone5(DetectorBaseTest):

    fixture_files = [
        'tests/fixtures/upstream/smartphone-5.yml',
    ]


class TestDetectTablet(DetectorBaseTest):

    fixture_files = [
        'tests/fixtures/upstream/tablet.yml',
    ]


class TestDetectTablet1(DetectorBaseTest):

    fixture_files = [
        'tests/fixtures/upstream/tablet-1.yml',
    ]


class TestDetectTablet2(DetectorBaseTest):

    fixture_files = [
        'tests/fixtures/upstream/tablet-2.yml',
    ]


class TestDetectTV(DetectorBaseTest):

    fixture_files = [
        'tests/fixtures/upstream/tv.yml',
    ]
