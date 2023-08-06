from os import path
import glob
import os
import kpl_dataset.define_pb2 as define
from kpl_dataset import record
from google.protobuf.text_format import MessageToString, Parse

DEFAULT_DATA_NAME = "root"


class ReadOnlyDataset:
    def __init__(self, data_dir, data_name):
        data_name = data_name or DEFAULT_DATA_NAME
        if not path.isfile(path.join(data_dir, "{}.meta".format(data_name))):
            data_name = glob.glob("{}/*.data".format(data_dir))[0].split(".")[0]
        self._data_file = os.path.join(data_dir, "{}.data".format(data_name))
        self._index_file = os.path.join(data_dir, "{}.index".format(data_name))
        self._meta_file = os.path.join(data_dir, "{}.meta".format(data_name))
        self._data_open = False
        self._data_handle = None
        self._meta, self._index = self._read_meta_index()
        self._record_count = len(self._index) - 1
        assert self._record_count >= 0, "Dataset length < 0. please make sure close dataset after all records written"
        self._cursor = 0

    def _read_meta_index(self):
        with open(self._index_file, "rb") as fi:
            str = fi.read()
            indexes = define.Index()
            indexes.ParseFromString(str)
        with open(self._meta_file, "r") as fi:
            str = fi.read()
            meta = define.Meta()
            Parse(str, meta)
            decode_meta = record.RecordDefine.decode_meta(meta.record_type)
        return decode_meta, indexes.index

    def _init_data_handle(self):
        self._data_handle = open(self._data_file, "rb")

    def next(self):
        if not self._data_open:
            self._init_data_handle()
            self._data_open = True
        if self._cursor >= self._record_count:
            raise StopIteration
        buffer = self._data_handle.read(self._index[self._cursor + 1] - self._index[self._cursor])
        data = define.FeatureMap()
        data.ParseFromString(buffer)
        self._cursor += 1
        return record.RecordDefine.decode(data, self._meta)

    def __getitem__(self, idx):
        idx = int(idx)
        if not self._data_open:
            self._init_data_handle()
            self._data_open = True
        start = self._index[idx]
        end = self._index[idx + 1]
        self._data_handle.seek(start, 0)
        buffer = self._data_handle.read(end - start)
        data = define.FeatureMap()
        data.ParseFromString(buffer)
        self._cursor = idx
        return record.RecordDefine.decode(data, self._meta)

    def __next__(self):
        return self.next()

    def __iter__(self):
        return self

    def __len__(self):
        return self._record_count

    def reset(self):
        self._cursor = 0
        self._data_handle.seek(0)

    def close(self):
        if self._data_open:
            self._data_handle.close()


class WriteOnlyDataset:
    VERSION = 1

    def __init__(self, data_dir, data_name, record_type):
        self._data_dir = data_dir
        self._data_name = data_name or DEFAULT_DATA_NAME
        self._record_type = record_type
        self._data_handle = open(os.path.join(self._data_dir, "{}.data".format(self._data_name)), "wb")
        self._index_handle = open(os.path.join(self._data_dir, "{}.index".format(self._data_name)), "wb")
        self._meta_file = os.path.join(self._data_dir, "{}.meta".format(self._data_name))
        self._index = define.Index()
        self._index.index.append(0)
        self._last_index = 0
        self._valid_write_meta()

    def _valid_write_meta(self):
        meta = record.RecordDefine.encode_meta(self._record_type, self._data_name, self.VERSION)
        with open(self._meta_file, "w") as fo:
            fo.write(MessageToString(meta))
            fo.close()

    def write(self, value):
        example = record.RecordDefine.encode(value, self._record_type)
        example = example.SerializeToString()
        deserilized = define.FeatureMap()
        deserilized.ParseFromString(example)
        self._last_index += len(example)
        self._index.index.append(self._last_index)
        self._data_handle.write(example)

    def close(self):
        self._data_handle.close()
        self._index_handle.write(self._index.SerializeToString())
        self._index_handle.close()
