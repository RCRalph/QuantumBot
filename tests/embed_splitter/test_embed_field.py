from embed_splitter.embed_field import EmbedField


class TestEmbedField:
    EXAMPLE_FIELD_NAME = "Example field name"
    EXAMPLE_FIELD_VALUE = "Example field value"

    def test_len(self) -> None:
        # Arrange
        embed_field = EmbedField(
            name=self.EXAMPLE_FIELD_NAME, value=self.EXAMPLE_FIELD_VALUE
        )

        # Act
        field_len = len(embed_field)

        # Assert
        assert field_len == len(self.EXAMPLE_FIELD_NAME) + len(self.EXAMPLE_FIELD_VALUE)
