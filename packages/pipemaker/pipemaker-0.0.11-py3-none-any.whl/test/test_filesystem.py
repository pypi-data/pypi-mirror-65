import pytest
import pandas as pd
from pipemaker.filesystem import Filepath
from pipemaker.utils.defaultlog import log


@pytest.mark.parametrize("fs1", ["", "s3://registr1", "googledrive://"])
@pytest.mark.parametrize("ext", [".pkl", ".xlsx", ".csv"])
def test_filepath(fs1, ext, request):
    """ test exists, save, load, remove """

    # setup
    temp_fp = Filepath(f"{fs1}/pytest/{request.function.__name__}")
    temp_fp.makedirs(recreate=True)
    value = pd.DataFrame([12])

    # exists
    fp = Filepath(f"{temp_fp.url}/file1{ext}")
    assert fp.exists() == False

    # save
    fp.save(value)
    assert fp.exists()

    # load
    loaded = fp.load()
    assert loaded.equals(value)

    # remove
    fp.remove()
    assert fp.exists() == False
