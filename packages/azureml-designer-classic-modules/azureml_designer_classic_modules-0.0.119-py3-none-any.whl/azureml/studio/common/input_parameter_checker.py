from .datatable.data_table import DataTable
from .error import ErrorMapping, InvalidColumnTypeError
from azureml.studio.modulehost.constants import ElementTypeName


class InputParameterChecker:

    @staticmethod
    def verify_data_table(data_table: DataTable, friendly_name):
        """
        Verify that input dataset is not null or empty
        :param data_table: The data_table specified as input to a module
        :param friendly_name: The friendly name of the table as it appears in the UI
        :return:
        """
        ErrorMapping.verify_not_null_or_empty(data_table, friendly_name)
        ErrorMapping.verify_number_of_rows_greater_than_or_equal_to(curr_row_count=data_table.number_of_rows,
                                                                    required_row_count=1,
                                                                    arg_name=friendly_name)
        ErrorMapping.verify_number_of_columns_greater_than_or_equal_to(curr_column_count=data_table.number_of_columns,
                                                                       required_column_count=1,
                                                                       arg_name=friendly_name)

    @staticmethod
    def parameter_range_check(parameter, lower_bound, upper_bound, lower_inclusive, upper_inclusive, friendly_name):
        ErrorMapping.verify_value_in_range(value=parameter, lower_bound=lower_bound, upper_bound=upper_bound,
                                           lower_inclusive=lower_inclusive, upper_inclusive=upper_inclusive,
                                           arg_name=friendly_name)

    @staticmethod
    def verify_all_columns_are_string_type(data_table, friendly_name):
        """Check if datatype of dataset is string
        :param data_table: input data set
        :return: None
        Raise error if the selected data table contains invalid data type.
        """
        column_names = data_table.data_frame.columns
        illegal_column_names = [n for n in column_names if
                                data_table.get_element_type(n) != ElementTypeName.STRING]
        if illegal_column_names:
            illegal_column_types = [data_table.get_element_type(n) for n in illegal_column_names]
            ErrorMapping.throw(InvalidColumnTypeError(
                col_name=','.join(illegal_column_names),
                col_type=','.join(illegal_column_types),
                arg_name=friendly_name)
            )
