import csv
import getopt
import os
import sys

names_to_geo_ids = {
    'Khotang': 'dstrct-13', 'Rautahat': 'dstrct-31', 'Dailekh': 'dstrct-63',
    'Ramechhap': 'dstrct-18', 'Banke': 'dstrct-65', 'Sarlahi': 'dstrct-22',
    'Myagdi': 'dstrct-49', 'Sindhuli': 'dstrct-19', 'Gulmi': 'dstrct-45',
    'Saptari': 'dstrct-15', 'Parsa': 'dstrct-33', 'Rasuwa': 'dstrct-28',
    'Salyan': 'dstrct-61', 'Rupandehi': 'dstrct-44', 'Mugu': 'dstrct-53',
    'Bajura': 'dstrct-67', 'Dhankuta': 'dstrct-07', 'Dang': 'dstrct-60',
    'Kathmandu': 'dstrct-27', 'Sankhuwasabha': 'dstrct-05',
    'Solukhumbu': 'dstrct-11', 'Doti': 'dstrct-70',
    'Arghakhanchi': 'dstrct-46', 'Baglung': 'dstrct-51',
    'Bhojpur': 'dstrct-06', 'Dhanusha': 'dstrct-20', 'Panchthar': 'dstrct-02',
    'Kalikot': 'dstrct-55', 'Tahanun': 'dstrct-38', 'Bardiya': 'dstrct-66',
    'Lalitpur': 'dstrct-26', 'Humla': 'dstrct-56', 'Kaski': 'dstrct-40',
    'Syangja': 'dstrct-41', 'Dadeldhura': 'dstrct-74', 'Dhading': 'dstrct-30',
    'Pyuthan': 'dstrct-59', 'Taplejung': 'dstrct-01', 'Rolpa': 'dstrct-58',
    'Bhaktapur': 'dstrct-25', 'Lamjung': 'dstrct-37', 'Sunsari': 'dstrct-10',
    'Kapilbastu': 'dstrct-47', 'Kanchanpur': 'dstrct-75',
    'Kailali': 'dstrct-71', 'Sindhupalchowk': 'dstrct-23',
    'Jumla': 'dstrct-54', 'Morang': 'dstrct-09', 'Dolpa': 'dstrct-52',
    'Surkhet': 'dstrct-64', 'Siraha': 'dstrct-16', 'Nawalparasi': 'dstrct-42',
    'Chitwan': 'dstrct-35', 'Jhapa': 'dstrct-04', 'Baitadi': 'dstrct-73',
    'Achham': 'dstrct-68', 'Makawanpur': 'dstrct-34', 'Bara': 'dstrct-32',
    'Okhaldhunga': 'dstrct-12', 'Rukum': 'dstrct-57', 'Darchula': 'dstrct-72',
    'Tehrathum': 'dstrct-08', 'Nuwakot': 'dstrct-29', 'Bajhang': 'dstrct-69',
    'Mustang': 'dstrct-48', 'Parbat': 'dstrct-50', 'Udayapur': 'dstrct-14',
    'Illam': 'dstrct-03', 'Manang': 'dstrct-39', 'Palpa': 'dstrct-43',
    'Dolakha': 'dstrct-17', 'Jajarkot': 'dstrct-62', 'Mahottari': 'dstrct-21',
    'Kavre': 'dstrct-24', 'Gorkha': 'dstrct-36'
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

    district_dict = {}
    for cookingfile in csvfilenames:
        district_geoid = names_to_geo_ids[cookingfile.split('/')[-2]]
        with open(cookingfile, 'r') as cooking:
            all = cooking.readlines()
            headers = all[0].split(',')[1:]
            totals = all[len(all) - 1].split(',')[1:]
            district_vals = {}

            for idx, header in enumerate(headers):
                district_vals[header.strip(' \t\n\r')] = \
                    int(totals[idx].strip(' \t\n\r'))

            district_dict[district_geoid] = district_vals

    all_rows = []
    national_totals = {}
    for key, value in district_dict.items():
        for fuel in value.keys():
            if fuel == 'LPG':
                fuel_name = fuel
            else:
                fuel_name = fuel.lower().replace('_', ' ').capitalize()

            all_rows.append({
                'geo_level': 'district',
                'geo_code': key,
                'main type of cooking fuel': fuel_name,
                'total': value[fuel]
            })
            if fuel_name in national_totals:
                national_totals[fuel_name] = national_totals[fuel_name] \
                                                + value[fuel]
            else:
                national_totals[fuel_name] = value[fuel]

    for key, value in national_totals.items():
        all_rows.append({
            'geo_level': 'country',
            'geo_code': 'NP',
            'main type of cooking fuel': key,
            'total': value
        })

    with open(outputfile, 'w') as csvout:
        fieldnames = all_rows[0].keys()
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
