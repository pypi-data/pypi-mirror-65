import os
import pandas as pd
from finka.dart.lib import Dart


def test_corp_codes():
    dart = Dart(os.environ.get('DART_API_KEY'))
    data = dart.get_corp_codes()
    assert isinstance(data, pd.DataFrame)
    assert data.shape[0] > 50000
