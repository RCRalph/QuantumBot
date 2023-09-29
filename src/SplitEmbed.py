import discord

class SplitEmbed:
    MAX_COMBINED_LENGTH = 5000
    data: discord.Embed

    def __init__(self, data: discord.Embed):
        self.data = data

    def embed_length(self, embed: discord.Embed):
        result = 0

        for item in [
            embed.title,
            embed.description,
            embed.footer.text,
            embed.author.name,
        ]:
            if item is not None:
                result += len(item)

        for field in embed.fields:
            for item in [field.name, field.value]:
                if item is not None:
                    result += len(item)

        return result

    def should_split_embed(self, embed: discord.Embed):
        return self.embed_length(embed) >= self.MAX_COMBINED_LENGTH or len(embed.fields) >= 25

    def get_empty_embed(self):
        return discord.Embed(
            title=self.data.title,
            color=self.data.color
        )

    def append_embed_field(self, embed_field, target: discord.Embed):
        target.add_field(
            name=embed_field.name,
            value=embed_field.value,
            inline=embed_field.inline
        )

    def get_embeds(self):
        result: list[discord.Embed] = []

        glue_last_two = False
        for item in self.data.fields:
            if not len(result) or self.should_split_embed(result[-1]):
                result.append(self.get_empty_embed())

                if glue_last_two:
                    self.append_embed_field(result[-2].fields[-1], result[-1])
                    result[-2].remove_field(-1)
                    glue_last_two = False

            glue_last_two = item.name.startswith("━")

            self.append_embed_field(item, result[-1])

        if len(result) > 1:
            for i in range(len(result)):
                result[i].title += f" ({i + 1}/{len(result)})"

        return result
