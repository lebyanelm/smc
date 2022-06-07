"""
'Short Morse Code' (TM) decoder script.

Under the courtesy of the Facecode.IO
"""

import segno

qrcode = segno.make_qr("Myself at 21st", error="L")
qrcode.show(dark='darkblue', light='#eee')
