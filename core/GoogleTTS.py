#!/usr/bin/python

import argparse
import re
import subprocess
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from collections import namedtuple


def split_text(input_text, max_length=100):
    """
    Try to split between sentences to avoid interruptions mid-sentence.
    Failing that, split between words.
    """
    def split_text_rec(input_text, regexps, max_length=max_length):
        if len(input_text) <= max_length:
            return [input_text]

        if isinstance(regexps, str):
            regexps = [regexps]
        regexp = regexps.pop(0) if regexps else '(.{%d})' % max_length

        text_list = re.split(regexp, input_text)
        combined_text = []
        combined_text.extend(split_text_rec(text_list.pop(0), regexps, max_length))
        for val in text_list:
            current = combined_text.pop()
            concat = current + val
            if len(concat) <= max_length:
                combined_text.append(concat)
            else:
                combined_text.append(current)
                combined_text.extend(split_text_rec(val, regexps, max_length))
        return combined_text

    return split_text_rec(input_text.replace('\n', ''),
                          ['([,.|;]+)', '( )'])


audio_args = namedtuple('audio_args', ['language', 'output'])


def audio_extract(input_text='', args=None):
    if args is None:
        args = audio_args(language='en', output=open('output/output.mp3', 'wb'))
    if type(args) is dict:
        args = audio_args(
            language=args.get('language', 'en'),
            output=open(args.get('output', 'output/output.mp3'), 'wb')
        )

    combined_text = split_text(input_text)

    for idx, val in enumerate(combined_text):
        mp3url = "http://translate.google.com/translate_tts?tl=%s&q=%s&total=%s&idx=%s" % (
            args.language,
            urllib.parse.quote(val),
            len(combined_text),
            idx)
        headers = {
            "Host": "translate.google.com",
            "Referer": "http://www.gstatic.com/translate/sound_player2.swf",
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_3) "
                          "AppleWebKit/535.19 (KHTML, like Gecko) "
                          "Chrome/18.0.1025.163 Safari/535.19"
        }
        req = urllib.request.Request(mp3url, b'', headers)
        sys.stdout.write('.')
        sys.stdout.flush()
        if len(val) > 0:
            try:
                response = urllib.request.urlopen(req)
                args.output.write(response.read())
                time.sleep(.5)
            except urllib.error.URLError as e:
                print('%s' % e)
    args.output.close()
    print('Saved MP3 to %s' % args.output.name)


def text_to_speech_mp3_argparse():
    description = 'Google TTS Downloader.'
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument('-o', '--output',
                        action='store', nargs='?',
                        help='Filename to output audio to',
                        type=argparse.FileType('wb'), default='output/output.mp3')
    parser.add_argument('-l', '--language',
                        action='store', nargs='?',
                        help='Language to output text to.', default='en')
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('-f', '--file',
                       type=argparse.FileType('r'),
                       help='File to read text from.')
    group.add_argument('-s', '--string',
                       action='store', nargs='+',
                       help='A string of text to convert to speech.')
    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(1)
    return parser.parse_args()


if __name__ == "__main__":
    args = text_to_speech_mp3_argparse()
    if args.file:
        input_text = args.file.read()
    if args.string:
        input_text = ' '.join(map(str, args.string))
    audio_extract(input_text=input_text, args=args)
    subprocess.run(["mpg123", "output/output.mp3"])
