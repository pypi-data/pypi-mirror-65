#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Snoopdroid
#
# Copyright (C) 2019 Claudio Guarnieri <https://nex.sx>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

import os
import sys
import argparse
import datetime

from .ui import info, logo
from .acquisition import Acquisition
from .virustotal import virustotal_lookup
from .koodous import koodous_lookup

def main():
    parser = argparse.ArgumentParser(description="Extract information from Android device")
    parser.add_argument("--storage", default=os.getcwd(), help="Specify a different base folder to store the acquisition")
    parser.add_argument("--limit", default=None, help="Set a limit to the number of packages to extract (mainly for debug purposes)")
    parser.add_argument("--all-apks", action="store_true", help="Extract all packages installed on the phone, even those marked as safe")
    parser.add_argument("--virustotal", action="store_true", help="Check packages on VirusTotal")
    parser.add_argument("--koodous", action="store_true", help="Check packages on Koodous")
    parser.add_argument("--all-checks", action="store_true", help="Run all available checks")
    parser.add_argument("--from-file", default=None, help="Instead of acquiring from phone, load an existing packages.json file for lookups (mainly for debug purposes)")
    args = parser.parse_args()

    logo()

    try:
        if args.from_file:
            acq = Acquisition.fromJSON(args.from_file)
        else:
            # TODO: Need to come up with a better folder name.
            acq_folder = datetime.datetime.now().isoformat().split(".")[0].replace(":", "")
            storage_folder = os.path.join(args.storage, acq_folder)

            acq = Acquisition(storage_folder=storage_folder,
                all_apks=args.all_apks, limit=args.limit)
            acq.run()
        
        packages = acq.packages

        if len(packages) == 0:
            return

        if args.virustotal or args.all_checks:
            virustotal_lookup(packages)

        print("")

        if args.koodous or args.all_checks:
            koodous_lookup(packages)
    except KeyboardInterrupt:
        print("")
        sys.exit(-1)

if __name__ == "__main__":
    main()
