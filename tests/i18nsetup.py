import gettext


def setup_translations(testcase):
    current_lang = testcase.data_layer.get_setting("language.current").split('-')[0]
    testcase.UTILS.reporting.log_to_file("Current language: [{}]".format(current_lang))
    translation = gettext.translation('default', 'tests/locale', languages=[current_lang])
    translation.install(unicode=True)
    return translation.ugettext
