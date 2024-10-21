import os
import shutil

class workspaceHandler:
    def __init__(self,dataset_directory,workspace_directory):
        self.dataset_directory = dataset_directory
        self.workspace_directory = workspace_directory 
        self.sequences = []
        pass

    # def read_list_txt(self):
    #     """Gathers all folders containing BMP images."""
    #     self.sequences = open(os.path.join(self.dataset_directory, "list.txt")).read().splitlines()

    # def create_sequence_folders(self):        
    #     for sequence in self.sequences:
    #         sequence_folder = os.path.join(self.workspace_directory,"sequences", sequence)
    #         os.makedirs(sequence_folder)
    
    def copy_structure_and_files(self):
        # Iterate over all items in the dataset directory
        for root, dirs, files in os.walk(self.dataset_directory):
            # Determine the relative path from dataset_directory to the current root
            relative_path = os.path.relpath(root, self.dataset_directory)
            
            # Create the corresponding destination folder, excluding 'color' folders
            if 'color' not in relative_path:
                dest_folder = os.path.join(self.workspace_directory,"sequences", relative_path)
                os.makedirs(dest_folder, exist_ok=True)
                
                # Copy all files in the current directory to the destination directory
                for file in files:
                    source_file = os.path.join(root, file)
                    dest_file = os.path.join(dest_folder, file)
                    shutil.copy2(source_file, dest_file)
                    print(f"Copied {source_file} to {dest_file}")
    
    def delete_sequences_folder(self):
        sequences_folder = os.path.join(self.workspace_directory,"sequences")
        try:
            shutil.rmtree(sequences_folder)
            print(f"Successfully deleted {sequences_folder}")
        except FileNotFoundError:
            print(f"The directory {sequences_folder} does not exist.")
        except PermissionError:
            print(f"Permission denied: unable to delete {sequences_folder}")
        except Exception as e:
            print(f"Error occurred: {e}")


# if __name__ == "__main__":
#     dataset_directory = 'dataset'  # Replace with your actual path
#     workspace_directory = 'ws'
#     ws_handler = workspaceHandler(dataset_directory,workspace_directory)
#     ws_handler.copy_structure_and_files()
        