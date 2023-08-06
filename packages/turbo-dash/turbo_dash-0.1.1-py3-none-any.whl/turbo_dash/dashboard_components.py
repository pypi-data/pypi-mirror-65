import dash_core_components as dcc
import dash_html_components as html


class TurboHeader:

    def __init__(
            self,
            wrapper_class_name=None,
            logo_object=None,
            links_object=None,
    ):
        """quickly create a header for your dashboard with minimal inputs

        :param wrapper_class_name: optional, css class name for the header wrapper
        :param logo_object: optional, TurboLogo object
        :param links_object: optional, TurboLinks object
        """
        self.wrapper_class_name = wrapper_class_name
        self.logo_object = logo_object
        self.links_object = links_object

        self.html = html.Div(
            className=self.wrapper_class_name,
            children=[
                self.logo_object.html,
                self.links_object.html,
            ],
        )


class TurboLogo:

    def __init__(
            self,
            logo_component_id=None,
            logo_class_name=None,
            logo_file_path=None,
            logo_href=None,
            logo_width=None
    ):
        """logo object that will display the logo in the header of your dashboard

        :param logo_component_id: optional, ID for the logo A
        :param logo_class_name: optional, css class name for the logo A
        :param logo_file_path: optional, file path or url to the logo object,
            recommended that you put this in a top level directory named 'static/'
        :param logo_href: optional, href link for your logo if clicked on
        :param logo_width: optional, width of the logo Img
        """
        self.logo_component_id = logo_component_id
        self.logo_class_name = logo_class_name
        self.logo_file_path = logo_file_path
        self.logo_href = logo_href
        self.logo_width = logo_width

        self.html = html.A(
            id=self.logo_component_id,
            className=self.logo_class_name,
            href=self.logo_href,
            children=html.Img(
                src=self.logo_file_path,
                width=self.logo_width,
            )
        )


class TurboLinks:

    def __init__(
            self,
            list_of_link_objects,
            wrapper_class_name=None,
    ):
        """object that will create the links in the header of your dashboard

        :param list_of_link_objects: list of TurboLink objects
        :param wrapper_class_name: optional, css class name for the links wrapper
        """
        self.list_of_link_objects = list_of_link_objects
        self.wrapper_class_name = wrapper_class_name

        self.html = html.Div(
            className=self.wrapper_class_name,
            children=[link.html for link in self.list_of_link_objects]
        )


class TurboLink:

    def __init__(
            self,
            link_component_id=None,
            link_href=None,
            link_class_name=None,
            link_text=None,
    ):
        """object hat will create each link in the header of your dashboard

        :param link_component_id: optional, id for the dcc.Link object
        :param link_href: optional, href to use
        :param link_class_name: optional, css class name for the link
        :param link_text: optional, text to display in the link
        """
        self.link_component_id = link_component_id
        self.link_href = link_href
        self.link_class_name = link_class_name
        self.link_text = link_text

        self.html = dcc.Link(
            id=self.link_component_id,
            href=self.link_href,
            children=[
                html.Div(
                    className=self.link_class_name,
                    children=self.link_text,
                ),
            ]
        )
