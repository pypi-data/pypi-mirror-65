import dash_core_components as dcc
import dash_html_components as html

from config import LOGO_PATH


class turbo_dash:

    def __init__(
            self,
            app_to_callback,
            list_of_inputs,
            list_of_outputs,
            layout_template=None,
    ):
        """quickly create a dashboard by providing a list of inputs and outputs

        :param app_to_callback: dash app we want to make reactive (i.e. call back)
        :param list_of_inputs: list of TurboInput objects to use in our dashboard
        :param list_of_outputs: list of TurboOutput objects to use in our dashboard
        :param layout_template: optional, template to use for the layout
        """
        self.app_to_callback = app_to_callback
        self.list_of_inputs = list_of_inputs
        self.list_of_outputs = list_of_outputs
        self.layout_template = layout_template

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
                id='main_div',
                children=[
                    html.Div(
                        id='input_div',
                        children=[i.html for i in self.list_of_inputs]
                    ),
                    html.Div(
                        id='output_div',
                        children=[o.html for o in self.list_of_outputs]
                    ),
                ],
            )
        elif self.layout_template == 'turbo':
            return html.Div(
                id='main_div',
                children=[
                    html.Div(  # header
                        id='header_div',
                        className='header',
                        children=[
                            html.A(  # logo
                                href='#',
                                children=html.Img(
                                    src=LOGO_PATH,
                                    width='100px',
                                )
                            ),  # /logo
                            html.Div(  # links
                                className='header-links',
                                children=[
                                    dcc.Link(  # link0
                                        id='link0',
                                        href='#',
                                        children=[
                                            html.Div(className='header-link', children='Link to Something')
                                        ]
                                    ),  # /link0
                                    dcc.Link(  # link1
                                        id='link1',
                                        href='#',
                                        children=[
                                            html.Div(className='header-link', children='Link to Something Else')
                                        ]
                                    ),  # /link1
                                ],
                            ),  # /links
                        ],
                    ),  # /header
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
        # who are you? who who, who who
        else:
            raise ValueError(
                """I don't know what to do with a "{}" output type. Please add it to {}."""
                .format(self.layout_template, __file__)
            )
