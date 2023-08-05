import dash
import dash_core_components as dcc
import dash_html_components as html


class TurboInput:
    def __init__(
            self,
            output_id_list,
            input_type,
            df,
            value_column,
            label_column=None,
            turbo_filter_object=None,
            input_class_name=None,
            input_label=None,
            input_label_class_name=None,
    ):
        """input object that will assemble the information we need

        :param output_id_list: ID(s) for which outputs this input will affect
        :param input_type: string for the type of input we want to use,
            you might have to add functionality for your input if you're using a new one
        :param df: dataframe we'll use to gather the filter info
        :param value_column: column in the dataframe that contains the values
        :param label_column: optional, column in the dataframe that contains the labels, defaults to the value_column
        :param turbo_filter_object: optional, TurboFilter object that contains info about
            what input strings the filter will output and how to filter the dataframe based on those inputs
        :param input_class_name: optional, css class name for the input object
        :param input_label: optional, text label for the input object
        :param input_label_class_name: optional, css class name for the label of the input object
        """
        self.output_id_list = output_id_list
        self.input_type = input_type
        self.df = df
        self.value_column = value_column
        if label_column is None:
            self.label_column = value_column
        else:
            self.label_column = label_column
        self.turbo_filter_object = turbo_filter_object
        self.input_class_name = input_class_name
        if input_label is None:
            self.input_label = self.label_column
        else:
            self.input_label = input_label
        self.input_label_class_name = input_label_class_name

        self.input_component_id = self.turbo_filter_object.input_component_id
        self.lambda_function_list = self.turbo_filter_object.lambda_function_list
        self.dash_dependencies_input_list = self.turbo_filter_object.dash_dependencies_input_list

        self.html = self.assemble_input_html()

    def assemble_input_html(self):
        """assemble the input html we want and update a few variables relating to the input"""

        if self.input_type == 'Dropdown':
            filter_options = [
                # groupby objects are cool, they create a list of dfs and the grouped values
                # since we're grouping by both label and value, we get a tuple returned with the df
                {'label': i[0], 'value': i[1]} for i, i_df in self.df.groupby([self.label_column, self.value_column])
            ]

            return html.Div(
                children=[
                    html.Div(
                        className=self.input_label_class_name,
                        children=self.input_label,
                    ),
                    dcc.Dropdown(
                        id=self.input_component_id,
                        className=self.input_class_name,
                        options=filter_options,
                    ),
                ]
            )

        if self.input_type == 'RangeSlider':
            values = self.df[self.value_column].unique()
            minimum = min(values)
            maximum = max(values)
            marks = {int(val): {'label': str(val), 'style': {'transform': 'rotate(45deg)'}} for val in values}

            return html.Div(
                children=[
                    html.Div(
                        className=self.input_label_class_name,
                        children=self.input_label,
                    ),
                    dcc.RangeSlider(
                        id=self.input_component_id,
                        className=self.input_class_name,
                        min=minimum,
                        max=maximum,
                        value=[minimum, maximum],
                        marks=marks,
                        step=None,
                    ),
                ]
            )

        # who are you? who who, who who
        else:
            raise ValueError(
                """I don't know what to do with a "{}" input type. Please add it to {}."""
                .format(self.input_type, __file__)
            )


class TurboFilter:
    def __init__(
            self,
            input_component_id,
            filter_input_property_list,
            lambda_function_list,
    ):
        """object that helps us organize the input values we collect and how we'll update the data using them
        Is this necessary to have a separate object? No
        But it does help us organize everything because this is an important aspect of dash

        :param input_component_id: ID for the input, dash will use this in the callbacks
        :param filter_input_property_list: list of input strings that tell us what values to look for from each filter,
            e.g. ['value'] for Dropdown and RadioItems, ['start_date', 'end_date'] for DatePickerRange
        :param lambda_function_list: list of lambda functions we want to apply to each of the inputs, respectively
            these functions must take two arguments: a dataframe and the value to filter on
        """
        self.input_component_id = input_component_id
        self.filter_input_property_list = filter_input_property_list
        self.lambda_function_list = lambda_function_list

        self.dash_dependencies_input_list = [  # comprehend the list of dash.dependencies.Input
            dash.dependencies.Input(component_id=self.input_component_id, component_property=input_property)
            for input_property in self.filter_input_property_list
        ]
