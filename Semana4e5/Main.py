import bz2
import lzma
import os
import time

import pyppmd

import HuffmanCodec

import LZW
from Semana4e5 import Deflate


def huffman_encoding(data):
    start = time.perf_counter()
    encoded_text = HuffmanCodec.encode(data)
    compressed_data = bytearray()
    for i in range(0, len(encoded_text), 8):
        compressed_data.append(int(encoded_text[i:i + 8], 2))
    print("\tCompression Huffman: ", round(time.perf_counter() - start, 5), "seg")
    start = time.perf_counter()
    decompressed_data = HuffmanCodec.decode(encoded_text)
    print("\tDecompression Huffman: ", round(time.perf_counter() - start, 5), "seg")
    print("\tHuffman:", decompressed_data == data)  # True
    return compressed_data, decompressed_data


def bzip(data):
    start = time.perf_counter()
    compressed_data = bz2.compress(data.encode())
    print("\tCompression Bzip2: ", round(time.perf_counter() - start, 5), "seg")
    start = time.perf_counter()
    decompressed_data = bz2.decompress(compressed_data)
    print("\tDecompression Bzip2: ", round(time.perf_counter() - start, 5), "seg")
    str_decompressed_data = decompressed_data.decode()
    # print(str_decompressed_data)
    print("\tBzip2:", str_decompressed_data == data)  # True
    return compressed_data, decompressed_data


def lzma_encoding(data):
    start = time.perf_counter()
    compressed_data = lzma.compress(str.encode(data))
    print("\tCompression LZMA: ", round(time.perf_counter() - start, 5), "seg")
    start = time.perf_counter()
    decompressed_data = lzma.decompress(compressed_data)
    print("\tDecompression LZMA: ", round(time.perf_counter() - start, 5), "seg")
    str_decompressed_data = decompressed_data.decode()
    # print(str_decompressed_data)
    print("\tLZMA:", str_decompressed_data == data)  # True
    return compressed_data, decompressed_data


def lzw_encoding(data):
    start = time.perf_counter()
    compressed_data = LZW.compress(data)
    print("\tCompression LZW: ", round(time.perf_counter() - start, 5), "seg")
    start = time.perf_counter()
    decompressed_data = LZW.decompress(compressed_data)
    print("\tDecompression LZW: ", round(time.perf_counter() - start, 5), "seg")
    print("\tLZW:", decompressed_data == data)  # True
    # print(compressed_data)
    new = ""
    for i in compressed_data:
        new += str(i)
    return new.encode(), decompressed_data


def ppm_encoding(data):
    start = time.perf_counter()
    compressed_data = pyppmd.compress(data.encode())
    print("\tCompression PPM: ", round(time.perf_counter() - start, 5), "seg")
    start = time.perf_counter()
    decompressed_data = pyppmd.decompress(compressed_data).decode()
    print("\tDecompression PPM: ", round(time.perf_counter() - start, 5), "seg")
    print("\tPPM:", decompressed_data == data)  # True
    return compressed_data, decompressed_data


def deflate_encoding(data):
    start = time.perf_counter()
    compressed_data = Deflate.deflate(data.encode())
    print("\tCompression Deflate: ", round(time.perf_counter() - start, 5), "seg")
    start = time.perf_counter()
    decompressed_data = Deflate.inflate(compressed_data)
    print("\tDecompression Deflate: ", round(time.perf_counter() - start, 5), "seg")
    str_decompressed_data = decompressed_data.decode()
    print("\tDeflate:", str_decompressed_data == data)  # True
    return compressed_data, decompressed_data


def get_ratio(original_size, compressed):

    compressed_size = os.path.getsize(compressed)
    compression_percent = round(100 - compressed_size / original_size * 100, 2)
    print(f"\tTamanho do comprimido: {compressed_size} bytes / "
          f"Ratio de compressão: {compression_percent}%")


data_type = [".txt", ".csv", ".js", ".txt"]
filenames = ["bible", "finance", "jquery-3.6.0", "random"]
compression_type = [".bzip2", ".lzma", ".lzw", ".huffman", ".ppm", ".deflate"]
for i in range(len(filenames)):
    j = 0
    read_path = "..\dataset\\" + filenames[i] + data_type[i]
    original_size = os.path.getsize(read_path)
    print(filenames[i] + data_type[i] + " (Tamanho: " + str(original_size) + " bytes):")
    with open(read_path, "r") as file:
        data = file.read()
        for j in range(len(compression_type)):
            write_path = "..\compressed_dataset\\" + filenames[i] + compression_type[j]
            with open(write_path, "wb") as write_file:
                if j == 0:
                    compressed_data_bzip, decompressed_data_bzip = bzip(data)
                    write_file.write(compressed_data_bzip)
                elif j == 1:
                    compressed_data_lzma, decompressed_data_lzma = lzma_encoding(data)
                    write_file.write(compressed_data_lzma)
                elif j == 2:
                    compressed_data_lzw, decompressed_data_lzw = lzw_encoding(data)
                    write_file.write(compressed_data_lzw)
                elif j == 3:
                    compressed_data_huffman, decompressed_data_huffman = huffman_encoding(data)
                    write_file.write(compressed_data_huffman)
                elif j == 4:
                    compressed_data_ppm, decompressed_data_ppm = ppm_encoding(data)
                    write_file.write(compressed_data_ppm)
                elif j == 5:
                    compressed_data_deflate, decompressed_data_deflate = deflate_encoding(data)
                    write_file.write(compressed_data_deflate)
            get_ratio(original_size, write_path)
            print()
