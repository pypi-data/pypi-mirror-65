import glob
import logging
import os
import re
import tempfile
from typing import List, Optional
import attr

from rho_ml.rho_model import RhoModel
from rho_ml.stored_model import StoredModel

logger = logging.getLogger(__name__)


def combine_model_name_and_version(model_name: str, model_version: str) -> str:
    return model_name + '_' + model_version


def get_storage_key(model: RhoModel) -> str:
    """ Combine model name and version to get a key for storing and retrieving a
    model. """
    return combine_model_name_and_version(
        model_name=model.name, model_version=model.version.to_string())


class PipelineStorageConfig(object):
    def store(self, model: RhoModel, base_class_name: Optional[str] = None):
        raise NotImplementedError

    def retrieve(self, *args, **kwargs) -> RhoModel:
        raise NotImplementedError

    def get_key_from_pattern(self,
                             model_name: str,
                             version_pattern: str) -> str:
        """ Given some pattern of the form 'name-1.2.3', 'name-1.2.*', or
        'name-1.*', etc., return the key that should be """
        raise NotImplementedError


@attr.s(auto_attribs=True)
class LocalModelStorage(PipelineStorageConfig):
    base_path: str = attr.ib(default=tempfile.gettempdir())

    def store(self, model: RhoModel, base_class_name: Optional[str] = None):
        stored_predictor = StoredModel.from_model(
            model=model, base_class_name=base_class_name)
        storage_key = get_storage_key(model=model)
        storage_path = os.path.join(self.base_path, storage_key)
        with open(storage_path, 'wb') as f:
            f.write(stored_predictor.to_pickle())

    def retrieve(self, key: str) -> RhoModel:
        storage_path = os.path.join(self.base_path, key)
        with open(storage_path, 'rb') as f:
            stored_predictor = StoredModel.from_pickle(f.read())
        predictor = stored_predictor.load_model()
        return predictor

    def get_key_from_pattern(self,
                             model_name: str,
                             version_pattern: str) -> str:
        search_pattern = combine_model_name_and_version(
            model_name=model_name, model_version=version_pattern)
        search_path = os.path.join(self.base_path, search_pattern)
        local_candidates = glob.glob(search_path)
        result_key = find_highest_compatible_version(
            search_version=version_pattern, available_keys=local_candidates)
        return result_key


def validate_model_version(model_version):
    """ Model version must conform to semver but can include wildcards.
    """
    pattern = re.compile(r"^[0-9\*]+\.[0-9\*]+\.[0-9\*]+$")
    if not pattern.match(model_version):
        raise ValueError("Invalid model_version format ({0}). Must conform "
                         "to semver with wildcards allowed. "
                         "e.g. 1.1.1, 1.*.*".format(model_version))
    return model_version


def find_highest_compatible_version(
        search_version: str,
        available_keys: List[str],
        prefix_pattern: str = r"(.*)\_",
        version_pattern: str = r"(\d+\.\d+\.\d+)(.*)"
):
    """ Return the key of the highest compatible model version.

        Args:
            search_version (string): The version to search. This can include
                wildcards. E.g. "1.0.0", "2.*.*", "1.1.*"
            available_keys (list): List of full model keys with prefix
                and version, e.g.
                ['model_prefix_0.0.0', 'model_prefix_0.1.0']
            prefix_pattern (r string): Regex pattern describing any prefix
                that may be prepended to the search version. Pass as None
                to exclude a prefix pattern (e.g. if your available_keys is a
                list of only version nums ['0.1.1', '0.1.2']). NOTE: This
                pattern must currently consist of exactly one regex group.
            version_pattern (r string): Regex pattern describing version
                numbers. NOT recommended to modify this pattern, as the logic
                assumes semver, which is default version pattern provided.
        Returns:
            string: string with major, minor, patch of highest
                compatible version found in available keys based on the
                search version. e.g. "0.1.0"
                e.g. if search version is "0.1.*" & available keys includes
                ['my_prefix_0.1.1', 'my_prefix_1.0.0', 'my_prefix_0.1.5']
                this will return my_prefix_0.1.5
    """
    search_version = validate_model_version(search_version)

    search_pattern = re.compile(version_pattern)
    group_index = 1
    if prefix_pattern is not None:
        group_index = 2
        search_pattern = re.compile(prefix_pattern + version_pattern)

    def _run_search(available_keys, v_index, version_elements):
        """ Loop through all keys to identify highest compatible.
            This is called sequentially for major, minor, patch.

            Args:
                available_keys (list): List of full model keys with prefix
                    and version, e.g.
                    ['model_prefix_0.0.0', 'model_prefix_0.1.0']
                v_index (int): The index of the model version to find. 0 is
                    major, 1 is minor, 2 is patch.
                version_elements (list): List of integers representing the
                    indices of version elements that have already been
                    found. The first element is always major, second is
                    minor, third is patch. e.g. [0, 1, 0] == "0.1.0"
            Returns:
                string: string with major, minor, patch of highest
                    compatible version found in available keys based on the
                    search version. e.g. "0.1.0"
        """
        highest_compatible_num = -1  # Haven't found anything yet
        for available_version in available_keys:
            groups = search_pattern.search(available_version)
            if groups is None:
                continue

            this_version = groups.group(group_index)  # e.g. 0.0.0

            # Skip this available_version if it has a version element
            # > something we've already found. e.g. if we already found
            # major version 1 as the max, and this is major version 0,
            # then it doesn't matter what the value of this_num is because
            # it's already incompatible. This can only ever ben 3 elements
            # when following semver, so hardcode.
            incompatible_previous_version_num = False
            for i in range(len(version_elements)):
                if version_elements[i] is None \
                        or int(this_version.split(".")[i]) \
                        != version_elements[i]:
                    incompatible_previous_version_num = True

            if incompatible_previous_version_num:
                continue

            # We only compare one version num (major/minor/patch) at a time
            this_num = int(this_version.split(".")[v_index])

            # The 'search_num' can include wildcards, which means it
            # can be anything. If it's an int, then this_num must be
            # equal to the search_num.
            search_num = search_version.split(".")[v_index]
            if search_num == "*":
                if this_num > highest_compatible_num:
                    highest_compatible_num = this_num
            else:
                search_num = int(search_num)
                if this_num > highest_compatible_num \
                        and this_num == search_num:
                    highest_compatible_num = this_num

        if highest_compatible_num == -1:
            return None
        return highest_compatible_num

    version_elements = []
    for element_idx in range(3):
        version_elements.append(
            _run_search(available_keys, element_idx, version_elements)
        )

    if any(v is None for v in version_elements):
        logger.warning("Unable to find compatible version for {0} from: {1}"
                       .format(search_version, available_keys))
        return None

    highest_version = str(version_elements[0]) + "." \
                      + str(version_elements[1]) \
                      + "." + str(version_elements[2])

    # Return the whole key that has the discovered version.
    for key in available_keys:
        if highest_version in key.split('_')[-1]:
            return key

    return None
