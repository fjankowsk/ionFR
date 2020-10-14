'''
Script to download publicly available TEC maps
usage:
python ftpdownload.py yyyy-mm-dd [-t type]
The positional argument gives the date of the observation
-t gives type of ionex file (codg,upcg,igsg) codg maps are default option

v0.1 Charlotte Sobey 2013 
'''

import argparse
import ftplib
import datetime
import optparse as op


def parse_args():
    parser = argparse.ArgumentParser(
            description='Download public TEC maps.',
            formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )

    parser.add_argument(
            'date',
            type=str,
            help='Date (yyyy-mm-dd).'
    )

    parser.add_argument(
            '--type', '-t',
            default='cod',
            type=str,
            choices=[
                    'cod',
                    'esa',
                    'igs',
                    'jpl',
                    'upc'
            ],
            help='Type of IONEX file.'
    )

    args = parser.parse_args()

    return args


def download(ftp, directory, file):
    ftp.cwd(directory)
    f = open(file, "wb")
    ftp.retrbinary("RETR " + file, f.write)
    f.close()


#
# MAIN
#

def main():
    args = parse_args()

    year = int(args.date.split('-')[0])
    month = int(args.date.split('-')[1])
    day = int(args.date.split('-')[2])

    dayofyear = datetime.datetime.strptime(''+str(year)+' '+str(month)+' '+str(day)+'', '%Y %m %d').timetuple().tm_yday

    if dayofyear < 10:
        dayofyear = '00' + str(dayofyear)
    if dayofyear < 100 and dayofyear >= 10:
        dayofyear = '0' + str(dayofyear)

    # output the name of the IONEX file you require
    filename = '{type}g{dayofyear}0.{twodigityear}i.Z'.format(
        type=args.type,
        dayofyear=dayofyear,
        twodigityear=str(year)[2:]
    )
    print('Filename: {0}'.format(filename))

    directory = '/pub/gps/products/ionex/{year}/{dayofyear}/'.format(
        year=year,
        dayofyear=dayofyear
    )
    print('Directory: {0}'.format(directory))

    ftp = ftplib.FTP("cddis.gsfc.nasa.gov")
    ftp.login("anonymous", "anonymous")

    # Download appropriate file via ftp
    download(ftp, directory, filename)

    print('done')


if __name__ == '__main__':
        main()
