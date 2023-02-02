import evervault

evervault.init(
    "NTI5:3s2tleqTrvlbkzzWMFWG1Rvh7vzITeDMWzQPjN1nETlXm5oYFFMsjPXQNzVfzadOx",
    curve=evervault.Curves.SECP256R1,
)

with open("pyproject.toml", mode="rb") as zip_file:
    contents = zip_file.read()
    print(type(contents))
    print(contents[:20])
    encrypted = evervault.encrypt(contents)
    encrypted_string = evervault.encrypt("this was a triumph")
    print(encrypted_string)
    print(len(encrypted))
    print(encrypted[:70])
    f = open("pyproject.bin", "wb")
    f.write(encrypted)
    f.close()
