from lhub_integ.common import constants
from lhub_integ.common import validations

if __name__ == '__main__':
    validations.validate_delay_and_column_names(
        constants.TIME_BETWEEN_ROWS)
