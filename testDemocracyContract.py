from unittest import TestCase
from os.path import dirname, join
from pytezos import ContractInterface, MichelsonRuntimeError

admin       = "tz1TGu6TN5GSez2ndXXeDX6LgUDvLzPLqgYV"
non_admin   = "tz1iWiN1hqFHEJEGW4gunUW6o2t1SC8sJoKT"
wallet1 = "tz1ddb9NMYHZi5UzPdzTZMYQQZoMub195zgv"


class pyTestContract(TestCase):

    @classmethod
    def setUpClass(cls):
        project_dir = dirname(dirname(__file__))
        cls.votingContract = ContractInterface.create_from(join(project_dir, 'democracyContract.tz'))



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


#Vérifie le vote
    def test_vote(self):
        result = self.votingContract.vote(True).result(
            storage = {
            "votes": { non_admin: True },
            #"paused": False,
            "paused": True,
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
