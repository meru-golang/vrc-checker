import vrcpy
import asyncio
import subprocess
import re
from config import lo, fa

loop = asyncio.get_event_loop()
cl = vrcpy.Client(loop=loop)

#2FA

Tfa = ['oathtool', '--totp', '--base32', fa.code]
Tfacode = re.findall(r'\d+', subprocess.check_output(Tfa).decode('utf-8'))


async def main():
    await cl.login(
        username= lo.user,
        password= lo.pw,
        mfa= Tfacode
    )

    try:
        # Start the ws event loop
        await cl.start()
    except KeyboardInterrupt:
        await cl.logout()

@cl.event
async def on_connect():
    print("WS connected!")


@cl.event
async def on_ready():
    print("Cache ready!")


@cl.event
async def on_disconnect():
    print("WS disconnected!")

loop.run_until_complete(main())