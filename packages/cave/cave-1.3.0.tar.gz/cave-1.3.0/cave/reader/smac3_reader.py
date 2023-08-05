import os
import shutil
import typing

from ConfigSpace.configuration_space import ConfigurationSpace, Configuration
from ConfigSpace.hyperparameters import FloatHyperparameter, IntegerHyperparameter, Constant, CategoricalHyperparameter
from ConfigSpace.read_and_write import json as pcs_json
from smac.runhistory.runhistory import RunHistory
from smac.scenario.scenario import Scenario
from smac.utils.io.input_reader import InputReader
from smac.utils.io.traj_logging import TrajLogger

from cave.reader.base_reader import BaseReader, changedir


class SMAC3Reader(BaseReader):

    def get_scenario(self):
        run_1_existed = os.path.exists('run_1')
        in_reader = InputReader()
        # Create Scenario (disable output_dir to avoid cluttering)
        scen_fn = os.path.join(self.folder, 'scenario.txt')
        if not os.path.isfile(scen_fn):
            scen_fn = self.get_glob_file(self.folder, 'scenario.txt')
        scen_dict = in_reader.read_scenario_file(scen_fn)
        scen_dict['output_dir'] = ""

        with changedir(self.ta_exec_dir):
            # We always prefer the less error-prone json-format if available:
            pcs_fn = scen_dict.get('pcs_fn', 'no_pcs_fn')
            cs_json = os.path.join(os.path.dirname(pcs_fn), 'configspace.json')
            if not pcs_fn.endswith('.json') and os.path.exists(cs_json):
                self.logger.debug("Detected, '%s' ignoring '%s'", cs_json, pcs_fn)
                with open(cs_json, 'r') as fh:
                    scen_dict['cs'] = pcs_json.read(fh.read())
                    scen_dict['pcs_fn'] = cs_json

            self.logger.debug("Creating scenario from '%s'", self.ta_exec_dir)
            scen = Scenario(scen_dict)

        if (not run_1_existed) and os.path.exists('run_1'):
            shutil.rmtree('run_1')
        return scen

    def get_runhistory(self, cs):
        """
        Returns
        -------
        rh: RunHistory
            runhistory
        """
        rh_fn = os.path.join(self.folder, 'runhistory.json')
        if not os.path.isfile(rh_fn):
            rh_fn = self.get_glob_file(self.folder, 'runhistory.json')
        rh = RunHistory()
        try:
            rh.load_json(rh_fn, cs)
        except FileNotFoundError:
            self.logger.warning("%s not found. trying to read SMAC3-output, "
                                "if that's not correct, change it with the "
                                "--format option!", rh_fn)
            raise
        return rh

    def get_validated_runhistory(self, cs):
        """
        Returns
        -------
        validated_rh: RunHistory
            runhistory with validation-data, if available
        """
        rh_fn = os.path.join(self.folder, 'validated_runhistory.json')
        rh = RunHistory(average_cost)
        try:
            rh.load_json(rh_fn, cs)
        except FileNotFoundError:
            self.logger.warning("%s not found. trying to read SMAC3-validation-output, "
                                "if that's not correct, change it with the "
                                "--validation_format option!", rh_fn)
            raise
        return rh

    def get_trajectory(self, cs):
        def alternative_configuration_recovery(config_list: typing.List[str], cs: ConfigurationSpace):
            """ Used to recover ints and bools as categoricals or constants from trajectory """
            config_dict = {}
            for param in config_list:
                k,v = param.split("=")
                v = v.strip("'")
                hp = cs.get_hyperparameter(k)
                if isinstance(hp, FloatHyperparameter):
                    v = float(v)
                elif isinstance(hp, IntegerHyperparameter):
                    v = int(v)
                ################# DIFFERENCE: ################
                elif isinstance(hp, CategoricalHyperparameter) or isinstance(hp, Constant):
                    if isinstance(hp.default_value, bool):
                        v = True if v == 'True' else False
                    elif isinstance(hp.default_value, int):
                        v = int(v)
                    elif isinstance(hp.default_value, float):
                        v = float(v)
                    else:
                        v = v
                ##############################################
                config_dict[k] = v
            config = Configuration(configuration_space=cs, values=config_dict)
            config.origin = "External Trajectory"
            return config

        TrajLogger._convert_dict_to_config = alternative_configuration_recovery


        traj_fn = os.path.join(self.folder, 'traj_aclib2.json')
        if not os.path.isfile(traj_fn):
            traj_fn = self.get_glob_file(self.folder, 'traj_aclib2.json')
        traj = TrajLogger.read_traj_aclib_format(fn=traj_fn, cs=cs)
        return traj

    @classmethod
    def check_for_files(cls, path):
        for f in ["scenario.txt", 'runhistory.json', "traj_aclib2.json"]:
            if not (cls.get_glob_file(path, f, 0)
                    or os.path.isfile(os.path.join(path, f))):
                break
        else:
            return True
        return False
