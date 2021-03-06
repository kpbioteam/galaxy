import logging

from galaxy.tools.actions import upload_common
from galaxy.util import ExecutionTimer
from . import ToolAction

log = logging.getLogger(__name__)


class UploadToolAction(ToolAction):

    def execute(self, tool, trans, incoming={}, set_output_hid=True, history=None, **kwargs):
        dataset_upload_inputs = []
        for input_name, input in tool.inputs.items():
            if input.type == "upload_dataset":
                dataset_upload_inputs.append(input)
        assert dataset_upload_inputs, Exception("No dataset upload groups were found.")

        persisting_uploads_timer = ExecutionTimer()
        incoming = upload_common.persist_uploads(incoming, trans)
        log.debug("Persisted uploads %s" % persisting_uploads_timer)
        check_timer = ExecutionTimer()
        # We can pass an empty string as the cntrller here since it is used to check whether we
        # are in an admin view, and this tool is currently not used there.
        uploaded_datasets = upload_common.get_uploaded_datasets(trans, '', incoming, dataset_upload_inputs, history=history)

        if not uploaded_datasets:
            return None, 'No data was entered in the upload form, please go back and choose data to upload.'

        log.debug("Checked uploads %s" % check_timer)
        create_job_timer = ExecutionTimer()
        json_file_path = upload_common.create_paramfile(trans, uploaded_datasets)
        data_list = [ud.data for ud in uploaded_datasets]
        rval = upload_common.create_job(trans, incoming, tool, json_file_path, data_list, history=history)
        log.debug("Created upload job %s" % create_job_timer)
        return rval
