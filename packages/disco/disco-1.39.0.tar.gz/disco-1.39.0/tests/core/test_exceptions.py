from tests.base_test import BaseTest
from disco.core.exceptions import GraphQLRequestException


class TestExceptions(BaseTest):

    def test_graphql_request_exception(self):
        error_message = self.random_str('error-message')
        graphql_error_messages = self.random_list('GQL-error-')

        graphql_errors = [dict(message=graphql_error_message) for graphql_error_message in graphql_error_messages]

        gql_error = GraphQLRequestException(error_message, graphql_errors)

        assert gql_error.errors == graphql_errors
        assert gql_error.messages() == graphql_error_messages

        expected_output = ", ".join(graphql_error_messages)

        assert str(gql_error) == expected_output
        assert gql_error.__str__() == expected_output
        assert gql_error.__repr__() == graphql_errors
