import plotly.express as px
import dash
import dash_core_components as dcc


class TurboOutput:
    def __init__(
            self,
            output_component_id,
            output_component_property,
            output_type,
            df=None,
            x=None,
            y=None,
            color=None,
            template=None,
            turbo_input_list=None,
    ):
        """output object that will assemble the information we need

        :param output_component_id: component ID for the output, dash will use this in the callbacks
        :param output_component_property: property we want to update for the output, dash will use this in the callbacks
        :param output_type: string for the type of output we want to use,
            you might have to add functionality for your output if you're using a new one
        :param df: optional, dataframe we'll use to gather the output data
        :param x: optional, column we'll use for the x axis data
        :param y: optional, column we'll use for the y axis data
        :param color: optional, plotly express color argument (column to color accordingly)
        :param template: optional, plotly express template for the output
        :param turbo_input_list: optional, list of TurboInput objects that will affect this output
        """
        self.output_component_id = output_component_id
        self.output_component_property = output_component_property
        self.output_type = output_type
        self.df = df
        self.x = x
        self.y = y
        self.color = color
        self.template = template
        self.turbo_input_list = turbo_input_list

        # this is important! This is the dash output that the callback will update
        self.dash_dependencies_output = dash.dependencies.Output(
            component_id=self.output_component_id,
            component_property=self.output_component_property,
        )

        # this is also important! This is the list of dash inputs the callback will listen for
        # We need to flatten all the dash dependencies input lists for this output and grab the dependencies
        # this is using list comprehension, the expanded equivalent would be:
        # lst = []
        # for turbo_input in self.turbo_input_list:
        #     for item in turbo_input.dash_dependencies_input_list:
        #         lst.append(item)
        self.dash_dependencies_input_list = [
            inp for turbo_input in self.turbo_input_list for inp in turbo_input.dash_dependencies_input_list
        ]

        # yet again, this is important! This is the list of lambda functions we're going to filter the dataframe on
        self.lambda_function_list = [
            func for turbo_input in self.turbo_input_list for func in turbo_input.lambda_function_list
        ]

        self.html = dcc.Graph(id=self.output_component_id)  # set the html we'll use for the layout

    def assemble_output_object(self, filtered_df):
        """assemble the output object we want"""

        if self.output_type == 'bar':
            return px.bar(
                data_frame=filtered_df,
                x=self.x,
                y=self.y,
                color=self.color,
                template=self.template,
            )

        elif self.output_type == 'scatter':
            return px.scatter(
                data_frame=filtered_df,
                x=self.x,
                y=self.y,
                color=self.color,
                template=self.template,
            )

        elif self.output_type == 'line':
            return px.line(
                data_frame=filtered_df,
                x=self.x,
                y=self.y,
                color=self.color,
                template=self.template,
            )

        # who are you? who who, who who
        else:
            raise ValueError(
                """I don't know what to do with a "{}" output type. Please add it to {}."""
                .format(self.output_type, __file__)
            )

    def filter_dataframe(self, args):
        """filter the dataframe based on the input values, columns, and operators provided"""
        filtered_df = self.df

        for index, input_filter_value in enumerate(args):  # args is a list of all the filter input values

            # if the value provided is None, we'll return the original df, otherwise we'll do the filtering
            if input_filter_value is not None:
                filtered_df = self.lambda_function_list[index](filtered_df, input_filter_value)

        return filtered_df

    def callback(self, app_to_callback):
        @app_to_callback.callback(
            output=self.dash_dependencies_output,
            inputs=self.dash_dependencies_input_list,
        )
        def filter_and_assemble_output(*input_values):
            """put everything together into one function where we filter and assemble the output"""
            filtered_df = self.filter_dataframe(input_values)
            return self.assemble_output_object(filtered_df=filtered_df)
