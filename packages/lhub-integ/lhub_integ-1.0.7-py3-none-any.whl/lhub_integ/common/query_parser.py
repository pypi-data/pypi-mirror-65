from lhub_integ.common import input_helpers

TYPE_LITERAL = 'LIT'
TYPE_VARIABLE = 'VAR'
DELIMITER_OPEN = '{{'
DELIMITER_CLOSE = '}}'

# Validates and Parses a Query Template string
# Ex:   'select {{col}} from {{tbl}} where {{cond}}'
#
# Returns a pair of (validation_message, parsed_query_template_list)
# Only one part of the pair will exist, the other will be None
#
# Example:
#
# (None,                       # validation message
#  [('LIT', 'select '),    # note whitespace
#   ('VAR', 'col'),
#   ('LIT', ' from '),
#   ('VAR', 'tbl'),
#   ('LIT', ' where '),
#   ('VAR', 'cond')])


def validate_and_parse(query_template_str):
    output = []
    parts = query_template_str.split(DELIMITER_OPEN)
    if len(parts) != len(query_template_str.split(DELIMITER_CLOSE)):
        return "Mismatch in number of open and close double-braces", None

    for part in parts:
        if DELIMITER_CLOSE in part:
            # must contain a variable then a literal
            subparts = part.split(DELIMITER_CLOSE)

            if len(subparts) != 2:
                return "Incorrect variable substitution near '{}' of '{}'".format(part, query_template_str), None

            variable_name = input_helpers.safe_strip(subparts[0])
            literal = subparts[1] # trailing whitespace is expected here

            if ' ' in variable_name:
                return "Variable cannot contain a space: '{}'".format(variable_name), None

            output.append(
                (TYPE_VARIABLE, variable_name)
            )

            if literal:
                output.append(
                    (TYPE_LITERAL, literal)
                )
        else:
            # must be a literal
            literal = part
            if literal:
                output.append(
                    (TYPE_LITERAL, literal)
                )
    return None, output


# Takes a parsed query template and a dict of variable names and values
# Fills in values of variables in the template and returns the query string
def generate_query(parsed_query_template_list, variable_name_value_dict):
    query_str = ''
    for element_type, element_value in parsed_query_template_list:
        if element_type == TYPE_LITERAL:
            query_str += element_value
        elif element_type == TYPE_VARIABLE:
            # Assumes column exists # TODO reconsider
            variable_name = element_value
            if variable_name in variable_name_value_dict:
                query_str += str(variable_name_value_dict.get(variable_name))
            else:
                raise ValueError("The following variable is missing from the input table: {}".format(variable_name))
        else:
            raise ValueError("Unknown query element type: {}".format(element_type))
    return query_str
