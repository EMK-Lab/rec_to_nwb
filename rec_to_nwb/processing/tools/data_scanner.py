import fnmatch
import os

from rec_to_nwb.processing.exceptions.missing_data_exception import MissingDataException
from rec_to_nwb.processing.metadata.metadata_manager import MetadataManager
from rec_to_nwb.processing.tools.beartype.beartype import beartype
from rec_to_nwb.processing.tools.dataset import Dataset
from rec_to_nwb.processing.tools.file_sorter import FileSorter


class DataScanner:

    @beartype
    def __init__(self, data_path: str, animal_name: str, nwb_metadata: MetadataManager):

        self.data_path = data_path
        self.animal_name = animal_name
        self.nwb_metadata = nwb_metadata
        self.data = None

    @beartype
    def get_all_epochs(self, date: str) -> list:
        all_datasets = []
        path_curr = os.path.join(self.data_path,
                                 self.animal_name,
                                 'preprocessing',
                                 date)
        directories = os.listdir(path_curr)
        FileSorter.sort_filenames(directories)
        # print(directories)
        for directory in directories:
            if directory.startswith(date):
                dataset_name = (directory.split('_')[2] + '_' + directory.split('_')[3]).split('.')[0]
                # print(dataset_name)
                if not dataset_name in all_datasets:
                    all_datasets.append(dataset_name)
        return all_datasets

    @beartype
    def get_all_data_from_dataset(self, date: str) -> list:
        path_curr = os.path.join(self.data_path,
                                 self.animal_name,
                                 'preprocessing',
                                 date)
        self.__check_if_path_exists(path_curr)

        return os.listdir(path_curr)

    @beartype
    def extract_data_from_date_folder(self, date: str):
        self.data = {self.animal_name: self.__extract_experiments(self.data_path, self.animal_name, [date])}
        print(self.data)

    @beartype
    def extract_data_from_dates_folders(self, dates: list):
        self.data = {self.animal_name: self.__extract_experiments(self.data_path, self.animal_name, dates)}
        print(self.data)

    def extract_data_from_all_dates_folders(self):
        self.data = {self.animal_name: self.__extract_experiments(self.data_path, self.animal_name, None)}
        print(self.data)

    def __extract_experiments(self, data_path, animal_name, dates):
        preprocessing_path = os.path.join(data_path,
                                          animal_name,
                                          'preprocessing')
        if not dates:
            dates = FileSorter.sort_filenames(os.listdir(preprocessing_path))

        return {date: self.__extract_datasets(os.path.join(preprocessing_path, date)) for date in dates}

    @staticmethod
    def __extract_datasets(date_path):
        existing_datasets = set()
        datasets = {}
        directories = FileSorter.sort_filenames(os.listdir(date_path))

        for directory in directories:
            #print('directory', directory)
            dir_split = directory.split('_')
            if dir_split[0].isdigit():
                dir_last_part = dir_split.pop().split('.')
                dataset_name = dir_split.pop() + '_' + dir_last_part[0]
                #print('dir_last_part', dir_last_part)
                #print('dataset_name', dataset_name)
                if not (dataset_name in existing_datasets):
                    datasets[dataset_name] = Dataset(dataset_name)
                    existing_datasets.add(dataset_name)
                for dataset in datasets.values():
                    if dataset_name == dataset.name:

                        path_curr = os.path.join(date_path,
                                                 directory
                                                 )
                        print('path_curr', path_curr)
                        print('dir_last_part', dir_last_part)
                        dataset.add_data_to_dataset(path_curr, dir_last_part.pop())
        print(datasets)
        return datasets

    @beartype
    def get_all_animals(self) -> list:
        return list(self.data.keys())

    @beartype
    def get_all_experiment_dates(self, animal: str) -> list:
        return list(self.data[animal].keys())

    @beartype
    def get_all_datasets(self, animal: str, date: str) -> list:
        return list(self.data[animal][date].keys())

    @beartype
    def get_mda_timestamps(self, animal: str, date: str, dataset: str):
        for file in self.data[animal][date][dataset].get_all_data_from_dataset('mda'):
            if file.endswith('timestamps.mda'):
                return str(Path(f"{self.data[animal][date][dataset].get_data_path_from_dataset('mda')}/{file}"))
        return None

    @staticmethod
    @beartype
    def get_probes_from_directory(path: str):
        probes = []
        files = FileSorter.sort_filenames(os.listdir(path))
        for probe_file in files:
            if fnmatch.fnmatch(probe_file, "probe*.yml"):
                path_curr = os.path.join(path, probe_file)
                probes.append(path_curr)
        return probes

    def __check_if_path_exists(self, path):
        if not (os.path.exists(path)):
            raise MissingDataException('missing ' + self.data_path + ' directory')
