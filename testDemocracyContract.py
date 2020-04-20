from unittest import TestCase
from os.path import dirname, join
from pytezos import ContractInterface, MichelsonRuntimeError

admin = "tz1TGu6TN5GSez2ndXXeDX6LgUDvLzPLqgYV"
non_admin = "tz1iWiN1hqFHEJEGW4gunUW6o2t1SC8sJoKT"
wallet1 = "tz1ddb9NMYHZi5UzPdzTZMYQQZoMub195zgv"
wallet2 = "tz1b7tUupMgCNw2cCLpKTkSD1NZzB5TkP2sv"
wallet3 = "tz1faswCTDciRzE4oJ9jn2Vm2dvjeyA9fUzU"
wallet4 = "tz1gjaF81ZRRvdzjobyfVNsAeSC6PScjfQwN"
wallet5 = "tz1KqTpEZ7Yob7QbPE4Hy4Wo8fHG8LhKxZSx"
wallet6 = "tz1VtUMXUwuAfN4euuGg6YC23QT5WDk94M74"
wallet7 = "tz1PJSVnbr8ztVSrT2NuBEmGubnYKcxk3zie"
wallet8 = "tz1LuiwRnA63anqr6ot86xJR3VK86qJxURDj"
wallet9 = "tz1fPexY96eBrdzXySYzyqq6vM2ZpN5e4q2g"

class pyTestContract(TestCase):

    @classmethod
    def setUpClass(cls):
        project_dir = dirname(dirname(__file__))
        cls.votingContract = ContractInterface.create_from(join(project_dir, 'democracyContract.tz'))

#Vérifie le vote
    def test_vote(self):
        result = self.votingContract.vote(True).result(
            storage = {
            "votes": { },
            "paused": False,
            "admin": admin
            },
            source = non_admin
        )
        self.assertEqual(True, result.storage['votes'][non_admin])

#Vérifie le vote de l'administrateur
    def test_admin_vote(self):
        with self.assertRaises(MichelsonRuntimeError):
            self.votingContract.vote(False).result(
                storage = {
                "votes": { non_admin: True },
                "paused": False,
                "admin": admin
                },
                source = admin
            )

#Vérifie le double vote
    def test_vote_twice(self):
        with self.assertRaises(MichelsonRuntimeError):
            self.votingContract.vote(True).result(
                storage = {
                "votes": { non_admin: True },
                "paused": False,
                "admin": admin
                },
                source = non_admin
            )
#Vérifie la pause
    def test_vote_paused(self):
        with self.assertRaises(MichelsonRuntimeError):
            self.votingContract.vote(True).result(
                storage = {
                "votes": { wallet1: True },
                "paused": True,
                "admin": admin
                },
                source = non_admin
            )
#Vérifie la pause du contrat après 10 votes
    def test_vote_pausing(self):
        result = self.votingContract.vote(True).result(
            storage = {
            "votes": { wallet1: True, wallet2: False, wallet3: False, wallet4: False, wallet5: False, wallet6: False, wallet7: False, wallet8: False , wallet9: False },
            "paused": False,
            "admin": admin
            },
            source = non_admin
        )
        self.assertEqual(10, result.storage["voteCount"])
        self.assertEqual(True, result.storage['paused'])

#Vérifications de la remise à zéro
    def test_reset(self):
        result = self.votingContract.reset(
            0
        ).result(
            storage = {
            "votes": { wallet1 : True },
            "paused": True,
            "admin": admin
            },
            source = non_admin
        )
        self.assertEqual({}, result.storage["votes"])
        self.assertEqual(False, result.storage["paused"])


    def test_reset_not_admin(self):
        with self.assertRaises(MichelsonRuntimeError):
            self.votingContract.reset(
                0
            ).result(
                storage = {
                "votes": { wallet1: True },
                "paused": True,
                "admin": admin
                },
                source = non_admin
            )
