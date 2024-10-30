from codes.x264 import *
from codes.videoCreator import VideoCreator
from codes.uncompress import FrameExtractor
from codes.workspaceUtils import workspaceHandler
import time,os

start_time = time.time()
dataset_directory = "dataset"
output_directory = "vot_ws"
codec = x264()
compressor = VideoCreator(dataset_directory,output_directory)
uncompressor = FrameExtractor(output_directory,max_threads=12)
ws_handler = workspaceHandler(dataset_directory,output_directory)
compressor.gather_folders()

tracker_name = 'NCC_Python'

def evaluate():
    cwd=os.getcwd()
    os.chdir(os.path.join(cwd,output_directory))
    os.system(f'vot evaluate -f' + tracker_name)
    os.chdir(cwd)

def analysis(name):
    cwd=os.getcwd()
    os.chdir(os.path.join(cwd,output_directory))
    os.system(f'vot analysis --nocache --name {name} --format json ' + tracker_name)
    os.chdir(cwd)

for bitrate in codec.bitrate_step :
    codec.bitrate = bitrate
    ws_handler.copy_structure_and_files()
    compressor.get_gst_encoder_command(codec.generate_gst_encoder_command())
    compressor.run()
    uncompressor.run()
    evaluate()
    analysis(name=f"bitrate-{bitrate}")

end_time = time.time()
execution_time = end_time - start_time
print("Total Execution Time : ", execution_time)