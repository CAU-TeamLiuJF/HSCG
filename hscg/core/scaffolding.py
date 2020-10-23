import os
from ..base import BaseConfigParam, BashIO, split_fasta_by_size, run_bash, logger
from xml.dom import minidom


class DataConfigParam(BaseConfigParam):
    def __init__(self):
        super().__init__()

        self.section = "scaffolding"
        self.need = "1"
        self.method_type = "PBJELLY2"  # PBJELLY2, SSPACELongRead
        self.workdir = "scaffolding"


class BoptConfigParam(BaseConfigParam):
    def __init__(self):
        super().__init__()

        self.section = "scaffolding"
        self.pbjelly_fakequals_path = "fakeQuals.py"
        self.pbjelly_jelly_path = "Jelly.py"
        self.sspace_longread_path = "SSPACE-LongRead.pl"


class OptConfigParam(BaseConfigParam):
    def __init__(self):
        super().__init__()

        self.section = "scaffolding"

        self.pbjelly2_param = "-minMatch 8 -sdpTupleSize 8 -minPctIdentity 75 -bestn 1 -nCandidates 10 -maxScore -500 -noSplitSubreads"
        self.pbjelly2_xml = "Protocol.xml"
        self.pbjelly2_threads = 1

        self.sspacelongread_threads = 1


def generate_pbjelly2_xml(assembly, thread, base_prefix="", blasr_command="", output="output", output_file="Protocol.xml", pacbio_list=[]):
    doc = minidom.Document()

    # root node
    root = doc.createElement('jellyProtocol')
    # root.setAttribute('company','AAA')
    doc.appendChild(root)

    # attribute node
    reference = doc.createElement('reference')
    output_dir = doc.createElement('outputDir')
    blasr = doc.createElement('blasr')
    input = doc.createElement('input')
    input.setAttribute('baseDir', base_prefix)
    root.appendChild(reference)
    root.appendChild(output_dir)
    root.appendChild(blasr)
    root.appendChild(input)

    reference_text = doc.createTextNode(assembly)
    reference.appendChild(reference_text)
    blasr_content = [blasr_command, "-nproc", thread]
    blasr_text = doc.createTextNode(" ".join(blasr_content))
    blasr.appendChild(blasr_text)
    output_text = doc.createTextNode(output)
    output_dir.appendChild(output_text)

    # add job
    for file in pacbio_list:
        job = doc.createElement('job')
        job_text = doc.createTextNode(file)
        job.appendChild(job_text)
        input.appendChild(job)

    with open(output_file, "w") as wp:
        doc.writexml(wp, indent='', addindent='\t', newl='\n', encoding='utf-8')


