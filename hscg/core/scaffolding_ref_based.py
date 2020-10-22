import os
from ..base import BaseConfigParam, BashIO, run_bash, logger


class DataConfigParam(BaseConfigParam):
    def __init__(self):
        super().__init__()

        self.section = "scaffolding_ref_based"
        self.need = "1"
        self.workdir = "scaffolding_ref_based"


class BoptConfigParam(BaseConfigParam):
    def __init__(self):
        super().__init__()

        self.section = "scaffolding_ref_based"
        self.ragoo_path = "ragoo.py"


class OptConfigParam(BaseConfigParam):
    def __init__(self):
        super().__init__()

        self.section = "scaffolding_ref_based"
        self.program = "RaGoo"
        self.ragoo_param = "-C"
        self.ragoo_threads = 1


class ScaffoldingRefBased:
    def __init__(self, pipeline_config_params, binary_config_params, core_config_params):
        super().__init__()
        self.module_name = 'scaffolding_ref_based'
        self.bash_script = 'scaffolding_ref_based.sh'

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
            if 'need' not in self.pipeline_config_params[self.module_name]:
                logger.error('Please provide [need] in opt.ini!')
                exit(1)
            elif self.pipeline_config_params[self.module_name]['need'] not in ('0', '1'):
                logger.error('[need] should in [0, 1]!')
                exit(1)
            else:
                if self.pipeline_config_params[self.module_name]['need'] == '1':
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
                if 'ragoo_path' not in self.binary_config_params[self.module_name] or not self.binary_config_params[self.module_name]['ragoo_path']:
                    logger.error('Please provide [ragoo_path] in bopt.ini!')
                    exit(1)

            if self.module_name not in self.core_config_params:
                logger.error('Please provide [{}] in parameter.ini!'.format(self.module_name))
                exit(1)
            else:
                if 'program' not in self.core_config_params[self.module_name] or not self.core_config_params[self.module_name]['program']:
                    logger.error('Please provide [program] in parameter.ini!')
                    exit(1)
                if 'ragoo_param' not in self.core_config_params[self.module_name] or not self.core_config_params[self.module_name]['ragoo_param']:
                    logger.error('Please provide [ragoo_param] in parameter.ini!')
                    exit(1)
                if 'ragoo_threads' not in self.core_config_params[self.module_name] or not self.core_config_params[self.module_name]['ragoo_threads']:
                    logger.error('Please provide [ragoo_threads] in parameter.ini!')
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
        #        Reference-based Scaffolding           #
        ################################################
        """)
        logger.info('Executing Reference-based Scaffolding ...')
        self.validate_config_params()

        if self.need == 1:
            # Use Use raw/cleaned fasta
            if self.pipeline_config_params['long_read']['need_clean'] == '1':
                pacbio = os.path.join('..', self.pipeline_config_params['long_read']['workdir'], self.core_config_params['long_read']['output'])
            else:
                pacbio = self.pipeline_config_params['data']['long_reads_file']

            # Use raw/generated assembly
            if self.pipeline_config_params['scaffolding']['need'] == '1':
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

            thread = self.core_config_params[self.module_name]['ragoo_threads']
            reference_file = self.pipeline_config_params['data']['reference_file']

            # Initialize command
            command_list = []

            link_assembly_file = "final_assembly.fasta"
            link_reference_file = "reference.fasta"
            command_temp = ['ln', '-snf', '{}'.format(assembly), link_assembly_file]
            command_list.append(' '.join(command_temp))
            command_temp = ['ln', '-snf', '{}'.format(reference_file), link_reference_file]
            command_list.append(' '.join(command_temp))

            command_temp = [self.binary_config_params[self.module_name]['ragoo_path']]
            command_temp.append(link_assembly_file)
            command_temp.append(link_reference_file)
            command_temp.append(self.core_config_params[self.module_name]['ragoo_param'])
            command_temp.append('-t {}'.format(thread))
            command_list.append(" ".join(command_temp))

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

            logger.info('Reference-based Scaffolding completed!')
            os.chdir(current_path)
        else:
            logger.info('Skipping Reference-based Scaffolding.')
