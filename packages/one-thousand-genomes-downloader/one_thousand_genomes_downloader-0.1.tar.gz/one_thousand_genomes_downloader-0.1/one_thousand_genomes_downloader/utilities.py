import os
import sys
from ftplib import FTP
from tqdm import tqdm
from one_thousand_genomes_downloader.constants import BASE_PATH, ALIGNMENT_DIR, FTP_PATH, FORMATS, OUTPUT_FOLDER, \
    DEFAULT_FILE_FORMAT, EXOME_ALIGNMENT_DIR


def get_sample_folder(sample, use_exome_alignment):
    """get sample folder"""
    alignment_dir = EXOME_ALIGNMENT_DIR if use_exome_alignment else ALIGNMENT_DIR
    return f"{BASE_PATH}/{sample}/{alignment_dir}"


def mkdir_p(name):
    """create dir if not exist"""
    if not os.path.exists(name):
        os.makedirs(name)


class OneThousandGenomesDownloader:
    """
    FTP Downloader class
    """

    def __init__(self, file_format=DEFAULT_FILE_FORMAT, use_mapped_file=True, use_exome_alignment=True,
                 on_download_finish=None, output_folder=None):
        """
        :param file_format: the file format of the sample: bam or cram
        :param use_mapped_file: if to download the mapped or the unmapped file
        :param use_exome_alignment: if to download from the exome alignment folder
        :param on_download_finish: a callback function
        :param output_folder: output folder
        """
        self.file_format = DEFAULT_FILE_FORMAT
        self.set_file_format(file_format)
        self.file_mapped = 'mapped' if use_mapped_file else 'unmapped'
        self.on_download_finish = on_download_finish
        self.output_folder = output_folder if output_folder is not None else OUTPUT_FOLDER
        self.use_exome_alignment = use_exome_alignment

    def __call__(self, sample):
        """
        :param sample: sample name
        """
        ftp = FTP(FTP_PATH)
        ftp.login()
        ftp.cwd(get_sample_folder(sample, self.use_exome_alignment))
        files = [f for f in ftp.nlst() if
                 f'.{self.file_mapped}.' in f and (f.split(".")[-1] in FORMATS[self.file_format])]
        out_folder = f"{self.output_folder}/{sample}"
        mkdir_p(out_folder)
        for idx, sample_file in enumerate(files):
            with open(f'{out_folder}/{sample_file}', 'wb') as out_file:
                with tqdm(total=ftp.size(sample_file),
                          unit_scale=True,
                          desc=f"{idx} - {sample_file}",
                          miniters=1,
                          file=sys.stdout,
                          leave=True
                          ) as pbar:
                    def callback(data):
                        pbar.update(len(data))
                        out_file.write(data)

                    ftp.retrbinary('RETR {}'.format(sample_file), callback)
        ftp.quit()
        if self.on_download_finish is not None:
            self.on_download_finish(sample)

    def set_file_format(self, file_format):
        """Set file format"""
        if file_format in FORMATS.keys():
            self.file_format = file_format
        else:
            raise Exception(f"the file format {file_format} is not supported.")
