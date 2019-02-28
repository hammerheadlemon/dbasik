import logging
import os

from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.conf import settings
from django.contrib import messages
from django.core.files.storage import default_storage
from django.core.files.uploadedfile import UploadedFile
from django.urls import reverse_lazy
from django.views.generic import FormView

from excelparser.forms import ProcessPopulatedTemplateForm
from excelparser.helpers.parser import ParsedSpreadsheet

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class ProcessPopulatedTemplate(FormView):
    form_class = ProcessPopulatedTemplateForm
    template_name = "excelparser/process_populated_template.html"

    def get_initial(self):
        return {'return_obj': self.kwargs['return_id']}

    def get_success_url(self):
        return str(reverse_lazy("returns:return_data", args=[self.kwargs['return_id']]))

    def form_invalid(self, form):
        error_msg = form.errors.get('source_file')
        if error_msg:
            messages.add_message(self.request, messages.ERROR, f"{error_msg}")
            return redirect("excelparser:process_populated", self.kwargs['return_id'])
        else:
            return redirect("excelparser:process_populated", self.kwargs['return_id'])


    def form_valid(self, form):
        logger.info("Trying to parse form {}".format(form))
        uploaded_file: UploadedFile = self.request.FILES['source_file']
        save_path = os.path.join(settings.MEDIA_ROOT, 'uploads', uploaded_file.name)
        path = default_storage.save(save_path, uploaded_file)
        project = form.cleaned_data['return_obj'].project
        return_obj = form.cleaned_data['return_obj']
        datamap = form.cleaned_data['datamap']
        use_datamap_types = form.cleaned_data['use_datamap_types']
        try:
            logger.info("Trying to parse spreadsheet {}".format(save_path))
            parsed_spreadsheet = ParsedSpreadsheet(path, project, return_obj, datamap, use_datamap_types)
        except Exception:
            messages.add_message(self.request, messages.ERROR, f"ERROR uploading file: {uploaded_file}. Please check that it is a valid template.")
            return redirect("excelparser:process_populated", self.kwargs['return_id'])
        parsed_spreadsheet.process()
        return HttpResponseRedirect(self.get_success_url())
