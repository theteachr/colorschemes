module Ring exposing (..)


type alias Ring a =
    { prev : List a
    , curr : a
    , next : List a
    }


forward : Ring a -> Ring a
forward ({ prev, curr, next } as ring) =
    case ( prev, next ) of
        ( ps, x :: xs ) ->
            { prev = curr :: ps, curr = x, next = xs }

        ( ps, [] ) ->
            let
                reversedPrev =
                    List.reverse (curr :: ps)
            in
            case reversedPrev of
                newCurr :: rest ->
                    { prev = [], curr = newCurr, next = rest }

                [] ->
                    ring


backward : Ring a -> Ring a
backward ({ prev, curr, next } as ring) =
    case ( prev, next ) of
        ( p :: ps, xs ) ->
            { prev = ps, curr = p, next = curr :: xs }

        ( [], xs ) ->
            let
                reversedNext =
                    List.reverse (curr :: xs)
            in
            case reversedNext of
                newCurr :: rest ->
                    { prev = rest, curr = newCurr, next = [] }

                [] ->
                    ring


fromList : List a -> Maybe (Ring a)
fromList l =
    case l of
        [] ->
            Nothing

        x :: xs ->
            Just { prev = [], curr = x, next = xs }
