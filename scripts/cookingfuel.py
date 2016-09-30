import csv
import getopt
import os
import sys

names_to_geo_ids = {
    'Khotang': '13', 'Rautahat': '31', 'Dailekh': '63',
    'Ramechhap': '18', 'Banke': '65', 'Sarlahi': '22',
    'Myagdi': '49', 'Sindhuli': '19', 'Gulmi': '45',
    'Saptari': '15', 'Parsa': '33', 'Rasuwa': '28',
    'Salyan': '61', 'Rupandehi': '44', 'Mugu': '53',
    'Bajura': '67', 'Dhankuta': '07', 'Dang': '60',
    'Kathmandu': '27', 'Sankhuwasabha': '05',
    'Solukhumbu': '11', 'Doti': '70',
    'Arghakhanchi': '46', 'Baglung': '51',
    'Bhojpur': '06', 'Dhanusha': '20', 'Panchthar': '02',
    'Kalikot': '55', 'Tahanun': '38', 'Bardiya': '66',
    'Lalitpur': '26', 'Humla': '56', 'Kaski': '40',
    'Syangja': '41', 'Dadeldhura': '74', 'Dhading': '30',
    'Pyuthan': '59', 'Taplejung': '01', 'Rolpa': '58',
    'Bhaktapur': '25', 'Lamjung': '37', 'Sunsari': '10',
    'Kapilbastu': '47', 'Kanchanpur': '75',
    'Kailali': '71', 'Sindhupalchowk': '23',
    'Jumla': '54', 'Morang': '09', 'Dolpa': '52',
    'Surkhet': '64', 'Siraha': '16', 'Nawalparasi': '42',
    'Chitwan': '35', 'Jhapa': '04', 'Baitadi': '73',
    'Achham': '68', 'Makawanpur': '34', 'Bara': '32',
    'Okhaldhunga': '12', 'Rukum': '57', 'Darchula': '72',
    'Tehrathum': '08', 'Nuwakot': '29', 'Bajhang': '69',
    'Mustang': '48', 'Parbat': '50', 'Udayapur': '14',
    'Illam': '03', 'Manang': '39', 'Palpa': '43',
    'Dolakha': '17', 'Jajarkot': '62', 'Mahottari': '21',
    'Kavre': '24', 'Gorkha': '36'
}
    

def cookingfuelcsv(districtsdir, outputfile):

    def get_immediate_subdirectories(a_dir):
        return [name for name in os.listdir(a_dir)
                if os.path.isdir(os.path.join(a_dir, name))]

    def build_csv_location(districtname):
        return '{}/{}/{}'.format(districtsdir,
                                 districtname,
                                 'COOKING_FUEL.csv')

    csvfilenames = list(map(build_csv_location,
                            get_immediate_subdirectories(districtsdir)))

    all_rows = []
    national_totals = {}
    for cookingfile in csvfilenames:
        district_geoid = names_to_geo_ids[cookingfile.split('/')[-2]]
        with open(cookingfile, 'r') as cooking:
            all = cooking.readlines()
            headers = all[0].split(',')[1:]
            totals = all[len(all) - 1].split(',')[1:]

            for idx, header in enumerate(headers):
                fuel_name = header.strip(' \t\n\r')
                district_total = int(totals[idx].strip(' \t\n\r'))
                all_rows.append({
                    'geo_level': 'district',
                    'geo_code': district_geoid,
                    'main type of cooking fuel': fuel_name,
                    'total': district_total
                })
                if fuel_name in national_totals:
                    national_totals[fuel_name] += district_total
                else:
                    national_totals[fuel_name] = district_total

    for key, value in national_totals.items():
        all_rows.append({
            'geo_level': 'country',
            'geo_code': 'NP',
            'main type of cooking fuel': key,
            'total': value
        })

    with open(outputfile, 'w') as csvout:
        fieldnames = ['geo_code', 'geo_level',
                      'main type of cooking fuel', 'total']
        writer = csv.DictWriter(csvout, fieldnames=fieldnames)
        writer.writeheader()
        for row in all_rows:
            writer.writerow(row)

    print('Done!')


def main(args):
    indir = ''
    outputcsv = ''
    try:
        opts, args = getopt.getopt(args, 'hi:o:', ['indir=', 'outputcsv='])
    except getopt.GetoptError:
        print('python districtnames.py -i <indir> -o <outputcsv>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('python districtnames.py -i <indir>  -o <outputcsv>')
            sys.exit()
        elif opt in ('-i', '--indir'):
            indir = arg
        elif opt in ('-o', '--outputcsv'):
            outputcsv = arg

    cookingfuelcsv(indir, outputcsv)


if __name__ == '__main__':
    main(sys.argv[1:])
