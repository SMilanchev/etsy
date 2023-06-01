from etsy_crawler.chrome_driver import get_driver_and_browser_versions
import settings
from etsy_crawler.proxies import delete_expiring_proxies


class IncompatibleVersionsError(Exception):
    pass


def init_project_settings():
    versions = get_driver_and_browser_versions()
    if not versions['same']:
        msg = settings.INCOMPATIBLE_CHROME_DRIVER_EXC.format_map(
            {
                'chrome_version': versions['browser'], 'chrome_driver_version': versions['driver_version']
            }
        )
        raise IncompatibleVersionsError(msg)

    delete_expiring_proxies()
