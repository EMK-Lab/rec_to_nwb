from src.datamigration.exceptions.missing_data_exception import MissingDataException
from src.datamigration.nwb_builder.managers.pos_data_manager import PosDataManager
from src.datamigration.nwb_builder.managers.pos_timestamp_manager import PosTimestampManager
from src.datamigration.nwb_builder.nwb_builder_tools.data_iterator import DataIterator, DataIterator1D


class PositionExtractor:
    def __init__(self, datasets):
        self.datasets = datasets
        self.all_pos = []
        self.continuous_time = []

        self.__extract_data()

    def __extract_data(self):
        for dataset in self.datasets:
            data_from_current_dataset = [dataset.get_data_path_from_dataset('pos') + pos_file for pos_file in
                                         dataset.get_all_data_from_dataset('pos') if
                                         (pos_file.endswith('.pos_online.dat'))]
            if data_from_current_dataset is None or dataset.get_continuous_time() is None:
                raise MissingDataException("Incomplete data in dataset "
                                           + str(dataset.name)
                                           + "missing continuous time file")
            self.all_pos.append(data_from_current_dataset)
            self.continuous_time.append(dataset.get_continuous_time())

    def get_position(self):
        pos_data = PosDataManager(directories=self.all_pos)
        return DataIterator(pos_data)

    def get_timestamps(self):
        pos_timestamps = PosTimestampManager(directories=self.all_pos,
                                             continuous_time_directories=self.continuous_time)
        return DataIterator1D(pos_timestamps)
