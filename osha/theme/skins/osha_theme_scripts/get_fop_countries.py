## Script (Python) "get_fop_countries"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##title=Return a list of Focal Point Countries
##parameters=

from osha.theme.config import EUROPEAN_NETWORK

countries = []
for cc_and_name, link in EUROPEAN_NETWORK:
    try:
        cc, name = cc_and_name.split(' ', 1)
    except ValueError:
        # Account for country group delimiters
        continue
    countries.append
    
    # XXX: For now only create UK, DE and DK
    if cc not in ['UK', 'DE', 'DK']:
        continue

    countries.append((name, cc))

return countries

