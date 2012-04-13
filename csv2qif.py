#!/usr/bin/env python
# -*- coding: iso-8859-15 -*-
# -*- Mode: Python; py-ident-offset: 4 -*-
# vim:ts=4:sw=4:et
'''
CSV2OFX
=======

This script converts the CSV provided by CGD (CAIXA GERAL DE DEPOSITOS)
home banking system to a QIF format so the it can be imported to personal
finance systems.

'''
__revision__ = '$Rev$'[6:-2]

import sys
import csv
from datetime import datetime

def read_csv(statement_file):
    ''' reads a csv statement file and returns the converted data
    '''
    csv_reader = csv.reader(statement_file, delimiter=';')
    data = []
    for row in csv_reader:
        try:
            d_mov, d_val, desc, credit, debit = row[:5]
            d_mov = datetime.strptime(d_mov, '%d-%m-%Y')
            credit = credit.replace('.', '')
            credit = credit.replace(',', '.')
            if credit:
                credit = float(credit)
            else:
                credit = 0
            debit = debit.replace('.', '')
            debit = debit.replace(',', '.')
            if debit:
                debit = float(debit)
            else:
                debit = 0
            data.append([d_mov, desc, credit, debit, ])
        except Exception, e:
            continue
    return data

def convert_qif(data, outputfile):
    ''' writes the extracted data into a QIF file

        Example:
        !Type:Bank
        D26/08/09
        T-20
        PLEVANTAMENTO
        ^
    '''
    for row in data:
        outputfile.write('!Type:Bank\n')
        outputfile.write('D%s\n' % (row[0].strftime("%d/%m/%Y"), ))
        if row[2]:
            outputfile.write('T-%s\n' % (str(row[2]), ))
        else:
            outputfile.write('T%s\n' % (str(row[3]), ))
        outputfile.write('P%s\n' % (row[1], ))
        outputfile.write('^\n')

def main(statement_file):
    ''' driver function
    '''

    try:
        statement = open(statement_file)
    except IOError, error:
        print 'could not open statement file: %s\n\t%s' % \
            (statement_file, str(error), )
        sys.exit(1)

    try:
        output = file(statement.name.replace('csv', 'qif'), 'w')
    except IOError, error:
        print 'could not open output file: %s\n\t%s' % \
            (statement.name.replace('csv', 'qif'), str(error), )

    data = read_csv(statement)
    convert_qif(data, output)
    print 'converted data saved to %s file' % \
            (statement.name.replace('csv', 'qif'), )

    statement.close()
    output.close()

if __name__ == '__main__':

    if len(sys.argv) < 2:
        print './cvs2qif.py statement.csv'
        sys.exit(1)
    else:
        main(sys.argv[1])
