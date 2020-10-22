import os
from ..base import BaseConfigParam, logger

class DataConfigParam(BaseConfigParam):
    def __init__(self):
        super().__init__()

        self.section = "data"
        self.short_reads_file = ""
        self.short_reads_paired = "1"
        self.long_reads_file = ""
        self.reference_file = ""
        self.assembly = ""


class Data:
    def __init__(self, pipeline_config_params, binary_config_params, core_config_params):
        super().__init__()
        self.module_name = "data"
        # self.bash_script = "short_reads_treatment.sh"
        self.pipeline_config_params = pipeline_config_params

        self.data_config = DataConfigParam()

    def validate_config_params(self):
        if self.module_name not in self.pipeline_config_params:
            logger.error('Please provide [{}] in opt.ini!'.format(self.module_name))
            exit(1)
        else:
            if 'short_reads_paired' not in self.pipeline_config_params[self.module_name]:
                logger.error('Please provide [short_reads_paired] in opt.ini!')
                exit(1)
            elif self.pipeline_config_params[self.module_name]['short_reads_paired'] not in ('0', '1'):
                logger.error('[short_reads_paired] should in [0, 1]!')
                exit(1)
            else:
                if 'short_reads_file' not in self.pipeline_config_params[self.module_name]:
                    logger.error('Please provide [short_reads_file] in opt.ini!')
                    exit(1)
                else:
                    short_reads_paired = self.pipeline_config_params[self.module_name]['short_reads_paired']
                    fq_file = self.pipeline_config_params[self.module_name]['short_reads_file']
                    if short_reads_paired == '0':
                        if not fq_file or not os.path.exists(fq_file):
                            logger.error("[short_reads_file] not exists: {}, if you won't use it, you can just provide an empty but existed file!".format(fq_file))
                            exit(1)
                    elif short_reads_paired == '1':
                        multiple_fq_file = self.pipeline_config_params[self.module_name]['short_reads_file']
                        if not multiple_fq_file:
                            logger.error("[short_reads_file] not exists, if you won't use it, you can just provide an empty but existed file!")
                            exit(1)
                        else:
                            if len(multiple_fq_file.split(',')) != 2:
                                logger.error("[short_reads_file] should be pair-end, if you won't use it, you can just provide an empty but existed file!")
                                exit(1)
                            else:
                                fq1, fq2 = self.pipeline_config_params['data']['short_reads_file'].split(',')
                                if not fq1 or not os.path.exists(fq1):
                                    logger.error("[short_reads_file] not exists: {}, if you won't use it, you can just provide an empty but existed file!".format(fq1))
                                    exit(1)
                                if not fq2 or not os.path.exists(fq2):
                                    logger.error("[short_reads_file] not exists: {}, if you won't use it, you can just provide an empty but existed file!".format(fq2))
                                    exit(1)

            if 'long_reads_file' not in self.pipeline_config_params[self.module_name]:
                logger.error('Please provide [long_reads_file] in opt.ini!')
                exit(1)
            else:
                long_reads_file = self.pipeline_config_params[self.module_name]['long_reads_file']
                if not long_reads_file or not os.path.exists(long_reads_file):
                    logger.error("[long_reads_file] not exists: {}, if you won't use it, you can just provide an empty but existed file!".format(long_reads_file))
                    exit(1)

            if 'reference_file' not in self.pipeline_config_params[self.module_name]:
                logger.error('Please provide [reference_file] in opt.ini!')
                exit(1)
            else:
                reference_file = self.pipeline_config_params[self.module_name]['reference_file']
                if not reference_file or not os.path.exists(reference_file):
                    logger.error("[reference_file] not exists: {}, if you won't use it, you can just provide an empty but existed file!".format(reference_file))
                    exit(1)

    def get_pipeline_config(self):
        return DataConfigParam().list_all_member()

    def get_binary_config(self):
        return []

    def get_core_config(self):
        return []

    def run_pipeline(self):
        print("""
        ################################################
        #                Data Validator                #
        ################################################
        """)
        logger.info('Executing Data validator...')
        self.validate_config_params()
        logger.info('Data validator completed!')
