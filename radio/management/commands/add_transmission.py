import os
import sys
import datetime
import json
import pytz

from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from django.utils import timezone
from django.utils.dateparse import parse_datetime
from radio.models import *

class Command(BaseCommand):
    help = 'Insert radio transmisison info'

    def add_arguments(self, parser):
        parser.add_argument('json_name')
        parser.add_argument(
            '--vhf',
            action='store_true',
            dest='vhf',
            default=False,
            help='Add a VHF tranmission',
        )
        parser.add_argument(
            '--source',
            type=int,
            #action='store_true',
            #dest='source',
            default=-1,
            help='Set the source of the transmission',
        )
        parser.add_argument(
            '--system',
            type=int,
            default=-1,
            help='Set the radio system of the transmission',
        )
        parser.add_argument(
            '--web_url',
            default='/',
            help='Set the web folder the audio file is in',
        )
        parser.add_argument(
            '--verbose',
            action='store_true',
            dest='verbose',
            default=False,
            help='Verbose output',
        )

    def handle(self, *args, **options):
        add_new_trans(options)

def talkgroup(tg_dec,system):
    try:
        tg = TalkGroup.objects.get(dec_id=tg_dec, system=system)
    except TalkGroup.DoesNotExist:
        name = '#{}'.format(tg_dec)
        tg = TalkGroup.objects.create(dec_id=tg_dec, system=system, alpha_tag=name, description='TalkGroup {}'.format(name))
    return tg

def add_new_trans(options):

    full_file_name = options['json_name']
    file_name = os.path.basename(full_file_name)
    vhf = options['vhf']
    source_opt = options['source']
    system_opt = options['system']
    web_url_opt = options['web_url']
    verbose = options['verbose']
    if verbose:
        print('You passed in {}'.format(options['json_name']))
    source_default = False
    if source_opt == -1:
        source_opt = 1
        source_default = True
    if vhf:
        tg_dec = file_name.split('_', 1)[0]
        # 90002_cnf_20160903_015052.mp3
        file_dt = file_name.split('_')[2]
        file_time = file_name.split('_')[3].split('.')[0]
        full_dt = "{}{}".format(file_dt,file_time)
        epoc_ts = datetime.datetime.strptime(full_dt, "%Y%m%d%H%M%S").timestamp()
        # XXX - ARGGGGGGGGGGGGG FIX THIS ASAP, convert to the time
        epoc_ts = epoc_ts - 25200
        #pytz.timezone('UTC').localize(new_time, is_dst=None)
        #epoc_ts = new_time.timestamp()
        if verbose:
            print("Time {} is {}".format(full_dt,epoc_ts))
        #epoc_ts.replace(tzinfo=pytz.UTC)
    else:
        tg_dec = file_name.split('-', 1)[0]
        epoc_ts = file_name.split('-', 2)[1].split('_', 1)[0]
    if verbose:
        print("TalkGroup", tg_dec)
    if vhf:
        freq = 0
    else:
        freq = file_name.split('_', 2)[1]

    dt = datetime.datetime.fromtimestamp(int(epoc_ts), pytz.UTC)
    #if vhf:
    #dt.replace(tzinfo=pytz.UTC)
    
    source = Source.objects.get(pk=source_opt)

    t = Transmission( start_datetime = dt,
                     audio_file = file_name,
                     talkgroup = tg_dec,
                     freq = int(float(freq)),
                     emergency = False,
                     source = source,
                     audio_file_url_path = web_url_opt,
                   )
    system = 1
    if not vhf:
        # First try and open file with given path, if not fail back
        # to old hardcoded audio_files path
        json_file = '{}.json'.format(full_file_name)
        if not os.path.exists(json_file):
            json_file = 'audio_files/{}.json'.format(file_name)
        with open(json_file) as data_file:
            data = json.load(data_file)
        if data:
            if data['emergency']:
                t.emergency = True
            count = 0
            t.play_length = data.get('play_length',1)
            system = data.get('system', 1)
            if system_opt >= 0: 
                system = system_opt # Command line overrides json
            t.system = System.objects.get(pk=system)
            t.talkgroup_info = talkgroup(tg_dec, t.system)
            if source_default:
                json_source = data.get('source', 1)
                if(json_source > 0):
                    # No need to re add source if its still 0
                    source = Source.objects.get(pk=data['source'])
                    t.source = source
            t.save()
            for unit in data['srcList']:
                try:
                    trans_unit = unit['src']
                except TypeError:
                    trans_unit = unit
                u,created = Unit.objects.get_or_create(dec_id=trans_unit,system=t.system)
                tu = TranmissionUnit.objects.create(transmission=t, unit=u, order=count)
                count=count+1
    else:
        if system_opt >= 0:
            system = system_opt # Command line overrides json
        t.system = System.objects.get(pk=system)
        t.talkgroup_info = talkgroup(tg_dec, t.system)
        t.save()
