
from django.conf import settings
from django.forms import widgets
from django.utils.encoding import force_unicode
from django.utils.safestring import mark_safe
from django.forms.util import flatatt

class GoogleMapsAddressWidget(widgets.TextInput):
    "a widget that will place a google map right after the #id_address field"
    
    class Media:
        css = {'all': (settings.STATIC_URL + 'django_google_maps/css/google-maps-admin.css',),}
        js = (
            'https://ajax.googleapis.com/ajax/libs/jquery/1.4.4/jquery.min.js',
            GoogleMapsAddressWidget.build_google_maps_api_url(),
            settings.STATIC_URL + 'django_google_maps/js/google-maps-admin.js',
        )

    @staticmethod
    def build_google_maps_api_url():
        google_maps_api = 'https://maps.google.com/maps/api/js?sensor=false'
        google_api_key = getattr(settings,'GOOGLE_API_KEY', None)
        if google_api_key is not None:
            google_maps_api = '%s&key=%s' % (google_maps_api, google_api_key)
        return google_maps_api

    def render(self, name, value, attrs=None):
        if value is None:
            value = ''
        final_attrs = self.build_attrs(attrs, type=self.input_type, name=name)
        if value != '':
            # Only add the 'value' attribute if a value is non-empty.
            final_attrs['value'] = force_unicode(self._format_value(value))
        return mark_safe(u'<input%s /><div class="map_canvas_wrapper"><div id="map_canvas"></div></div>' % flatatt(final_attrs))
