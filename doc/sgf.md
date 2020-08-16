# Smart Game Format

## 1. SGF Basics
SGF is a text only format. It contains game tree, with all their nodes and properties, and nothing more. Example:
```
(;FF[4]C[root](;C[a];C[b](;C[c])
(;C[d];C[e]))
(;C[f](;C[g];C[h];C[i])
(;C[j])))
```

## 2. Basic (EBNF) Definition
```
Collection = GameTree { GameTree }
GameTree   = "(" Sequence { GameTree } ")"
Sequence   = Node { Node }
Node       = ";" { Property }
Property   = PropIdent PropValue { PropValue }
PropIdent  = UcLetter { UcLetter }
PropValue  = "[" CValueType "]"
CValueType = (ValueType | Compose)
ValueType  = (None | Number | Real | Double | Color | SimpleText |
		Text | Point  | Move | Stone)
```

SGF files are comprised of pairs of properties and property values, each of which describes a feature of the game. A partial list appears below. Full information can be found using the references in the Links section below.
* **FF**: File format: version of SGF specification governing this SGF file.
* **GM**: Game: type of game represented by this SGF file. A property value of 1 refers to Go.
* **SZ**: Size: size of the board, non square boards are supported.
* **HA**: Handicap: the number of handicap stones given to Black. Placement of the handicap stones are set using the AB property.
* **KM**: Komi: Komi is a Japanese go term adopted into English. In a game of Go, Black has the advantage of first move. In order to compensate for this, White can be given an agreed, set number of points before starting the game. These points are called komi.
* **RU**: Rules: ruleset (e.g.: Japanese).
* **RE**: Result: result, usually in the format "B+R" (Black wins by resign) or "B+3.5" (black wins by 3.5 moku).
* **B**:  a move by Black at the location specified by the property value.
* **W**: a move by White at the location specified by the property value.

## Reference
* https://senseis.xmp.net/?SmartGameFormat
* https://www.red-bean.com/sgf/
