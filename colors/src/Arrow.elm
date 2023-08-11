module Arrow exposing (..)

import Html exposing (Html, div)
import Svg
import Svg.Attributes exposing (..)


type Arrow
    = Up
    | Down
    | Left
    | Right


viewArrow : Arrow -> List String -> Html msg
viewArrow arrow classes =
    let
        rotate =
            case arrow of
                Up ->
                    "rotate(270)"

                Down ->
                    "rotate(90)"

                Left ->
                    "rotate(180)"

                Right ->
                    "rotate(0)"

        arrowAttrs =
            [ "arrow", "center-everything" ] |> List.append classes |> List.map class
    in
    div arrowAttrs
        [ Svg.svg
            [ width "24"
            , height "24"
            , fill "currentColor"
            , transform rotate
            ]
            [ Svg.path
                [ d "M7.293 4.707 14.586 12l-7.293 7.293 1.414 1.414L17.414 12 8.707 3.293 7.293 4.707z" ]
                []
            ]
        ]



-- <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24"><path
-- d="M7.293 4.707 14.586 12l-7.293 7.293 1.414 1.414L17.414 12 8.707 3.293 7.293 4.707z"/></svg>
