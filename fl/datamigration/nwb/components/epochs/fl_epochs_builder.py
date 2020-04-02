from fl.datamigration.nwb.components.epochs.fl_epochs import FlEpochs


class FlEpochsBuilder:

    def __init__(self, tags, tasks):
        self.tags = tags
        self.tasks = tasks

    def build(self, epochs_extracted_session_times):
        return FlEpochs(
            epochs_extracted_session_times[0],
            epochs_extracted_session_times[1],
            self.tags,
            self.tasks
        )