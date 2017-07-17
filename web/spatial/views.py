from django import forms
from django.views.generic.edit import FormView
from spatial.utils import reverse_geocode

class LatLonForm(forms.Form):
    lat = forms.CharField(label="Latitude", initial='36.372306')
    lon = forms.CharField(label="Longitude", initial='127.365111')

class ReverseGeocodeView(FormView):
    template_name = 'form.html'
    form_class = LatLonForm

    def form_valid(self, form, **kwargs):
        result = reverse_geocode(form.cleaned_data['lat'], form.cleaned_data['lon'])
        context = self.get_context_data(**kwargs)
        context['result'] = result
        context['form'] = form
        return self.render_to_response(context)
