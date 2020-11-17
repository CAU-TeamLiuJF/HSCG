import os
from ..base import BaseConfigParam, BashIO, run_bash, logger


class DataConfigParam(BaseConfigParam):
    def __init__(self):
        super().__init__()

        self.section = "long_read"
        self.need_clean = 1
        self.workdir = 'long_reads_correct'


class BoptConfigParam(BaseConfigParam):
    def __init__(self):
        super().__init__()

        self.section = "long_read"
        self.lordec_path = "lordec-correct"


class OptConfigParam(BaseConfigParam):
    def __init__(self):
        super().__init__()

        self.section = "long_read"
        self.program = 'LORDEC'
        self.param = '-k 21 -s 3 -a 5 -S statistics.txt'
        self.output = 'CorrectHQ.fa'
        self.threads = '1'


class LongReadsTreatment:
    def __init__(self, pipeline_config_params, binary_config_params, core_config_params):
        super().__init__()
        self.module_name = "long_read"
        self.bash_script = "long_reads_treatment.sh"

        self.pipeline_config_params = pipeline_config_params
        self.binary_config_params = binary_config_params
        self.core_config_params = core_config_params

        self.data_config = DataConfigParam()
        self.bopt_config = BoptConfigParam()
        self.opt_config = OptConfigParam()

        self.need = 0

    def validate_config_params(self):
        if self.module_name not in self.pipeline_config_params:
            logger.error('Please provide [{}] in opt.ini!'.format(self.module_name))
            exit(1)
        else:
            if 'need_clean' not in self.pipeline_config_params[self.module_name]:
                logger.error('Please provide [need_clean] in opt.ini!')
                exit(1)
            elif self.pipeline_config_params[self.module_name]['need_clean'] not in ('0', '1'):
                logger.error('[need_clean] should in [0, 1]!')
                exit(1)
            else:
                if self.pipeline_config_params[self.module_name]['need_clean'] == '1':
                    self.need = 1
                    if 'workdir' not in self.pipeline_config_params[self.module_name]:
                        logger.error('Please provide [workdir] in opt.ini!')
                        exit(1)
                    elif not self.pipeline_config_params[self.module_name]['workdir']:
                        logger.error('Please provide [workdir] in opt.ini!')
                        exit(1)
                else:
                    self.need = 0

        if self.need == 1:
            if self.module_name not in self.binary_config_params:
                logger.error('Please provide [{}] in bopt.ini!'.format(self.module_name))
                exit(1)
            else:
                if 'lordec_path' not in self.binary_config_params[self.module_name]:
                    logger.error('Please provide [lordec_path] in bopt.ini!')
                    exit(1)
                if not self.binary_config_params[self.module_name]['lordec_path']:
                    logger.error('Please provide [lordec_path] in bopt.ini!')
                    exit(1)

            if self.module_name not in self.core_config_params:
                logger.error('Please provide [{}] in parameter.ini!'.format(self.module_name))
                exit(1)
            else:
                if 'program' not in self.core_config_params[self.module_name] or not self.core_config_params[self.module_name]['program']:
                    logger.error('Please provide [program] in parameter.ini!')
                    exit(1)
                if 'param' not in self.core_config_params[self.module_name] or not self.core_config_params[self.module_name]['param']:
                    logger.error('Please provide [param] in parameter.ini!')
                    exit(1)
                if 'output' not in self.core_config_params[self.module_name] or not self.core_config_params[self.module_name]['output']:
                    logger.error('Please provide [output] in parameter.ini!')
                    exit(1)
                if 'threads' not in self.core_config_params[self.module_name] or not self.core_config_params[self.module_name]['threads']:
                    logger.error('Please provide [threads] in parameter.ini!')
                    exit(1)

    def get_pipeline_config(self):
        return DataConfigParam().list_all_member()

    def get_binary_config(self):
        return BoptConfigParam().list_all_member()

    def get_core_config(self):
        return OptConfigParam().list_all_member()

    def run_pipeline(self):
        print("""
        ################################################
        #              Long Reads Treatment            #
        ################################################
        """)
        logger.info('Executing error correction ...')
        self.validate_config_params()

        if self.need == 1:
            current_path = os.getcwd()

            # Initialize command
            command_content_list = [self.binary_config_params[self.module_name]['lordec_path']]
            command_content_list.append(self.core_config_params[self.module_name]['param'])
            command_content_list.append("-i {}".format(self.pipeline_config_params['data']['long_reads_file']))

            # Use raw/cleaned fastq
            # If cleaned in short_read step, read the preprocessed data
            # If not cleaned in short_read step, read the primary data
            if self.pipeline_config_params['short_read']['need_clean'] == '1':
                if self.pipeline_config_params['data']['short_reads_paired'] == '1':
                    fq1, fq2 = self.pipeline_config_params['data']['short_reads_file'].split(',')
                    fq1_prefix_pre = os.path.splitext(os.path.split(fq1)[1])[0].split('.')[:-1]
                    fq1_prefix_last = os.path.splitext(os.path.split(fq1)[1])[0].split('.')[-1]
                    fq1_name = '.'.join(fq1_prefix_pre) + "." + fq1_prefix_last + "_val_1.fq"
                    fq2_prefix_pre = os.path.splitext(os.path.split(fq2)[1])[0].split('.')[:-1]
                    fq2_prefix_last = os.path.splitext(os.path.split(fq2)[1])[0].split('.')[-1]
                    fq2_name = '.'.join(fq2_prefix_pre) + "." + fq2_prefix_last + "_val_2.fq"
                    fq1_path = os.path.join(current_path, self.pipeline_config_params['short_read']['workdir'], fq1_name)
                    fq2_path = os.path.join(current_path, self.pipeline_config_params['short_read']['workdir'], fq2_name)
                    command_content_list.append("-2 {},{}".format(fq1_path, fq2_path))
                else:
                    fq = self.pipeline_config_params['data']['short_reads_file']
                    fq_prefix_pre = os.path.splitext(os.path.split(fq)[1])[0].split('.')[:-1]
                    fq_prefix_last = os.path.splitext(os.path.split(fq)[1])[0].split('.')[-1]
                    fq_name = '.'.join(fq_prefix_pre) + "." + fq_prefix_last + "_val.fq"
                    fq_path = os.path.join(current_path, self.pipeline_config_params['short_read']['workdir'], fq_name)
                    command_content_list.append("-2 {}".format(fq_path))
            else:
                if self.pipeline_config_params['data']['short_reads_paired'] == '1':
                    fq1, fq2 = self.pipeline_config_params['data']['short_reads_file'].split(',')
                    command_content_list.append("-2 {},{}".format(fq1, fq2))
                else:
                    fq = self.pipeline_config_params['data']['short_reads_file']
                    command_content_list.append("-2 {}".format(fq))

            # Define output file
            command_content_list.append("-o {}".format(self.core_config_params[self.module_name]['output']))
            # Define thread
            command_content_list.append("-T {}".format(self.core_config_params[self.module_name]['threads']))

            # Generate command bash
            workdir = self.pipeline_config_params[self.module_name]['workdir']

            os.makedirs(workdir, exist_ok=True)
            os.chdir(workdir)

            bash_io = BashIO(self.bash_script)
            command = " ".join(command_content_list)
            print(command)
            bash_io.add_core_command(command)
            bash_io.output_bash()

            # Run command bash
            bash_command = ['bash', "{}".format(self.bash_script), '|&', 'tee', "{}.log".format(self.bash_script)]
            run_bash(self.module_name, bash_command)

            logger.info('Long reads error correction completed!')

            os.chdir(current_path)

        else:
            logger.info('Skipping error correction.')
