from app.modules.multilingual import MultilingualManager

def test_detect_and_translate():
    mm = MultilingualManager(provider='indic')
    lang = mm.detect_language('Hello world')
    assert isinstance(lang, str)
    # translation with indic provider is a passthrough in placeholder
    out = mm.translate('Hello', 'hi')
    assert isinstance(out, str)
