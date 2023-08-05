import logging

FEI_WS_USERNAME = ''
FEI_WS_PASSWORD = ''
FEI_WS_BASE_URL = 'https://data.fei.org/'
FEI_ESV3_BASE_URL = 'https://es3-api.fei.org/'
FEI_ES_BASE_URL = 'https://entry.fei.org/'
FEI_WS_USE_LOCAL_WSDL = False
FEI_WS_NORMALIZE_NAMES = True
FEI_WS_LOWER_CASE_WORDS = [
    'a', 'an', 'the', 'at', 'by', 'for', 'in', 'of', 'on', 'to', 'up', 'and', 'as', 'but', 'it',
    'or', 'nor', 'de', 'het', 'een', "'t", 'der', 'die', 'das', 'ein', 'des', 'dem', 'den', 'van',
]

FEI_WS_UPPER_CASE_ACRONYMS = [
    'SAP', 'KLM', 'VDL', 'SFN', 'LLC', 'S.A.R.L.'
]

logger = logging.getLogger('fei-ws.client')

try:
    from django.conf import settings
    FEI_WS_BASE_URL = getattr(settings, 'FEI_WS_BASE_URL', FEI_WS_BASE_URL)
    FEI_WS_USERNAME = getattr(settings, 'FEI_WS_USERNAME', FEI_WS_USERNAME)
    FEI_WS_PASSWORD = getattr(settings, 'FEI_WS_PASSWORD', FEI_WS_PASSWORD)
    FEI_ESV3_BASE_URL = getattr(settings, 'FEI_ESV3_BASE_URL', FEI_ESV3_BASE_URL)
    FEI_ES_BASE_URL = getattr(settings, 'FEI_ES_BASE_URL', FEI_ES_BASE_URL)
    FEI_WS_USE_LOCAL_WSDL = getattr(settings, 'FEI_WS_USE_LOCAL_WSDL', FEI_WS_USE_LOCAL_WSDL)
    FEI_WS_NORMALIZE_NAMES = getattr(settings, 'FEI_WS_NORMALIZE_NAMES', FEI_WS_NORMALIZE_NAMES)
    FEI_WS_UPPER_CASE_ACRONYMS = getattr(settings, 'FEI_WS_UPPER_CASE_ACRONYMS', FEI_WS_UPPER_CASE_ACRONYMS)
    FEI_WS_LOWER_CASE_WORDS = getattr(settings, 'FEI_WS_LOWER_CASE_WORDS', FEI_WS_LOWER_CASE_WORDS)
except ImportError as e:
    logger.info('Could not load django.conf')

