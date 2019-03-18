import os
from concurrent.futures import ThreadPoolExecutor
from threading import Lock

def process_chunk(input_file, output_file, chunk_start, chunk_end, lock):
    lines_read = 0

    with open(input_file, 'r') as in_f:
        with open(output_file, 'a') as out_f:
            read_pos = chunk_start
            while read_pos < chunk_end:
                in_f.seek(read_pos) # file.seek counts in \r\n
                line = in_f.readline()
                read_pos = in_f.tell()

                with lock:
                    out_f.write(line)

                lines_read += 1

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
    pool = ThreadPoolExecutor(10)

    input_file = './input.txt'
    output_file = './output.txt'

    threads = []
    lock = Lock()
    for chunk_start, chunk_end in chunkify(input_file, 10):
        threads.append(pool.submit(process_chunk, input_file, output_file, chunk_start, chunk_end, lock))

if __name__ == '__main__':
    main()