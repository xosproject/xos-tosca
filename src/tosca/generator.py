# Copyright 2017-present Open Networking Foundation
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from __future__ import absolute_import

import os

from xosapi.xos_grpc_client import Empty
from xosgenx.generator import XOSProcessor, XOSProcessorArgs

from multistructlog import create_logger
from xosconfig import Config

from .default import TOSCA_DEFS_DIR, TOSCA_KEYS_DIR

log = create_logger(Config().get("logging"))


current_dir = os.path.dirname(os.path.realpath(__file__))


class TOSCA_Generator:
    def clean(self, dir=TOSCA_DEFS_DIR):
        filesToRemove = [f for f in os.listdir(dir)]
        for f in filesToRemove:
            if not f.startswith("."):
                os.remove(dir + "/" + f)

    def clean_keys(self, dir=TOSCA_KEYS_DIR):
        keys_fn = os.path.join(dir, "KEYS.py")
        if os.path.exists(keys_fn):
            os.remove(keys_fn)

    def generate(self, client):
        log.info("[XOS-TOSCA] Generating TOSCA")

        try:
            xproto = client.utility.GetXproto(Empty())
            args = XOSProcessorArgs(
                output=TOSCA_DEFS_DIR,
                inputs=str(xproto.xproto),
                target=os.path.join(current_dir, "xtarget/tosca.xtarget"),
                write_to_file="target",
            )
            XOSProcessor.process(args)
            log.info("[XOS-TOSCA] Recipes generated in %s" % args.output)
        except Exception:
            log.exception("[XOS-TOSCA] Failed to generate TOSCA")

        try:
            xproto = client.utility.GetXproto(Empty())
            args = XOSProcessorArgs(
                output=TOSCA_KEYS_DIR,
                inputs=str(xproto.xproto),
                target=os.path.join(current_dir, "xtarget/tosca_keys.xtarget"),
                write_to_file="single",
                dest_file="KEYS.py",
            )
            XOSProcessor.process(args)
            log.info("[XOS-TOSCA] TOSCA Keys generated in %s" % args.output)
        except Exception:
            log.exception("[XOS-TOSCA] Failed to generate TOSCA Keys")
