import os
import subprocess
import time

class VideoCreator:
    def __init__(self, dataset_directory, output_directory):
        self.dataset_directory = dataset_directory
        self.output_directory = output_directory
        self.gst_encoder_command = []
        self.folders_to_process = []

    def create_video_from_images(self, image_folder, output_video):
        """Creates an MP4 video from BMP images in the specified folder."""
        gst_source_command = [
            "/usr/bin/gst-launch-1.0",
            "multifilesrc", f"location={image_folder}/%08d.bmp",
            "caps=\"image/bmp,framerate=30/1\"",
            "!", "avdec_bmp",
            "!", "videoconvert"
        ]

        gst_sink_command = [
            "!", "mp4mux",
            "!", "filesink", f"location={output_video}"
        ]
        gst_command = gst_source_command + self.gst_encoder_command + gst_sink_command
        try:
            print("Executing command:", ' '.join(gst_command))
            subprocess.run(gst_command, check=True)
        except subprocess.CalledProcessError as e:
            print(f"Error creating video from {image_folder}: {e}")

    def process_folder(self, folder):
        """Processes a single folder to create a video."""
        output_video = os.path.join(self.output_directory, "sequences", os.path.basename(os.path.dirname(folder)), f"{os.path.basename(os.path.dirname(folder))}.mp4")
        print("---------------->", output_video)
        self.create_video_from_images(folder, output_video)

    def gather_folders(self):
        """Gathers all folders containing BMP images."""
        sequences = open(os.path.join(self.dataset_directory, "list.txt")).read().splitlines()
        for sequence in sequences:
            sequence_folder = os.path.join(self.dataset_directory, sequence, "color")
            if any(fname.endswith(".bmp") for fname in os.listdir(sequence_folder)):
                self.folders_to_process.append(sequence_folder)

    def get_gst_encoder_command(self, gst_encoder_command):
        self.gst_encoder_command = gst_encoder_command

    def run(self):
        """Main function to find all image folders and process them sequentially."""
        #self.gather_folders()
        start_time = time.time()  # Start time

        # Sequentially process each folder
        for folder in self.folders_to_process:
            print("Folder is --->> ",folder)
            self.process_folder(folder)

        end_time = time.time()  # End time
        total_time = end_time - start_time  # Calculate total execution time
        print(f"Total execution time: {total_time:.2f} seconds")

# if __name__ == "__main__":
#     dataset_directory = 'dataset'  # Replace with your actual path
#     output_directory = 'output'   # Replace with your desired output path
#     video_creator = VideoCreator(dataset_directory, output_directory)
#     video_creator.run()
