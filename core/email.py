from protonmail import ProtonMail
import os

proton = None

def setup():
    global proton
    proton = ProtonMail()
    proton.login(os.getenv("emailUsername"), os.getenv("emailPassword"))