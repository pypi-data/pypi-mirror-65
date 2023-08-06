import enum
import io
import sys
from typing import List, Sequence, cast

import typepy
from dataproperty import Align, ColumnDataProperty, DataProperty, LineBreakHandling

from ...error import EmptyHeaderError
from ...style import StylerInterface, TextStyler
from .._table_writer import AbstractTableWriter
from ._interface import IndentationInterface, TextWriterInterface


@enum.unique
class RowType(enum.Enum):
    OPENING = "opening"
    MIDDLE = "middle"
    CLOSING = "closing"


class TextTableWriter(AbstractTableWriter, TextWriterInterface):
    """
    A base class for table writer with text formats.

    .. py:attribute:: column_delimiter

        A column delimiter of a table.

    .. py:attribute:: char_left_side_row

        A character of a left side of a row.

    .. py:attribute:: char_right_side_row

        A character of a right side of a row.

    .. py:attribute:: char_cross_point

        A character of the crossing point of column delimiter and row
        delimiter.

    .. py:attribute:: char_opening_row

        A character of the first line of a table.

    .. py:attribute:: char_header_row_separator

        A character of a separator line of the header and
        the body of the table.

    .. py:attribute:: char_value_row_separator

        A character of a row separator line of the table.

    .. py:attribute:: char_closing_row

        A character of the last line of a table.

    .. py:attribute:: is_write_header_separator_row

        Write a header separator line of the table if the value is |True|.

    .. py:attribute:: is_write_value_separator_row

        Write row separator line(s) of the table if the value is |True|.

    .. py:attribute:: is_write_opening_row

        Write an opening line of the table if the value is |True|.

    .. py:attribute:: is_write_closing_row

        Write a closing line of the table if the value is |True|.

    .. py:attribute:: is_write_null_line_after_table

        Write a blank line of after writing a table if the value is |True|.

    .. figure:: ss/table_char.png
       :scale: 60%
       :alt: table_char

       Character attributes that compose a table
    """

    @property
    def margin(self) -> int:
        return self.__margin

    @margin.setter
    def margin(self, value: int) -> None:
        self.__margin = value

        self.__value_cell_margin_format = self.__make_margin_format(" ")
        self.__opening_row_cell_format = self.__make_margin_format(self.char_opening_row)
        self._header_row_separator_cell_format = self.__make_margin_format(
            self.char_header_row_separator
        )
        self.__value_row_separator_cell_format = self.__make_margin_format(
            self.char_value_row_separator
        )
        self.__closing_row_cell_format = self.__make_margin_format(self.char_closing_row)

    def __init__(self) -> None:
        super().__init__()

        self.stream = sys.stdout

        self.column_delimiter = "|"
        self.char_left_side_row = ""
        self.char_right_side_row = ""

        self.char_cross_point = ""
        self.char_left_cross_point = ""
        self.char_right_cross_point = ""
        self.char_top_left_cross_point = ""
        self.char_top_right_cross_point = ""
        self.char_bottom_left_cross_point = ""
        self.char_bottom_right_cross_point = ""

        self.char_opening_row = "-"
        self.char_opening_row_cross_point = "-"

        self.char_header_row_separator = "-"
        self.char_value_row_separator = "-"

        self.char_closing_row = "-"
        self.char_closing_row_cross_point = "-"

        self.margin = 0

        self._dp_extractor.preprocessor.line_break_handling = LineBreakHandling.REPLACE
        self.is_write_null_line_after_table = False

        self._init_cross_point_maps()

    def _init_cross_point_maps(self) -> None:
        self.__cross_point_maps = {
            RowType.OPENING: self.char_opening_row_cross_point,
            RowType.MIDDLE: self.char_cross_point,
            RowType.CLOSING: self.char_closing_row_cross_point,
        }
        self.__left_cross_point_maps = {
            RowType.OPENING: self.char_top_left_cross_point,
            RowType.MIDDLE: self.char_left_cross_point,
            RowType.CLOSING: self.char_bottom_left_cross_point,
        }
        self.__right_cross_point_maps = {
            RowType.OPENING: self.char_top_right_cross_point,
            RowType.MIDDLE: self.char_right_cross_point,
            RowType.CLOSING: self.char_bottom_right_cross_point,
        }

    def write_null_line(self) -> None:
        """
        Write a null line to the |stream|.
        """

        self._write_line()

    def write_table(self, **kwargs) -> None:
        """
        |write_table|.

        .. note::
            - |None| values are written as an empty string.
        """

        super().write_table(**kwargs)
        if self.is_write_null_line_after_table:
            self.write_null_line()

    def dump(self, output, close_after_write: bool = True) -> None:
        """Write data to the output with tabular format.

        Args:
            output (file descriptor or str):
                file descriptor or path to the output file.
            close_after_write (bool, optional):
                Close the output after write.
                Defaults to |True|.
        """

        try:
            output.write
            self.stream = output
        except AttributeError:
            self.stream = open(output, "w", encoding="utf-8")

        try:
            self.write_table()
        finally:
            if close_after_write:
                self.stream.close()
                self.stream = sys.stdout

    def dumps(self, **kwargs) -> str:
        """Get rendered tabular text from the table data.

        Only available for text format table writers.

        Returns:
            str: Rendered tabular text.
        """

        old_stream = self.stream

        try:
            self.stream = io.StringIO()
            self.write_table(**kwargs)
            tabular_text = self.stream.getvalue()
        finally:
            self.stream = old_stream

        return tabular_text

    def _create_styler(self, writer: AbstractTableWriter) -> StylerInterface:
        return TextStyler(writer)

    def _write_table_iter(self, **kwargs) -> None:
        super()._write_table_iter()
        if self.is_write_null_line_after_table:
            self.write_null_line()

    def _write_table(self, **kwargs) -> None:
        self._preprocess()
        self._write_opening_row()

        try:
            self._write_header()
            self.__write_header_row_separator()
        except EmptyHeaderError:
            pass

        is_first_value_row = True
        for values, value_dp_list in zip(self._table_value_matrix, self._table_value_dp_matrix):
            try:
                if is_first_value_row:
                    is_first_value_row = False
                else:
                    if self.is_write_value_separator_row:
                        self._write_value_row_separator()

                self._write_value_row(cast(List[str], values), value_dp_list)
            except TypeError:
                continue

        self._write_closing_row()

    def _get_opening_row_items(self) -> List[str]:
        return self.__get_row_separator_items(self.__opening_row_cell_format, self.char_opening_row)

    def _get_header_row_separator_items(self) -> List[str]:
        return self.__get_row_separator_items(
            self._header_row_separator_cell_format, self.char_header_row_separator
        )

    def _get_value_row_separator_items(self) -> List[str]:
        return self.__get_row_separator_items(
            self.__value_row_separator_cell_format, self.char_value_row_separator
        )

    def _get_closing_row_items(self) -> List[str]:
        return self.__get_row_separator_items(self.__closing_row_cell_format, self.char_closing_row)

    def __get_row_separator_items(self, margin_format: str, separator_char: str) -> List[str]:
        return [
            margin_format.format(separator_char * self._get_padding_len(col_dp))
            for col_dp in self._column_dp_list
        ]

    def _get_header_format_string(self, col_dp: ColumnDataProperty, value_dp: DataProperty) -> str:
        return "{{:{:s}{:s}}}".format(
            self._get_align_char(Align.CENTER), str(self._get_padding_len(col_dp, value_dp)),
        )

    def _to_header_item(self, col_dp: ColumnDataProperty, value_dp: DataProperty) -> str:
        return self.__value_cell_margin_format.format(super()._to_header_item(col_dp, value_dp))

    def _to_row_item(self, row_idx: int, col_dp: ColumnDataProperty, value_dp: DataProperty) -> str:
        return self.__value_cell_margin_format.format(
            super()._to_row_item(row_idx, col_dp, value_dp)
        )

    def _write_raw_string(self, unicode_text: str) -> None:
        self.stream.write(unicode_text)

    def _write_raw_line(self, unicode_text: str = "") -> None:
        self._write_raw_string(unicode_text + "\n")

    def _write(self, text):
        self._write_raw_string(text)

    def _write_line(self, text: str = "") -> None:
        self._write_raw_line(text)

    def _write_row(self, values: Sequence[str]) -> None:
        if typepy.is_empty_sequence(values):
            return

        self._write_line(
            self.char_left_side_row + self.column_delimiter.join(values) + self.char_right_side_row
        )

    def _write_header(self) -> None:
        if not self.is_write_header:
            return

        if typepy.is_empty_sequence(self._table_headers):
            raise EmptyHeaderError("header is empty")

        self._write_row(self._table_headers)

    def _write_value_row(
        self, values: Sequence[str], value_dp_list: Sequence[DataProperty]
    ) -> None:
        self._write_row(values)

    def __write_separator_row(self, values, row_type=RowType.MIDDLE):
        if typepy.is_empty_sequence(values):
            return

        cross_point = self.__cross_point_maps[row_type]
        left_cross_point = self.__left_cross_point_maps[row_type]
        right_cross_point = self.__right_cross_point_maps[row_type]

        left_cross_point = left_cross_point if left_cross_point else cross_point
        right_cross_point = right_cross_point if right_cross_point else cross_point
        if typepy.is_null_string(self.char_left_side_row):
            left_cross_point = ""
        if typepy.is_null_string(self.char_right_side_row):
            right_cross_point = ""

        self._write_line(left_cross_point + cross_point.join(values) + right_cross_point)

    def _write_opening_row(self) -> None:
        if not self.is_write_opening_row:
            return

        self.__write_separator_row(self._get_opening_row_items(), row_type=RowType.OPENING)

    def __write_header_row_separator(self):
        if any([not self.is_write_header, not self.is_write_header_separator_row]):
            return

        self.__write_separator_row(self._get_header_row_separator_items())

    def _write_value_row_separator(self) -> None:
        """
        Write row separator of the table which matched to the table type
        regardless of the value of the
        :py:attr:`.is_write_value_separator_row`.
        """

        self.__write_separator_row(self._get_value_row_separator_items())

    def _write_closing_row(self) -> None:
        if not self.is_write_closing_row:
            return

        self.__write_separator_row(self._get_closing_row_items(), row_type=RowType.CLOSING)

    def __make_margin_format(self, margin_char):
        margin_str = margin_char * self.__margin

        return margin_str + "{:s}" + margin_str


class IndentationTextTableWriter(TextTableWriter, IndentationInterface):
    """
    A base class for table writer with indentation text formats.

    .. py:attribute:: indent_string

        Indentation string for each level.
    """

    def __init__(self) -> None:
        super().__init__()

        self.set_indent_level(0)
        self.indent_string = ""

    def set_indent_level(self, indent_level: int) -> None:
        """
        Set the current indent level.

        :param int indent_level: New indent level.
        """

        self._indent_level = indent_level

    def inc_indent_level(self) -> None:
        """
        Increment the current indent level.
        """

        self._indent_level += 1

    def dec_indent_level(self) -> None:
        """
        Decrement the current indent level.
        """

        self._indent_level -= 1

    def _get_indent_string(self) -> str:
        return self.indent_string * self._indent_level

    def _write(self, text):
        self._write_raw_string(self._get_indent_string() + text)

    def _write_line(self, text: str = "") -> None:
        if typepy.is_not_null_string(text):
            self._write_raw_line(self._get_indent_string() + text)
        else:
            self._write_raw_line("")
