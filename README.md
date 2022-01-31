# Short Morse-Code

The **"Short Morse Code"** uses a simple and compacted data storage system with images,
similar to the known **"QR Code"**. The **"Short Morse Code"** is implemented using the principles
of Binary and Morse Code formating. Thus, the normal, well known / global **Morse**
and **Binary Encodings** use the same rules as the encoding process of the **Short Morse Code**.

# Reason for creation / invention

The **"Short Morse Code"** was created under the courtesy of the **Facecode.IO**, which is a
software based service from identifying users whith the use of a **_Face Scan_**.
Alternatively, The **Facecode.IO** provides another alternative for creating **Scans**, with a
**QR Code-like image** called the **Short Morse Code**. This **Encoded-Image** is designed to be used
to store **compacted, small amounts of data**, normal places of using this code could be, a **coffee mug**,
**under a branding label**, a **business card** or **a on price tag (for a modernized version of Barcodes).**

# Rules of encodings

## Colors

The **"Short Morse Code"** encodings are to be encoded unto a solid **PLAIN COLOR**, the **PLAIN COLOR** should determine the **DATA COLOR**, if **PLAIN COLOR** is white **RGB(255,255,255)**, **DATA COLOR** should be black **RGB(0,0,0)**, the opposite applies. When the end of an encoding is reached, a **RED** color is used to fill up the rest of the space to represent **NULL DATA**, also when the next encoding doesn't fit then moved to the next line.

## Code Size / Image Size

The size of the encoding will be determined by the length of tha data provided. The longer the string of data, the greater the height of the **image size**.

## Rules for data-encoding

1. In the **First Line**, the start and the end is to be encoded with the **RED (NULL DATA)**, this helps the scanner/decoder determine the orientation of the code.

2. Every single **Character** will be mapped to it's **Morse Encodings** that'll determine the sequence of the **DATA SPOTS**. A **Dash** signifies a **0** and a **Dot** signifies a **1** (equivalent to the binary-system), then a **Double Space** signifies the next **Character** of the **Data**.
