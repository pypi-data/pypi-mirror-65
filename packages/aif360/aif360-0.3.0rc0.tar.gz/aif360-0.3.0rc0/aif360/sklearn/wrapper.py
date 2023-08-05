from sklearn.base import BaseEstimator, MetaEstimatorMixin, clone

def aif360_wrap(transformer):
    def add_index_to_output(func):
        def transform(X, *args, **kwargs):
            out = func(X, *args, **kwargs)
            if out.ndims == 1:
                return pd.Series(out, index=X.index)
            else:
                return pd.DataFrame(out, index=X.index)
        return transform

    class Wrapped():
        def __init__(self, *args, **kwargs):
            self._instance = transformer(*args, **kwargs)

        def __getattribute__(self, attr):
            obj = self._instance.__getattribute__(attr)
            if attr == 'transform' or attr == 'fit_transform':
                return add_index_to_output(obj)
            else:
                return obj
