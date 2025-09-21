from functools import cached_property
from typing import Iterator

import discord

from embed_splitter.embed_field import EmbedField


class EmbedSplitter:
    MAX_COMBINED_LENGTH = 5000

    def __init__(
        self,
        embed: discord.Embed,
        fields: list[EmbedField],
        header_prefix: str | None = None,
    ):
        self._embed = embed
        self._fields = fields
        self._header_prefix = header_prefix

        for i, field in enumerate(self._fields):
            if self._embed_elements_length + len(field) < self.MAX_COMBINED_LENGTH:
                continue

            raise ValueError(
                f"Unable to split fields: Single embed field at index {i} too large"
            )

    @cached_property
    def _embed_elements_length(self) -> int:
        return sum(
            len(item)
            for item in [
                self._embed.title,
                self._embed.description,
                self._embed.footer.text,
                self._embed.author.name,
            ]
            if item is not None
        )

    def _should_split_embed(
        self, fields: list[EmbedField], new_field: EmbedField
    ) -> bool:
        if len(fields) >= 25:
            return True

        fields_length = sum(map(len, fields))

        return (
            self._embed_elements_length + fields_length + len(new_field)
            >= self.MAX_COMBINED_LENGTH
        )

    def _split_embed_fields(
        self,
        field_groups: list[list[EmbedField]],
        is_field_connected_to_previous_field: bool,
    ) -> None:
        if is_field_connected_to_previous_field:
            field_groups.append([field_groups[-1].pop()])
        else:
            field_groups.append([])

    def _get_embed_title(self, index: int, total_count: int) -> str | None:
        if total_count <= 1:
            return self._embed.title

        if self._embed.title is None:
            return f"({index}/{total_count})"

        return f"{self._embed.title} ({index}/{total_count})"

    def _get_embed_from_fields(
        self, fields: list[EmbedField], index: int, total_count: int
    ) -> discord.Embed:
        embed = discord.Embed(
            title=self._get_embed_title(index, total_count), colour=self._embed.colour
        )

        for field in fields:
            embed.add_field(name=field.name, value=field.value, inline=field.inline)

        return embed

    def __iter__(self) -> Iterator[discord.Embed]:
        field_groups: list[list[EmbedField]] = [[]]
        is_field_connected_to_previous_field = False

        for field in self._fields:
            if self._should_split_embed(field_groups[-1], field):
                self._split_embed_fields(
                    field_groups, is_field_connected_to_previous_field
                )

            is_field_connected_to_previous_field = (
                field.name.startswith(self._header_prefix)
                if self._header_prefix
                else False
            )

            field_groups[-1].append(field)

        for i, fields in enumerate(field_groups):
            yield self._get_embed_from_fields(fields, i + 1, len(field_groups))
