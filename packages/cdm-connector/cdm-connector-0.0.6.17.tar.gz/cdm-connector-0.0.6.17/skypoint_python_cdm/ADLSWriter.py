from .Writer import Writer
from azure.storage.blob import BlockBlobService
import json
import pandas as pd
import numpy as np


class ADLSWriter(Writer):
    """
        Write dataframe/json to specified blob storage location
    """
    def __init__(self, account_name, account_key, container_name, storage_name, dataflow_name):
        self.account_name = account_name
        self.account_key = account_key
        self.container_name = container_name
        self.storage_name = storage_name
        self.dataflow_name = dataflow_name

    def create_snapshot(self, location, snapshot_dir_name):
        """
            Create a snapshot of the file current file in the passed directory name
            location: dir1/dir2/dir3/filename.extension or "model.json"
            snashot_dir_name: Snapshot directory name
        """
        if location.strip() == "model.json":
            location = self.dataflow_name + "/" + location

        exists = block_blob_service.exists(self.container_name, location)
        if not exists:
            return False

        t = datetime.datetime.now().strftime('%d-%M-%Y-%H-%M-%S')
        file_path, filename = '/'.join(location.split('/')[:-1]), location.split('/')[-1]
        
        # copy file into snapshot folder
        old_blob_url = block_blob_service.make_blob_url(self.container_name, location)
        block_blob_service.copy_blob(self.container_name, file_path + '/' + snapshot_folder_name + '/' + filename + '@snapshot' + t, old_blob_url)
        new_blob_url = block_blob_service.make_blob_url(container_name, file_path + '/' + snapshot_folder_name + '/' + filename + '@snapshot' + t)
        
        # Delete old file
        block_blob_service.delete_blob(container_name, filename)
        return True
    
    def write_df(self, blob_location, dataframe, number_of_partition=5):
        """
            Write dataframe to specified blob storage location
        """
        block_blob_service = BlockBlobService(account_name=self.account_name, account_key=self.account_key)
        dfs = np.array_split(dataframe, number_of_partition)
        result = list()

        entity_name = blob_location.split('/')[0]
        blob_location = blob_location + "/" + entity_name
        for i in range(len(dfs)):
            dataframe = dfs[i].to_csv(index=False, header=False)
            filename = blob_location + str(i) + ".csv"
            block_blob_service.create_blob_from_text(self.container_name + "/" + self.dataflow_name, 
                                                     filename, dataframe)
            blob_url = 'https://' + self.storage_name + '.dfs.core.windows.net/' + self.container_name + '/' + filename
            result.append((filename, blob_url))
        return result

    def write_json(self, blob_location, json_dict):
        """
        write json to specified blob storage location
        """
        json_dict = json.dumps(json_dict)
        block_blob_service = BlockBlobService(
            account_name=self.account_name, account_key=self.account_key)
        block_blob_service.create_blob_from_text(self.container_name, self.dataflow_name+"/"+ blob_location, json_dict)
        blob_url = 'https://'+self.storage_name+'.dfs.core.windows.net/'+self.container_name+'/'+blob_location
        return blob_url
