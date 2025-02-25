# Copyright 2019 Creu Blanca
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

import logging
from io import StringIO

from odoo import _, models
from odoo.exceptions import UserError

_logger = logging.getLogger(__name__)

try:
    import csv
except ImportError:
    _logger.debug("Can not import csvwriter`.")


class ReportCSVAbstract(models.AbstractModel):
    _name = "report.report_csv.abstract"
    _description = "Abstract Model for CSV reports"

    def _get_objs_for_report(self, docids, data):
        """
        Returns objects for csv report.  From WebUI these
        are either as docids taken from context.active_ids or
        in the case of wizard are in data.  Manual calls may rely
        on regular context, setting docids, or setting data.

        :param docids: list of integers, typically provided by
            qwebactionmanager for regular Models.
        :param data: dictionary of data, if present typically provided
            by qwebactionmanager for TransientModels.
        :param ids: list of integers, provided by overrides.
        :return: recordset of active model for ids.
        """
        if docids:
            ids = docids
        elif data and "context" in data:
            ids = data["context"].get("active_ids", [])
        else:
            ids = self.env.context.get("active_ids", [])
        return self.env[self.env.context.get("active_model")].browse(ids)

    def create_csv_report(self, docids, data):
        objs = self._get_objs_for_report(docids, data)
        file_data = StringIO()
        if not self.csv_report_options()["fieldnames"]:
            options = {}
            if self.csv_report_options()["delimiter"]:
                options["delimiter"] = self.csv_report_options()["delimiter"]
            #file = csv.writer(file_data, delimiter=';')
            file = csv.writer(file_data, **options)
        else:
            file = csv.DictWriter(file_data, **self.csv_report_options())
        self.generate_csv_report(file, data, objs)
        file_data.seek(0)
        encoding = self._context.get("encoding")
        
        if not encoding:
            return file_data.read(), "csv"
        error_handling = self._context.get("encode_error_handling")
        if error_handling:
            return file_data.read().encode(encoding, errors=error_handling), "csv"
        try:
            return file_data.read().encode(encoding), "csv"
        except Exception as e:
            raise UserError(
                _("Failed to encode the data with the encoding set in the report.")
            ) from e

    def csv_report_options(self):
        """
        :return: dictionary of parameters. At least return 'fieldnames', but
        you can optionally return parameters that define the export format.
        Valid parameters include 'delimiter', 'quotechar', 'escapechar',
        'doublequote', 'skipinitialspace', 'lineterminator', 'quoting'.
        """
        return {"fieldnames": []}


    def generate_csv_report(self, file, data, objs):
        raise NotImplementedError()
