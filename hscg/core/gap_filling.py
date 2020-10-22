import os
from ..base import BaseConfigParam, BashIO, run_bash, logger


class DataConfigParam(BaseConfigParam):
    def __init__(self):
        super().__init__()

        self.section = "gap_filling"
        self.method_type = "TGS_GapCloser"  # TGS_GapCloser, LR_Gapcloser
        self.need = "1"
        self.workdir = "gap_filling"


class BoptConfigParam(BaseConfigParam):
    def __init__(self):
        super().__init__()

        self.section = "gap_filling"
        self.tgs_gapcloser_path = "TGS-GapCloser.sh"
        self.lr_gapcloser_path = "LR_Gapcloser.sh"


class OptConfigParam(BaseConfigParam):
    def __init__(self):
        super().__init__()

        self.section = "gap_filling"

        self.tgs_gapcloser_param = "--ne --tgstype pb"
        self.tgs_gapcloser_threads = 1

        self.lr_gapcloser_param = "-s p"
        self.lr_gapcloser_threads = 1


class GapFilling:
    def __init__(self, pipeline_config_params, binary_config_params, core_config_params):
        super().__init__()
        self.module_name = 'gap_filling'
        self.bash_script = "gap_filling.sh"

        self.pipeline_config_params = pipeline_config_params
        self.binary_config_params = binary_config_params
        self.core_config_params = core_config_params

        self.need = 0

    def validate_config_params(self):
        if self.module_name not in self.pipeline_config_params:
            logger.error('Please provide [{}] in opt.ini!'.format(self.module_name))
            exit(1)
        else:
            if 'need' not in self.pipeline_config_params[self.module_name]:
                logger.error('Please provide [need] in opt.ini!')
                exit(1)
            elif self.pipeline_config_params[self.module_name]['need'] not in ('0', '1'):
                logger.error('[need] should in [0, 1]!')
                exit(1)
            else:
                if self.pipeline_config_params[self.module_name]['need'] == '1':
                    self.need = 1

                    if 'method_type' not in self.pipeline_config_params[self.module_name]:
                        logger.error('Please provide [method_type] in opt.ini!')
                        exit(1)
                    elif self.pipeline_config_params[self.module_name]['method_type'] not in ('TGS_GapCloser', 'LR_Gapcloser'):
                        logger.error('[method_type] should in [TGS_GapCloser, LR_Gapcloser]!')
                        exit(1)

                    if 'workdir' not in self.pipeline_config_params[self.module_name]:
                        logger.error('Please provide [workdir] in opt.ini!')
                        exit(1)
                    elif not self.pipeline_config_params[self.module_name]['workdir']:
                        logger.error('Please provide [workdir] in opt.ini!')
                        exit(1)
                else:
                    self.need = 0

        if self.need == 1:
            method_type = self.pipeline_config_params[self.module_name]['method_type']

            if self.module_name not in self.binary_config_params:
                logger.error('Please provide [{}] in bopt.ini!'.format(self.module_name))
                exit(1)
            else:
                if method_type == 'TGS_GapCloser':
                    if 'tgs_gapcloser_path' not in self.binary_config_params[self.module_name] or not self.binary_config_params[self.module_name]['tgs_gapcloser_path']:
                        logger.error('Please provide [tgs_gapcloser_path] in bopt.ini!')
                        exit(1)
                elif method_type == 'LR_Gapcloser':
                    if 'lr_gapcloser_path' not in self.binary_config_params[self.module_name] or not self.binary_config_params[self.module_name]['lr_gapcloser_path']:
                        logger.error('Please provide [lr_gapcloser_path] in bopt.ini!')
                        exit(1)

            if self.module_name not in self.core_config_params:
                logger.error('Please provide [{}] in parameter.ini!'.format(self.module_name))
                exit(1)
            else:
                if method_type == 'TGS_GapCloser':
                    if 'tgs_gapcloser_param' not in self.core_config_params[self.module_name] or not self.core_config_params[self.module_name]['tgs_gapcloser_param']:
                        logger.error('Please provide [tgs_gapcloser_param] in parameter.ini!')
                        exit(1)
                    if 'tgs_gapcloser_threads' not in self.core_config_params[self.module_name] or not self.core_config_params[self.module_name]['tgs_gapcloser_threads']:
                        logger.error('Please provide [tgs_gapcloser_threads] in parameter.ini!')
                        exit(1)
                elif method_type == 'LR_Gapcloser':
                    if 'lr_gapcloser_param' not in self.core_config_params[self.module_name] or not self.core_config_params[self.module_name]['lr_gapcloser_param']:
                        logger.error('Please provide [lr_gapcloser_param] in parameter.ini!')
                        exit(1)
                    if 'lr_gapcloser_threads' not in self.core_config_params[self.module_name] or not self.core_config_params[self.module_name]['lr_gapcloser_threads']:
                        logger.error('Please provide [lr_gapcloser_threads] in parameter.ini!')
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
        #                  Gap Filling                 #
        ################################################
        """)
        logger.info('Executing Gap Filling ...')
        self.validate_config_params()

        if self.need == 1:
            # Use Use raw/cleaned fasta
            if self.pipeline_config_params['long_read']['need_clean'] == '1':
                pacbio = os.path.join('..', self.pipeline_config_params['long_read']['workdir'], self.core_config_params['long_read']['output'])
            else:
                pacbio = self.pipeline_config_params['data']['long_reads_file']

            # Use raw/generated assembly
            if self.pipeline_config_params['scaffolding_ref_based']['need'] == '1':
                assembly = os.path.join('..', self.pipeline_config_params['scaffolding_ref_based']['workdir'], 'ragoo_output', 'ragoo.fasta')
            elif self.pipeline_config_params['scaffolding']['need'] == '1':
                method_type = self.pipeline_config_params['scaffolding']['method_type']
                if method_type == 'PBJELLY2':
                    assembly = os.path.join('..', self.pipeline_config_params['scaffolding']['workdir'], 'output', 'jelly.out.fasta')
                elif method_type == 'SSPACELongRead':
                    assembly = os.path.join('..', self.pipeline_config_params['scaffolding']['workdir'], 'PacBio_scaffolder_results', 'scaffolds.fasta')
                else:
                    logger.error('Please provide [assembly] in opt.ini!')
                    exit(1)
            elif self.pipeline_config_params['assembly']['need'] == '1':
                assembly = os.path.join('..', self.pipeline_config_params['assembly']['workdir'], 'consensus_dir', 'final_assembly.fasta')
            else:
                if not self.pipeline_config_params['data']['assembly'] or not os.path.exists(self.pipeline_config_params['data']['assembly']):
                    logger.error('Please provide [assembly] in opt.ini!')
                    exit(1)
                assembly = self.pipeline_config_params['data']['assembly']

            method_type = self.pipeline_config_params[self.module_name]['method_type']

            command_list = []
            if method_type == 'TGS_GapCloser':
                logger.info('Running TGS_GapCloser pipeline ...')

                thread = self.core_config_params[self.module_name]['tgs_gapcloser_threads']

                command_temp = [self.binary_config_params[self.module_name]['tgs_gapcloser_path']]
                command_temp.append('--scaff {}'.format(assembly))
                command_temp.append('--reads {}'.format(pacbio))
                command_temp.append('--output test_ne')
                command_temp.append(self.core_config_params[self.module_name]['tgs_gapcloser_param'])
                command_temp.append('--thread {}'.format(self.core_config_params[self.module_name]['tgs_gapcloser_threads']))

                command_list.append(' '.join(command_temp))
            elif method_type == 'LR_Gapcloser':
                logger.info('Running LR_Gapcloser pipeline ...')

                thread = self.core_config_params[self.module_name]['lr_gapcloser_threads']

                command_temp = [self.binary_config_params[self.module_name]['lr_gapcloser_path']]
                command_temp.append('-i {}'.format(assembly))
                command_temp.append('-l {}'.format(pacbio))
                command_temp.append(self.core_config_params[self.module_name]['lr_gapcloser_param'])
                command_temp.append('-t {}'.format(self.core_config_params[self.module_name]['lr_gapcloser_threads']))

                command_list.append(' '.join(command_temp))

            # Generate command bash
            current_path = os.getcwd()
            workdir = self.pipeline_config_params[self.module_name]['workdir']

            os.makedirs(workdir, exist_ok=True)
            os.chdir(workdir)

            bash_io = BashIO(self.bash_script)
            command = "\n".join(command_list)
            print(command)
            for command in command_list:
                bash_io.add_core_command(command)
            bash_io.output_bash()

            # Run command bash
            bash_command = ['bash', "{}".format(self.bash_script), '|&', 'tee', "{}.log".format(self.bash_script)]
            run_bash(self.module_name, bash_command)

            logger.info('Gap Filling completed!')
            os.chdir(current_path)
        else:
            logger.info('Skipping Gap Filling.')
