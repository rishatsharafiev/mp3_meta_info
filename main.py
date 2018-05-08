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

        with open(out, 'w+') as write_file:
            csv_writer = csv.writer(write_file, delimiter=';', quotechar='|', quoting=csv.QUOTE_MINIMAL)
            csv_writer.writerow(['Имя файла', 'Название', 'Исполнитель', 'Жанр', 'Альбом'])

            for row in metadata:
                filename = row.get('filename', '')
                print(row)
                meta = row.get('metadata')
                name = meta.get('TIT2', '')
                singer = meta.get('TPE1', '')
                genre = meta.get('TXXX:WM/GenreID ', '')
                album = meta.get('TALB', '')

                csv_writer.writerow([filename, name, singer, genre, album])

        print('Done!!!')
    else:
        parser.print_help()

if __name__ == '__main__':
    main()
