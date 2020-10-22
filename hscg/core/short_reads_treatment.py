import os
from ..base import BaseConfigParam, BashIO, run_bash, logger


class DataConfigParam(BaseConfigParam):
    def __init__(self):
        super().__init__()

        self.section = "short_read"
        self.need_clean = '1'
        self.workdir = 'short_reads_qc'


class BoptConfigParam(BaseConfigParam):
    def __init__(self):
        super().__init__()

        self.section = "short_read"
        self.trim_galore_path = "trim_galore"


class OptConfigParam(BaseConfigParam):
    def __init__(self):
        super().__init__()

        self.section = "short_read"
        self.program = 'TrimGalore'
        self.param = '-q 20 --phred33 --stringency 3 --length 20 -e 0.1'
        self.threads = '1'


class ShortReadsTreatment:
    def __init__(self, pipeline_config_params, binary_config_params, core_config_params):
        super().__init__()
        self.module_name = "short_read"
        self.bash_script = "short_reads_treatment.sh"

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
                if 'trim_galore_path' not in self.binary_config_params[self.module_name]:
                    logger.error('Please provide [trim_galore_path] in bopt.ini!')
                    exit(1)
                if not self.binary_config_params[self.module_name]['trim_galore_path']:
                    logger.error('Please provide [trim_galore_path] in bopt.ini!')
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
        #              Short Reads Treatment           #
        ################################################
        """)
        logger.info('Executing quality control ...')
        self.validate_config_params()

        if self.need == 1:
            # Initialize command
            command_content_list = [self.binary_config_params[self.module_name]['trim_galore_path']]
            command_content_list.append(self.core_config_params[self.module_name]['param'])

            # if short reads number == 2, needs '--paired'
            pair_flag = 0
            if self.pipeline_config_params['data']['short_reads_paired'] == '1':
                command_content_list.append('--paired')
                reads_file = ' '.join(self.pipeline_config_params['data']['short_reads_file'].split(','))
                command_content_list.append(reads_file)
                pair_flag = 1
            else:
                reads_file = self.pipeline_config_params['data']['short_reads_file']
                command_content_list.append(reads_file)

            # if short reads end with .gz, needs '--gzip'
            gzip_flag = 0
            fq_filename = self.pipeline_config_params['data']['short_reads_file'].split(',')[0]
            if os.path.splitext(fq_filename)[1] == '.gz':
                command_content_list.append('--gzip')
                gzip_flag = 1

            # thread parameter
            command_content_list.append("-j {}".format(self.core_config_params[self.module_name]['threads']))

            # Generate command bash
            current_path = os.getcwd()
            workdir = self.pipeline_config_params[self.module_name]['workdir']

            os.makedirs(workdir, exist_ok=True)
            os.chdir(workdir)

            bash_io = BashIO(self.bash_script)
            command = " ".join(command_content_list)
            print(command)
            bash_io.add_core_command(command)

            if gzip_flag == 1:
                bash_io.add_core_command("")
                if pair_flag == 1:
                    fq1, fq2 = self.pipeline_config_params['data']['short_reads_file'].split(',')
                    # default output by trim_galore
                    fq1_name = '.'.join(os.path.splitext(os.path.split(fq1)[1])[0].split('.')[:-1]) + "_val_1.fq"
                    fq2_name = '.'.join(os.path.splitext(os.path.split(fq2)[1])[0].split('.')[:-1]) + "_val_2.fq"
                    bash_io.add_core_command("gunzip -c {}.gz > {}".format(fq1_name, fq1_name))
                    bash_io.add_core_command("gunzip -c {}.gz > {}".format(fq2_name, fq2_name))
                else:
                    fq = self.pipeline_config_params['data']['short_reads_file']
                    # default output by trim_galore
                    fq_name = '.'.join(os.path.splitext(os.path.split(fq)[1])[0].split('.')[:-1]) + "_val.fq"
                    bash_io.add_core_command("gunzip -c {}.gz > {}".format(fq_name, fq_name))

            bash_io.output_bash()

            # Run command bash
            bash_command = ['bash', "{}".format(self.bash_script), '|&', 'tee', "{}.log".format(self.bash_script)]
            run_bash(self.module_name, bash_command)

            logger.info('Short reads quality control completed!')

            os.chdir(current_path)
        else:
            logger.info('Skipping quality control.')
