from itertools import chain

import discord
import pytest

from embed_splitter.embed_field import EmbedField
from embed_splitter.embed_splitter import EmbedSplitter


@pytest.mark.parametrize("embed_title", ["Some embed title", None])
class TestEmbedSplitter:
    EXAMPLE_EMBED_COLOUR = 0x2F3855

    @staticmethod
    def _get_embed_length(embed: discord.Embed) -> int:
        embed_content_length = sum(
            len(item)
            for item in [
                embed.title,
                embed.description,
                embed.footer.text,
                embed.author.name,
            ]
            if item is not None
        )

        embed_fields_length = sum(
            len(item)
            for item in chain.from_iterable(
                (field.name, field.value) for field in embed.fields
            )
            if item is not None
        )

        return embed_content_length + embed_fields_length

    @classmethod
    def _get_expected_embed(
        cls, title: str | None, fields: list[EmbedField]
    ) -> discord.Embed:
        expected_embed = discord.Embed(title=title, colour=cls.EXAMPLE_EMBED_COLOUR)

        for field in fields:
            expected_embed.add_field(
                name=field.name, value=field.value, inline=field.inline
            )

        return expected_embed

    @pytest.fixture
    def example_embed(self, embed_title: str | None) -> discord.Embed:
        return discord.Embed(title=embed_title, colour=self.EXAMPLE_EMBED_COLOUR)

    def test_iter(self, example_embed: discord.Embed, embed_title: str | None) -> None:
        # Arrange
        embed_fields = [EmbedField(name="Some name", value="Some value")]

        expected_embed = self._get_expected_embed(embed_title, embed_fields)

        # Act
        embeds = list(EmbedSplitter(example_embed, embed_fields))

        # Assert
        assert len(embeds) == 1

        embed = embeds[0]
        assert embed == expected_embed
        assert self._get_embed_length(embed) <= EmbedSplitter.MAX_COMBINED_LENGTH

    def test_iter_empty_fields(
        self, example_embed: discord.Embed, embed_title: str | None
    ) -> None:
        # Arrange
        embed_fields: list[EmbedField] = []

        expected_embed = self._get_expected_embed(embed_title, embed_fields)

        # Act
        embeds = list(EmbedSplitter(example_embed, embed_fields))

        # Assert
        assert len(embeds) == 1

        embed = embeds[0]
        assert embed == expected_embed
        assert self._get_embed_length(embed) < EmbedSplitter.MAX_COMBINED_LENGTH

    def test_iter_too_many_fields(
        self, example_embed: discord.Embed, embed_title: str | None
    ) -> None:
        # Arrange
        embed_fields = [EmbedField(name=str(i), value=str(i * i)) for i in range(60)]

        expected_first_embed = self._get_expected_embed(
            f"{embed_title} (1/3)" if embed_title is not None else "(1/3)",
            embed_fields[:25],
        )

        expected_second_embed = self._get_expected_embed(
            f"{embed_title} (2/3)" if embed_title is not None else "(2/3)",
            embed_fields[25:50],
        )

        expected_third_embed = self._get_expected_embed(
            f"{embed_title} (3/3)" if embed_title is not None else "(3/3)",
            embed_fields[50:],
        )

        # Act
        embeds = list(EmbedSplitter(example_embed, embed_fields))

        # Assert
        assert embeds == [
            expected_first_embed,
            expected_second_embed,
            expected_third_embed,
        ]

        assert all(
            self._get_embed_length(embed) < EmbedSplitter.MAX_COMBINED_LENGTH
            for embed in embeds
        )

    def test_iter_fields_too_large(
        self, example_embed: discord.Embed, embed_title: str | None
    ) -> None:
        # Arrange
        embed_fields = [
            EmbedField(name=str(i) * 800, value=str(i) * 800) for i in range(10)
        ]

        expected_first_embed = self._get_expected_embed(
            f"{embed_title} (1/4)" if embed_title is not None else "(1/4)",
            embed_fields[:3],
        )

        expected_second_embed = self._get_expected_embed(
            f"{embed_title} (2/4)" if embed_title is not None else "(2/4)",
            embed_fields[3:6],
        )

        expected_third_embed = self._get_expected_embed(
            f"{embed_title} (3/4)" if embed_title is not None else "(3/4)",
            embed_fields[6:9],
        )

        expected_fourth_embed = self._get_expected_embed(
            f"{embed_title} (4/4)" if embed_title is not None else "(4/4)",
            embed_fields[9:],
        )

        # Act
        embeds = list(EmbedSplitter(example_embed, embed_fields))

        # Assert
        assert embeds == [
            expected_first_embed,
            expected_second_embed,
            expected_third_embed,
            expected_fourth_embed,
        ]

        assert all(
            self._get_embed_length(embed) < EmbedSplitter.MAX_COMBINED_LENGTH
            for embed in embeds
        )

    def test_iter_fields_in_separate_embeds(
        self, example_embed: discord.Embed, embed_title: str | None
    ) -> None:
        # Arrange
        embed_fields = [
            EmbedField(name=str(i) * 2100, value=str(2 * i) * 500) for i in range(10)
        ]

        expected_embeds = [
            self._get_expected_embed(
                (
                    f"{embed_title} ({i+1}/10)"
                    if embed_title is not None
                    else f"({i+1}/10)"
                ),
                [embed_fields[i]],
            )
            for i in range(10)
        ]

        # Act
        embeds = list(EmbedSplitter(example_embed, embed_fields))

        # Assert
        assert embeds == expected_embeds

        assert all(
            self._get_embed_length(embed) < EmbedSplitter.MAX_COMBINED_LENGTH
            for embed in embeds
        )

    @pytest.mark.parametrize("index", range(11))
    def test_iter_single_field_too_large(
        self, example_embed: discord.Embed, index: int
    ) -> None:
        # Arrange
        embed_fields = [
            EmbedField(name=str(i) * 800, value=str(i * i) * 800) for i in range(10)
        ]
        embed_fields.insert(index, EmbedField(name="0" * 6000, value="0" * 6000))

        expected_error_message = (
            f"Unable to split fields: Single embed field at index {index} too large"
        )

        # Act
        with pytest.raises(ValueError, match=expected_error_message):
            next(iter(EmbedSplitter(example_embed, embed_fields)))

    def test_iter_with_header(
        self, example_embed: discord.Embed, embed_title: str | None
    ) -> None:
        # Arrange
        embed_fields = [
            (
                EmbedField(name=str(i) * 3000, value=str(i) * 1000)
                if i % 2 == 1
                else EmbedField(
                    name=f"### Header {i}", value=f"This is a header for row {i + 1}"
                )
            )
            for i in range(10)
        ]

        expected_embeds = [
            self._get_expected_embed(
                (
                    f"{embed_title} ({i+1}/5)"
                    if embed_title is not None
                    else f"({i+1}/5)"
                ),
                [embed_fields[2 * i], embed_fields[2 * i + 1]],
            )
            for i in range(5)
        ]

        # Act
        embeds = list(EmbedSplitter(example_embed, embed_fields, "###"))

        # Assert
        assert embeds == expected_embeds

        assert all(
            self._get_embed_length(embed) < EmbedSplitter.MAX_COMBINED_LENGTH
            for embed in embeds
        )
