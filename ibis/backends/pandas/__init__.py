import ibis.config
from ibis.backends.base import BaseBackend

from .client import PandasClient, PandasDatabase, PandasTable
from .execution import execute
from .udf import udf  # noqa F401


class BasePandasBackend(BaseBackend):
    """
    Base class for backends based on pandas.
    """

    def connect(self, dictionary):
        """Construct a client from a dictionary of DataFrames.

        Parameters
        ----------
        dictionary : dict

        Returns
        -------
        Client
        """
        return self.client_class(backend=self, dictionary=dictionary)

    def from_dataframe(self, df, name='df', client=None):
        """
        convenience function to construct an ibis table
        from a DataFrame

        Parameters
        ----------
        df : DataFrame
        name : str, default 'df'
        client : Client, optional
            client dictionary will be mutated with the name of the DataFrame,
            if not provided a new client is created

        Returns
        -------
        Table
        """
        if client is None:
            return self.connect({name: df}).table(name)
        client.dictionary[name] = df
        return client.table(name)

    def register_options(self):
        ibis.config.register_option(
            'enable_trace',
            False,
            f'Whether enable tracing for {self.name} execution. '
            'See ibis.{self.name}.trace for details.',
            validator=ibis.config.is_bool,
        )


class Backend(BasePandasBackend):
    name = 'pandas'
    database_class = PandasDatabase
    table_class = PandasTable
    client_class = PandasClient

    def execute(self, *args, **kwargs):
        return execute(*args, **kwargs)
