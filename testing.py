import pytest

from conftest import W_ROWS, read_csv_rows, get_row_count, ACTUAL_COLUMNS

w_rows = W_ROWS
first_w_row = w_rows[0][1:]
w_rows = w_rows[1:]


def is_numeric(string: str) -> bool:
    try:
        float(string)
        return True
    except ValueError:
        return False


def compare_assert(row: list, w_row: list, first_w_row: list):
    result_list = []
    for c in ACTUAL_COLUMNS:
        if c in (0, 1, 2, 3, 4, 5, 25, 52, 53, 54, 55, 56, 57):
            if row[c] != w_row[c]:
                result_list.append((first_w_row[c], row[c], w_row[c]))
        elif c in (6, 7, 8, 9, 10, 11, 14, 15, 18, 19, 20, 21, 31, 32, 33, 40, 41):
            if not row[c]:
                result_list.append((first_w_row[c], row[c], "Shouldn't be empty or 0"))
        elif c in (22, 23, 24):
            if row[c] not in ['', 'index, follow']:
                result_list.append((first_w_row[c], row[c], "should be empty or `index, follow`"))
        elif c in (36, 37, 38, 39, 42, 43, 44, 45):
            if not is_numeric(row[c]):
                result_list.append((first_w_row[c], row[c], "should be any number"))
    return result_list


def compare_rows(wrow):
    csv_rows = read_csv_rows()
    for i in range(get_row_count()):
        w_row = wrow[1:]
        for row in csv_rows:
            if w_row[0] in row:
                # actual_row = []
                # actual_w_row = []
                # actual_row_title = []
                # for c in ACTUAL_COLUMNS:
                #     actual_row.append(row[c])
                #     actual_w_row.append(w_row[c])
                #     actual_row_title.append(first_w_row[c])
                #diffs_list = [(a, b, c) for a, b, c in zip(actual_row_title, actual_row, actual_w_row) if b != c]
                diffs_list = compare_assert(row, w_row, first_w_row)
                if len(diffs_list) > 0:
                    for diff in diffs_list:
                        print(f"Column name: {diff[0]}")
                        print(f"Actual value: {diff[1]}")
                        print(f"Expected value: {diff[2]}")
                        print("")
                assert len(diffs_list) < 1, f"Assertions failed"
                #assert actual_row == actual_w_row


@pytest.mark.parametrize('wrow', w_rows)
def test(wrow):
    compare_rows(wrow)
