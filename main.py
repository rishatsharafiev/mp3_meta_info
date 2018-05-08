# -*- coding: utf-8 -*-

import os
import csv
import argparse
import mutagen

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--path', help='Sources path')
    parser.add_argument('-o', '--out', help='Output file name without extention')
    args = parser.parse_args()

    if args.path and args.out:
        path = args.path
        files = [(f, os.path.join(path, f)) for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]
        out = args.out

        metadata = []

        for f in files:
            try:
                metadata.append({'filename': f[0], 'metadata': mutagen.File(f[1])})
            except mutagen.mp3.HeaderNotFoundError as err:
                print('ERROR: Bad file, ', err)

        metadata = [m for m in metadata if m.get('metadata')]

        with open(out, 'w', encoding='utf-8') as write_file:
            csv_writer = csv.writer(write_file, delimiter=';', quotechar='|', quoting=csv.QUOTE_MINIMAL)
            col_names = ['Имя файла', 'Название', 'Исполнитель', 'Жанр', 'Альбом', 'Композитор', 'Комментарий']
            csv_writer.writerow([i.encode('utf8').decode('utf8') for i in col_names])

            for row in metadata:
                filename = row.get('filename', '')
                meta = row.get('metadata')
                name = meta.get('TIT2', '')
                singer = meta.get('TPE1', '')
                genre = meta.get('TXXX:WM/GenreID ', '')
                album = meta.get('TALB', '')
                composer = meta.get('TCOM', '')
                comment = meta.get('COMM::rus', '')

                csv_writer.writerow([filename, name, singer, genre, album, composer, comment])

        print('Done!!!')
    else:
        parser.print_help()

if __name__ == '__main__':
    main()
