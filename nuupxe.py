#!/usr/bin/python

import argparse
import subprocess
import logging
import signal
import sys
from pathlib import Path

from serviceManager import ServiceManager

from core.irlp import Irlp
from core.voicesynthesizer import VoiceSynthesizer

from tendo import singleton

def set_exit_handler(func):
    signal.signal(signal.SIGTERM, func)

def on_exit(sig, func=None):
    print("exit handler triggered")
    sys.exit(1)

def main():
    log_dir = Path.home() / '.nuupxe'
    log_dir.mkdir(exist_ok=True)
    logging.basicConfig(
        filename=str(log_dir / 'nuupxe.log'),
        level=logging.INFO,
        format='%(asctime)s %(levelname)s %(message)s'
    )

    irlp = Irlp()
    if irlp.exists():
        irlp.forceunptt()

    parser = argparse.ArgumentParser(description='NuupXe Project, Voice Services Experimental Project')
    parser.add_argument('-m', '--module', help='Module Mode')
    parser.add_argument('-p', '--phonetic', help='Phonetic Mode')
    parser.add_argument('-s', '--server', help='Server Mode')
    parser.add_argument('-v', '--voice', help='Voice Mode')
    parser.add_argument('-d', '--dtmf', help='DMTF Code')
    args = parser.parse_args()

    if irlp.active():
        logging.info("Nodo activo, no podemos iniciar Proyecto NuupXe")
        sys.exit(0)

    experimental = ServiceManager(irlp)
    experimental.setup_synthesizer()
    voicesynthesizer = experimental.voicesynthesizerget()

    if (args.module or args.server) and experimental.enabled():
        logging.info("Proyecto NuupXe ya habilitado, no podemos iniciar otra instancia")
        sys.exit(1)

    if args.server == 'stop' and not experimental.enabled():
        voicesynthesizer.speech_it("Proyecto Nuup X e deshabilitado")
        subprocess.call('./nuupxe.sh stop', shell=True)
        sys.exit(1)

    if args.server == 'stop' and experimental.enabled():
        voicesynthesizer.speech_it("Deshabilitando Proyecto NuupXe, hasta pronto!")
        subprocess.call('./nuupxe.sh stop', shell=True)
        sys.exit(1)

    elif args.module:
        experimental.module_mode(args.module, args.dtmf)

    elif args.server == 'observer':
        experimental.modules_setup()
        experimental.observer_mode()

    elif args.server == 'scheduler':
        experimental.modules_setup()
        experimental.scheduler_mode()

    elif args.server == 'writing':
        experimental.modules_setup()
        experimental.writing_mode()

    elif args.dtmf:
        logging.info(args.dtmf)
        if args.dtmf.startswith('PS'):
            module = experimental.dtmf_setup(args.dtmf)
            experimental.module_mode(module, args.dtmf)
        elif args.dtmf.startswith('SS') and len(args.dtmf) == 4:
            experimental.module_mode('voicemailer', args.dtmf)
        elif len(args.dtmf) > 10:
            experimental.module_mode('aprstt', args.dtmf)

    elif args.voice:
        experimental.voice_mode(args.voice)

    elif args.phonetic:
        experimental.phonetic_mode(args.phonetic)

    experimental.disable()

if __name__ == "__main__":
    main()

# End of File
