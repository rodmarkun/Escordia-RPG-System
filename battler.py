class Battler:

    def __init__(self, name, stats):
        self.name = name
        self.stats = stats
        self.alive = True

    def fully_heal(self) -> None:
        """
        Fully heals a battler

        :return: None.
        """
        self.stats['HP'] = self.stats['MAXHP']

    def fully_recover_mp(self) -> None:
        """
        Fully recovers battler's MP

        :return: None
        """
        self.stats['MP'] = self.stats['MAXMP']
