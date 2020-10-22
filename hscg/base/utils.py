import os
import shutil
import datetime

def str_to_hump(text):
    """ Underline to hump code """
    arr = filter(None, text.lower().split('_'))
    res = ''
    for i in arr:
        res =  res + i[0].upper() + i[1:]
    return res


def split_fasta_by_size(fasta_file, output_dir="chunk_output"):
    """
    [ERROR] Input chunk_output/CorrectHQ.split1.fa needs to end with .fasta or .fastq! Exiting
    """
    fasta_dir, fasta_filename = os.path.split(fasta_file)
    fasta_prefix, fasta_suffix = os.path.splitext(fasta_filename)

    if fasta_suffix in ('.fastq', '.fasta'):
        specific_suffix = fasta_suffix
    elif fasta_suffix == '.fa':
        specific_suffix = '.fasta'
    elif fasta_suffix == '.fq':
        specific_suffix = '.fastq'
    else:
        specific_suffix = fasta_suffix

    n = 1
    current_dir = os.getcwd()

    if os.path.exists(output_dir):
        shutil.rmtree(output_dir)
    os.makedirs(output_dir, exist_ok=True)
    os.chdir(output_dir)

    output_mid = fasta_prefix + ".split" + str(n) + specific_suffix
    output_wp = open(output_mid, "a")

    with open(fasta_file, "r") as fp:
        for line in fp:
            if line.startswith(">"):
                size = os.stat(output_mid).st_size
                if size > 1000000000:  # 1GB
                    n += 1
                    output_wp.close()
                    output_mid = fasta_prefix + ".split" + str(n) + specific_suffix
                    output_wp = open(output_mid, "a")
            output_wp.write(str(line))

    os.chdir(current_dir)
    return output_dir

from time import time


# def time_costing(func):
#     def core():
#         begin_time = datetime.datetime.now()
#         func()
#         end_time = datetime.datetime.now()
#         print('Time elapsing:', end_time - begin_time)
#     return core


def record_time_decorator(func):
    def core():
        begin_time = datetime.datetime.now()
        func()
        end_time = datetime.datetime.now()
        print('Time elapsing:', end_time - begin_time)
    return core


def record_log():
    pass






#
