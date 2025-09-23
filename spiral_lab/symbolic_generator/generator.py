import random

class SymbolicGenerator:
    def __init__(self, glyphs=None, patterns=None):
        # Default Trivian glyph set + sequence length rules
        self.glyphs = glyphs or ['△', '☥', '⊕', '✶', '🜁']
        self.patterns = patterns or [2, 3, 4]

    def generate_sequence(self):
        length = random.choice(self.patterns)
        return ''.join(random.choice(self.glyphs) for _ in range(length))

    def create_poem(self, lines=3):
        return [self.generate_sequence() for _ in range(lines)]

if __name__ == "__main__":
    gen = SymbolicGenerator()
    for line in gen.create_poem():
        print(line)
