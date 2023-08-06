import dash_core_components as dcc
import dash_html_components as html

from turbo_dash.dashboard_components import TurboHeader, TurboLogo, TurboLinks, TurboLink
from turbo_dash.inputs import TurboInput, TurboFilter
from turbo_dash.outputs import TurboOutput


class turbo_dash:

    def __init__(
            self,
            app_to_callback,
            list_of_inputs=None,
            list_of_outputs=None,
            header_object=None,
            layout_template=None,
            inputs_class_name=None,
            outputs_class_name=None,
            turbo_header_logo_file_path=None,
            turbo_header_links_list=None,
            turbo_img_link=None
    ):
        """quickly create a dashboard by providing a list of inputs and outputs

        :param app_to_callback: dash app we want to make reactive (i.e. call back)
        :param list_of_inputs: optional, list of TurboInput objects to use in our dashboard
        :param list_of_outputs: optional, list of TurboOutput objects to use in our dashboard
        :param header_object: optional, TurboHeader object to display
        :param layout_template: optional, template to use for the layout
        :param inputs_class_name: optional, css class name for the inputs div
        :param outputs_class_name: optional, css class name for the outputs div
        :param turbo_header_logo_file_path: optional, if using a template you can create the logo with just a file path
        :param turbo_header_links_list: optional, if using a template you can create the header links with a list of
            dictionaries that looks like: [{'href': '/app1', 'text': 'app1'}]
            you may also add an optional link_class_name arg in the dictionary
        :param turbo_img_link: optional, if using the homepage or 404 template you can display an image
        """
        self.app_to_callback = app_to_callback
        self.list_of_inputs = list_of_inputs
        self.list_of_outputs = list_of_outputs
        self.header_object = header_object
        self.layout_template = layout_template
        self.inputs_class_name = inputs_class_name
        self.outputs_class_name = outputs_class_name
        self.turbo_header_logo_file_path = turbo_header_logo_file_path
        self.turbo_header_links_list = turbo_header_links_list
        self.turbo_img_link = turbo_img_link

        # bad code alert: if we didn't provide lists of inputs or outputs, set it to an empty list
        if self.list_of_inputs is None:
            self.list_of_inputs = []
        if self.list_of_outputs is None:
            self.list_of_outputs = []

        # if we provided a header object, grab the html
        if self.header_object is None:
            self.header_html = None
        else:
            self.header_html = self.header_object.html

        self.layout = self.create_layout()

    @property
    def callbacks(self):
        for o in self.list_of_outputs:
            o.callback(app_to_callback=self.app_to_callback)

        return True

    def create_layout(self):
        if self.layout_template is None or self.layout_template == 'default':
            # default layout, no divs or classes
            return html.Div(
                children=[
                    self.header_html,
                    html.Div(
                        className=self.inputs_class_name,
                        children=[i.html for i in self.list_of_inputs]
                    ),
                    html.Div(
                        className=self.outputs_class_name,
                        children=[o.html for o in self.list_of_outputs]
                    ),
                ],
            )

        elif self.layout_template == 'turbo':
            header_html = self.create_header_for_template()

            return html.Div(
                children=[
                    header_html,  # /header
                    html.Div(  # sidebar-and-content
                        className='sidebar-and-content',
                        children=[
                            html.Div(  # sidebar
                                className='sidebar',
                                children=[i.html for i in self.list_of_inputs]
                            ),  # /sidebar
                            html.Div(  # content
                                className='content',
                                children=[o.html for o in self.list_of_outputs]
                            ),  # /sidebar
                        ]
                    ),  # /sidebar-and-content
                ],
            )

        elif self.layout_template in ('homepage', '404'):
            header_html = self.create_header_for_template()

            return html.Div(
                children=[
                    header_html,
                    html.Div(
                        className='sidebar-and-content',
                        style={'text-align': 'center', 'display': 'block'},
                        children=html.Img(src=self.turbo_img_link),
                    ),
                ]
            )

        # who are you? who who, who who
        else:
            raise ValueError(
                """I don't know what to do with a "{}" layout template. Please add it to {}."""
                .format(self.layout_template, __file__)
            )

    def create_header_for_template(self):
        # if we're given some header html, use it
        if self.header_html is not None:
            return self.header_html

        # if we weren't given header html and we were given some info, use that
        elif self.turbo_header_logo_file_path is not None or self.turbo_header_links_list is not None:
            # make the logo if we were given the input
            if self.turbo_header_logo_file_path is not None:
                logo_object = TurboLogo(
                    logo_class_name='logo',
                    logo_file_path=self.turbo_header_logo_file_path,
                    logo_href='/',
                    logo_width='120px',
                )
            else:
                logo_object = None

            # make the links if we were given the input
            if self.turbo_header_links_list is not None:
                links_object = TurboLinks(
                    list_of_link_objects=[  # comprehend the link list
                        TurboLink(
                            link_href=dct['href'],
                            link_class_name=dct.get('link_class_name', 'header-link'),
                            link_text=dct['text'],
                        ) for dct in self.turbo_header_links_list
                    ],
                    wrapper_class_name='header-links',
                )
            else:
                links_object = None

            # assemble the header html
            return TurboHeader(
                wrapper_class_name='header',
                logo_object=logo_object,
                links_object=links_object,
            ).html

        # if we weren't given anything, set the header html to None
        else:
            return None
