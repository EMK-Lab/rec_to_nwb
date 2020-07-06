from rec_to_nwb.processing.nwb.components.video_files.fl_video_files_manager import FlVideoFilesManager
from rec_to_nwb.processing.nwb.components.video_files.video_files_creator import VideoFilesCreator
from rec_to_nwb.processing.nwb.components.video_files.video_files_injector import VideoFilesInjector


class VideoFilesOriginator:

    def __init__(self, raw_data_path, video_directory, video_files_metadata):
        self.video_directory = video_directory
        self.fl_video_files_manager = FlVideoFilesManager(raw_data_path, video_directory, video_files_metadata)

    def make(self, nwb_content):
        fl_video_files = self.fl_video_files_manager.get_video_files()
        for fl_video_file in fl_video_files:
            image_series = VideoFilesCreator.create(fl_video_file, self.video_directory, nwb_content)
            VideoFilesInjector.inject(nwb_content, image_series)