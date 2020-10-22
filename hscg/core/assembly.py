import os
from ..base import BaseConfigParam, BashIO, run_bash, logger


class DataConfigParam(BaseConfigParam):
    def __init__(self):
        super().__init__()

        self.section = "assembly"
        self.need = '1'
        self.workdir = 'assembly'



class BoptConfigParam(BaseConfigParam):
    def __init__(self):
        super().__init__()

        self.section = "assembly"
        self.sparseassembler_path = "SparseAssembler"
        self.dbg2olc_path = "DBG2OLC"
        self.split_and_run_sparc_path = "split_and_run_sparc.sh"


class OptConfigParam(BaseConfigParam):
    def __init__(self):
        super().__init__()

        self.section = "assembly"
        self.program = "DBG2OLC"
        self.sparseassembler_param = 'LD 0 k 67 g 15 NodeCovTh 1 EdgeCovTh 0 GS 2800000000'
        self.dbg2olc_param = 'LD 0 k 17 AdaptiveTh 0.001 KmerCovTh 2 MinOverlap 20 RemoveChimera 1'
        self.split_and_run_sparc_param = './consensus_dir 2 >cns_log.txt'


class Assembly:
    def __init__(self, pipeline_config_params, binary_config_params, core_config_params):
        super().__init__()
        self.module_name = "assembly"
        self.bash_script = "assembly.sh"

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
                        logger.error('Please provide [need_clean] in opt.ini!')
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
                if 'sparseassembler_path' not in self.binary_config_params[self.module_name] or not self.binary_config_params[self.module_name]['sparseassembler_path']:
                    logger.error('Please provide [lordec_path] in bopt.ini!')
                    exit(1)
                if 'dbg2olc_path' not in self.binary_config_params[self.module_name] or not self.binary_config_params[self.module_name]['dbg2olc_path']:
                    logger.error('Please provide [dbg2olc_path] in bopt.ini!')
                    exit(1)
                if 'split_and_run_sparc_path' not in self.binary_config_params[self.module_name] or not self.binary_config_params[self.module_name]['split_and_run_sparc_path']:
                    logger.error('Please provide [split_and_run_sparc_path] in bopt.ini!')
                    exit(1)

            if self.module_name not in self.core_config_params:
                logger.error('Please provide [{}] in parameter.ini!'.format(self.module_name))
                exit(1)
            else:
                if 'program' not in self.core_config_params[self.module_name] or not self.core_config_params[self.module_name]['program']:
                    logger.error('Please provide [program] in parameter.ini!')
                    exit(1)
                if 'sparseassembler_param' not in self.core_config_params[self.module_name] or not self.core_config_params[self.module_name]['sparseassembler_param']:
                    logger.error('Please provide [sparseassembler_param] in parameter.ini!')
                    exit(1)
                if 'dbg2olc_param' not in self.core_config_params[self.module_name] or not self.core_config_params[self.module_name]['dbg2olc_param']:
                    logger.error('Please provide [dbg2olc_param] in parameter.ini!')
                    exit(1)
                if 'split_and_run_sparc_param' not in self.core_config_params[self.module_name] or not self.core_config_params[self.module_name]['split_and_run_sparc_param']:
                    logger.error('Please provide [split_and_run_sparc_param] in parameter.ini!')
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
        #                  Assembly                    #
        ################################################
        """)
        logger.info('Executing assembly ...')
        self.validate_config_params()

        if self.need == 1:
            # Initialize command
            command_list = []
            # step 1
            command_temp = [self.binary_config_params[self.module_name]['sparseassembler_path']]
            command_temp.append(self.core_config_params[self.module_name]['sparseassembler_param'])
            # Use raw/cleaned fastq
            if self.pipeline_config_params['short_read']['need_clean'] == '1':
                if self.pipeline_config_params['data']['short_reads_paired'] == '1':
                    fq1, fq2 = self.pipeline_config_params['data']['short_reads_file'].split(',')
                    fq1_name = '.'.join(os.path.splitext(os.path.split(fq1)[1])[0].split('.')[:-1]) + "_val_1.fq"
                    fq2_name = '.'.join(os.path.splitext(os.path.split(fq2)[1])[0].split('.')[:-1]) + "_val_2.fq"
                    fq1_path = os.path.join('..', self.pipeline_config_params['short_read']['workdir'], fq1_name)
                    fq2_path = os.path.join('..', self.pipeline_config_params['short_read']['workdir'], fq2_name)
                    command_temp.append("i1 {} i2 {}".format(fq1_path, fq2_path))
                else:
                    fq = self.pipeline_config_params['data']['short_reads_file']
                    fq_name = '.'.join(os.path.splitext(os.path.split(fq)[1])[0].split('.')[:-1]) + "_val.fq"
                    fq_path = os.path.join('..', self.pipeline_config_params['short_read']['workdir'], fq_name)
                    command_temp.append("f {}".format(fq_path))
            else:
                if self.pipeline_config_params['data']['short_reads_paired'] == '1':
                    fq1, fq2 = self.pipeline_config_params['data']['short_reads_file'].split(',')
                    command_temp.append("i1 {} i2 {}".format(fq1, fq2))
                else:
                    fq = self.pipeline_config_params['data']['short_reads_file']
                    command_temp.append("f {}".format(fq))
            command_list.append(' '.join(command_temp))
            # step 2
            # Contigs.txt generated by SparseAssembler
            command_temp = [self.binary_config_params[self.module_name]['dbg2olc_path']]
            command_temp.append(self.core_config_params[self.module_name]['dbg2olc_param'])
            command_temp.append("Contigs Contigs.txt")
            # Use raw/cleaned fastq
            if self.pipeline_config_params['long_read']['need_clean'] == '1':
                pacbio = os.path.join('..', self.pipeline_config_params['long_read']['workdir'], self.core_config_params['long_read']['output'])
                command_temp.append("f {}".format(pacbio))
            else:
                pacbio = self.pipeline_config_params['data']['long_reads_file']
                command_temp.append('f {}'.format(pacbio))
            command_list.append(' '.join(command_temp))
            # step 3
            # backbone_raw.fasta, DBG2OLC_Consensus_info.txt generated by DBG2OLC   ctg_pb.fasta generated by user
            command_list.append('cat Contigs.txt {} > ctg_pb.fasta'.format(pacbio))
            command_temp = []
            command_temp.extend([
                self.binary_config_params[self.module_name]['split_and_run_sparc_path'],
                "backbone_raw.fasta DBG2OLC_Consensus_info.txt ctg_pb.fasta",
                self.core_config_params[self.module_name]['split_and_run_sparc_param']
            ])
            command_list.append(' '.join(command_temp))

            # Generate command bash
            current_path = os.getcwd()
            workdir = self.pipeline_config_params[self.module_name]['workdir']

            os.makedirs(workdir, exist_ok=True)
            os.chdir(workdir)

            bash_io = BashIO(self.bash_script)
            command = "\n".join(command_list)
            print(command)
            bash_io.add_pre_command("ulimit -s unlimited")
            for command in command_list:
                bash_io.add_core_command(command)
            bash_io.output_bash()

            # Run command bash
            bash_command = ['bash', "{}".format(self.bash_script), '|&', 'tee', "{}.log".format(self.bash_script)]
            run_bash(self.module_name, bash_command)

            logger.info('Assembly completed!')

            os.chdir(current_path)
        else:
            logger.info('Skipping assembly.')
