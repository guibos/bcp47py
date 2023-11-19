import os.path


class Base:
    _LANGUAGE_SUBTAG_REGISTRY_ENCODING = 'utf-8'
    _LANGUAGE_SUBTAG_REGISTRY_FILE_PATH = os.path.join(os.path.dirname(__file__), '../data', 'language-subtag-registry',
                                                       'language-subtag-registry')
