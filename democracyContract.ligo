// --------- Action ----------- //

//Définition des actions du smart contract. Voter + remise à zéro
type action is
| Vote of bool
| Reset of int

// --------- Storage ----------- //

//Définition du storage
type storageType is record [
  admin: address;
  paused: bool;
  votes: map(address, bool);
]

// --------- Admin ----------- //

//Vérifie que l'adresse appartient bien à l'administrateur
function isAdmin (const storage : storageType) : bool is
  block { skip } with (sender = storage.admin)

// --------- Pause ----------- //

//Vérifie que le contrat est en pause
function isPaused (const storage : storageType) : bool is
  block { skip } with (storage.paused)

// --------- Vote ----------- //

//Le choix du vote se fait avec un un booléen (True = Yes, False = No)
function addVote (const vote : bool; const storage : storageType) : (list(operation) * storageType) is
  block {
      var numberVotes : int := 0;
      if (isPaused(storage)) then block {
        if ( isAdmin(storage) )
          then block {
           case storage.votes[sender] of
             | Some (bool) -> failwith("Un utilisateur doit pouvoir ne voter qu'une seule fois !")
             | None -> block {
               storage.votes[sender] := vote;
               //ajout du vote
               for i in map storage.votes block {
                 numberVotes := numberVotes + 1;
               };
               //Met le contrat en pause au bout de 10 votes
               if (numberVotes = 10) then block {
                 storage.paused := True;
               }
              else block {
                  skip
                }
            }
          end
        }
      else block {
        failwith("L'administrateur n'a pas le droit de voter !");
       }
     }
     else block {
       failwith("Le smart contract est mis en pause !");
    }
  } with ((nil: list(operation)) , storage)

// --------- Reset ----------- //

function resetContract (const storage : storageType) : (list(operation) * storageType) is
  block {
    if ( isAdmin(storage) )
      then block {
        if ( isPaused(storage) )
          then block {
            //Remise à zéro du contrat
            for i in map storage.votes block {
              remove i from map storage.votes;
            };
            storage.paused := False;
          }
          else block {
            failwith("Le contrat est actuellement en pause !");
          }
      }
      else block {
        failwith("Seul l'administrateur peut executer cette fonction !");
      }
  } with ((nil: list(operation)) , storage)

// --------- Main ----------- //

function main (const p : action ; const s : storageType) :
  (list(operation) * storageType) is
  block { skip } with
  case p of
    | Vote(n) -> addVote(n, s)
    | Reset(n) -> resetContract(s)
  end
