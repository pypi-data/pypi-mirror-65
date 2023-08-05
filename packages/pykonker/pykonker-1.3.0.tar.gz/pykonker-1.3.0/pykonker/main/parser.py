"""
THIS SPECIFIC FILE IS DISTRIBUTED UNDER THE UNLICENSE: http://unlicense.org.

THIS MEANS YOU CAN USE THIS CODE EXAMPLE TO KICKSTART A PROJECT YOUR OWN.
AFTER YOU CREATED YOUR OWN ORIGINAL WORK, YOU CAN REPLACE THIS HEADER :)
"""

import sys
import argparse

from .api import Client


def main():
    """This function is called when run as python3 -m ${MODULE}
    Parse any additional arguments and call required module functions."""

    if sys.argv:
        # called through CLI
        module_name = __loader__.name.split('.')[0]
        parser = argparse.ArgumentParser(
            prog=module_name,
            description="Konker REST API for python: " + module_name,
        )

        parser.add_argument('-u', '--username', action='store', nargs=1, required=False, type=str,
                            default=['john@acme.com'],
                            help="username")
        parser.add_argument('-p', '--password', action='store', nargs=1, required=False, type=str,
                            default=['tiger'],
                            help="password")

        args = parser.parse_args(sys.argv[1:])

        konker = Client()
        konker.login(username=args.username[0], password=args.password[0])

        applications = konker.get_applications()

        if applications:

            print('CONNECTED TO KONKER PLATFORM')

            for application in applications:
                print('>> GET INFORMATION FOR APPLICATION {}'.format(application['name']))
                devices = konker.get_all_devices_for_application(application['name'])
                if devices:
                    print('\tDEVICES for "{}" are:'.format(application['name']))
                    print('\t{:34}\t{:20}\t{}\t{}\t{}'.format(
                        'guid',
                        'name',
                        'location',
                        'active',
                        'description'))
                    for device in devices:
                        print('\t\t{:34}\t{:20}\t{}\t{}\t{}'.format(
                            device['guid'],
                            device['name'],
                            device['locationName'],
                            device['active'],
                            device['description']))
                else:
                    print('\tno devices found for "{}"'.format(application))

                locations = konker.get_locations_for_application(application['name'])
                print('\tLOCATIONS FOR {}'.format(application['name']))
                if locations:
                    for location in locations:
                        print('\t\t{}\t{}\t'.format(location['name'], location['guid']))


        if konker.check_connection():
            sys.stdout.write('connected to Konker platform\n')
        else:
            return 1

    return 0
