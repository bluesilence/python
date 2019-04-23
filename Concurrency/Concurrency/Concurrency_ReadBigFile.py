import os
from threading import Lock
from multiprocessing.dummy import Pool

def process_chunk(input_file, output_file, chunk_start, chunk_end, lock):
    lines_read = 0

    with open(input_file, 'r') as in_f:
        with open(output_file, 'a') as out_f:
            read_pos = chunk_start
            while read_pos < chunk_end:
                in_f.seek(read_pos) # file.seek counts in \r\n
                line = in_f.readline()
                new_read_pos = in_f.tell()
                if read_pos == new_read_pos: # No line to read
                    break

                with lock:
                    out_f.write(line)

                lines_read += 1
                read_pos = new_read_pos
                print('read_pos: {}, chunk_end: {}'.format(read_pos, chunk_end))

    return lines_read

def chunkify(file_name, chunk_size):
    file_end = os.path.getsize(file_name)

    with open(file_name, 'r') as f:
        chunk_end = f.tell()

        while chunk_end <= file_end:
            chunk_start = chunk_end
            f.seek(chunk_start + chunk_size)
            f.readline() # Move file pointer to the beginning of next line
            chunk_end = f.tell()

            yield chunk_start, chunk_end

def main():
    input_file = './input.txt'
    output_file = './output.txt'

    pool = Pool(1)
    lock = Lock()
    pool.starmap(process_chunk, [ ( input_file, output_file, chunk_start, chunk_end, lock ) for chunk_start, chunk_end in chunkify(input_file, 10) ])

    pool.close()
    pool.join()

if __name__ == '__main__':
    main()