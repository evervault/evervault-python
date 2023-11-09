---
"evervault-python": minor
---

The `encrypt` function has been enhanced to accept an optional Data Role. This role, where specified, is associated with the data upon encryption. Data Roles can be created in the Evervault Dashboard (Data Roles section) and provide a mechanism for setting rules that dictate how and when data, tagged with that role, can be decrypted.

evervault.encrypt("hello world!", "allow-all");