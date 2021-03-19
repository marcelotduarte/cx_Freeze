"""
Sample to test the 'pycountry' hook

"""

import gettext
import pycountry

print("countries:", len(pycountry.countries))
print("BR-FN", pycountry.subdivisions.get(code="BR-FN"))

name = gettext.translation("iso3166", pycountry.LOCALES_DIR, languages=["pt"])
name.install()
_ = name.gettext
print("Brazil ->", _("Brazil"))