class Scaffolding:
    def __init__(self, pipeline_config_params, binary_config_params, core_config_params):
        super().__init__()
        self.module_name = "scaffolding"
        self.bash_script = "scaffolding.sh"

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
                    elif self.pipeline_config_params[self.module_name]['method_type'] not in ('PBJELLY2', 'SSPACELongRead'):
                        logger.error('[method_type] should in [PBJELLY2, SSPACELongRead]!')
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
            if self.module_name not in self.binary_config_params:
                logger.error('Please provide [{}] in bopt.ini!'.format(self.module_name))
                exit(1)
            else:
                method_type = self.pipeline_config_params[self.module_name]['method_type']

                if method_type == 'PBJELLY2':
                    if 'pbjelly_fakequals_path' not in self.binary_config_params[self.module_name] or not self.binary_config_params[self.module_name]['pbjelly_fakequals_path']:
                        logger.error('Please provide [trim_galore_path] in bopt.ini!')
                        exit(1)
                    if 'pbjelly_jelly_path' not in self.binary_config_params[self.module_name] or not self.binary_config_params[self.module_name]['pbjelly_jelly_path']:
                        logger.error('Please provide [pbjelly_jelly_path] in bopt.ini!')
                        exit(1)
                elif method_type == 'SSPACELongRead':
                    if 'sspace_longread_path' not in self.binary_config_params[self.module_name] or not self.binary_config_params[self.module_name]['sspace_longread_path']:
                        logger.error('Please provide [sspace_longread_path] in bopt.ini!')
                        exit(1)

            if self.module_name not in self.core_config_params:
                logger.error('Please provide [{}] in parameter.ini!'.format(self.module_name))
                exit(1)
            else:
                method_type = self.pipeline_config_params[self.module_name]['method_type']

                if method_type == 'PBJELLY2':
                    if 'pbjelly2_param' not in self.core_config_params[self.module_name] or not self.core_config_params[self.module_name]['pbjelly2_param']:
                        logger.error('Please provide [pbjelly2_param] in parameter.ini!')
                        exit(1)
                    if 'pbjelly2_xml' not in self.core_config_params[self.module_name] or not self.core_config_params[self.module_name]['pbjelly2_xml']:
                        logger.error('Please provide [pbjelly2_xml] in parameter.ini!')
                        exit(1)
                    if 'pbjelly2_threads' not in self.core_config_params[self.module_name] or not self.core_config_params[self.module_name]['pbjelly2_threads']:
                        logger.error('Please provide [pbjelly2_threads] in parameter.ini!')
                        exit(1)
                elif method_type == 'SSPACELongRead':
                    if 'sspacelongread_threads' not in self.core_config_params[self.module_name] or not self.core_config_params[self.module_name]['sspacelongread_threads']:
                        logger.error('Please provide [sspacelongread_threads] in parameter.ini!')
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
        #                Scaffolding                   #
        ################################################
        """)
        logger.info('Executing scaffolding ...')
        self.validate_config_params()

        if self.need == 1:
            method_type = self.pipeline_config_params[self.module_name]['method_type']

            current_path = os.getcwd()

            # Use raw/cleaned fastq
            if self.pipeline_config_params['long_read']['need_clean'] == '1':
                pacbio = os.path.join(current_path, self.pipeline_config_params['long_read']['workdir'], self.core_config_params['long_read']['output'])
            else:
                pacbio = self.pipeline_config_params['data']['long_reads_file']

            # Use raw/generated assembly
            if self.pipeline_config_params['assembly']['need'] == '1':
                assembly = os.path.join(current_path, self.pipeline_config_params['assembly']['workdir'], 'consensus_dir', 'final_assembly.fasta')
            else:
                if not self.pipeline_config_params['data']['assembly'] or not os.path.exists(self.pipeline_config_params['data']['assembly']):
                    logger.error('Please provide [assembly] in opt.ini!')
                    exit(1)
                assembly = self.pipeline_config_params['data']['assembly']


            workdir = self.pipeline_config_params[self.module_name]['workdir']

            os.makedirs(workdir, exist_ok=True)
            os.chdir(workdir)

            if method_type == 'PBJELLY2':
                logger.info('Running PBJELLY2 pipeline ...')

                # Split pacbio fasta
                logger.info('Splitting pacbio data ...')
                chunk_output_dirname = "chunk_output"
                split_fasta_by_size(pacbio, output_dir=chunk_output_dirname)

                thread = self.core_config_params['scaffolding']['pbjelly2_threads']
                xml = self.core_config_params['scaffolding']['pbjelly2_xml']
                blasr_param = self.core_config_params['scaffolding']['pbjelly2_param']

                link_assembly_file = "final_assembly.fasta"
                assembly_qual = os.path.splitext(link_assembly_file)[0] + '.qual'

                # generate xml by data and configuration
                pacbio_split_list = []
                for file in os.listdir(chunk_output_dirname):
                    pacbio_split_list.append(file)
                output_dir = "output"
                generate_pbjelly2_xml(link_assembly_file, thread, base_prefix=chunk_output_dirname, blasr_command=blasr_param, output=output_dir, output_file=xml, pacbio_list=pacbio_split_list)

                # Initialize command
                command_list = []
                # fakeQuals.py
                command_temp = ["ln", "-snf", "{}".format(assembly), link_assembly_file]
                command_list.append(" ".join(command_temp))
                command_temp = ["mkdir", "-p", "{}".format(output_dir)]
                command_list.append(" ".join(command_temp))
                command_temp = [self.binary_config_params[self.module_name]['pbjelly_fakequals_path']]
                command_temp.append(link_assembly_file)
                command_temp.append(assembly_qual)
                command_list.append(" ".join(command_temp))
                # fakeQuals.py should also run with splitted data
                for file in pacbio_split_list:
                    file_prefix = os.path.splitext(file)[0]
                    command_temp = [self.binary_config_params[self.module_name]['pbjelly_fakequals_path']]
                    command_temp.append(os.path.join(chunk_output_dirname, file))
                    command_temp.append(os.path.join(chunk_output_dirname, file_prefix+'.qual'))
                    command_list.append(" ".join(command_temp))

                # Jelly.py
                command_temp = [self.binary_config_params[self.module_name]['pbjelly_jelly_path'], 'setup', xml]
                command_list.append(" ".join(command_temp))
                command_temp = [self.binary_config_params[self.module_name]['pbjelly_jelly_path'], 'mapping', xml]
                command_list.append(" ".join(command_temp))
                command_temp = [self.binary_config_params[self.module_name]['pbjelly_jelly_path'], 'support', xml]
                command_list.append(" ".join(command_temp))
                command_temp = [self.binary_config_params[self.module_name]['pbjelly_jelly_path'], 'extraction', xml]
                command_list.append(" ".join(command_temp))
                command_temp = [self.binary_config_params[self.module_name]['pbjelly_jelly_path'], 'assembly', xml]
                command_temp.append('-x')
                command_temp.append('"'+"-nproc="+thread+'"')
                command_list.append(" ".join(command_temp))
                command_temp = [self.binary_config_params[self.module_name]['pbjelly_jelly_path'], 'output', xml]
                command_list.append(" ".join(command_temp))

                # Generate command bash
                bash_io = BashIO(self.bash_script)
                command = "\n".join(command_list)
                print(command)
                for command in command_list:
                    bash_io.add_core_command(command)
                bash_io.output_bash()

                # Run command bash
                bash_command = ['bash', "{}".format(self.bash_script), '|&', 'tee', "{}.log".format(self.bash_script)]
                run_bash(self.module_name, bash_command)

            elif method_type == 'SSPACELongRead':
                logger.info('Running SSPACE-LongRead pipeline ...')

                thread = self.core_config_params['scaffolding']['sspacelongread_threads']

                # Initialize command
                command_list = []

                command_temp = [self.binary_config_params[self.module_name]['sspace_longread_path']]
                command_temp.append('-c {}'.format(assembly))
                command_temp.append('-p {}'.format(pacbio))
                command_temp.append('-t {}'.format(thread))
                command_list.append(' '.join(command_temp))

                # Generate command bash
                bash_io = BashIO(self.bash_script)
                command = "\n".join(command_list)
                print(command)
                for command in command_list:
                    bash_io.add_core_command(command)
                bash_io.output_bash()

                # Run command bash
                bash_command = ['bash', "{}".format(self.bash_script), '|&', 'tee', "{}.log".format(self.bash_script)]
                run_bash(self.module_name, bash_command)

            logger.info('Scaffolding completed!')
            os.chdir(current_path)
        else:
            logger.info('Skipping scaffolding.')
