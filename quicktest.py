from twotest.quicktest import QuickDjangoTest

if __name__ == '__main__':
    QuickDjangoTest(
        apps=("wheelcms_users",),
        installed_apps=(
            'django.contrib.sites',
            'django.contrib.messages',
            'django.contrib.staticfiles',
            'django.contrib.humanize',

            'userena',

            'south',
            'haystack',

            'wheelcms_axle',
            'wheelcms_users',

            'drole',
            'granules',
            'taggit',
            'two.ol',
            'two.bootstrap',
            'twotest',
            'wheelcms_axle.tests',

        ),
        ROOT_URLCONF="wheelcms_axle.quicktest_urls",
        ANONYMOUS_USER_ID=-1,
        HAYSTACK_SITECONF = 'wheelcms_axle.search_sites',
        HAYSTACK_SEARCH_ENGINE = 'simple',
        AUTH_PROFILE_MODULE="wheelcms_axle.WheelProfile",
        CLEANUP_MEDIA=True,
        TEST_MEDIA_ROOT="/tmp/wheelcms_axle_test",
        USE_TZ=True,
        STATIC_URL='/',
        CONTENT_LANGUAGES=(('en', 'English'), ('nl', 'Nederlands')),
        FALLBACK='en',
        LANGUAGE_CODE='en',
    )
