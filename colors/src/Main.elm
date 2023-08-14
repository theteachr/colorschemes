module Main exposing (main)

import Arrow exposing (Arrow, viewArrow)
import Browser
import Browser.Events as Events
import Html exposing (Html, div, footer, h1, h2, header, li, text, ul)
import Html.Attributes exposing (class, id)
import Html.Events exposing (onClick)
import Json.Decode as D exposing (Decoder)
import Json.Encode as E
import Ring exposing (..)


main : Program E.Value Model Msg
main =
    Browser.element
        { init = init
        , view = view
        , update = update
        , subscriptions = subscriptions
        }


type alias Colorscheme =
    { name : String
    , variants : Ring String
    }


className : Colorscheme -> String
className { name, variants } =
    let
        hyphenatedName =
            String.replace " " "-" <| String.toLower name

        variantName =
            variants.curr
    in
    hyphenatedName ++ "-" ++ variantName


type alias Model =
    Ring Colorscheme


type ButtonState
    = Enabled
    | Disabled


defaultScheme : Colorscheme
defaultScheme =
    { name = "Rose"
    , variants = { prev = [], curr = "main", next = [] }
    }


emptyModel : { prev : List a, curr : Colorscheme, next : List b }
emptyModel =
    { prev = [], curr = defaultScheme, next = [] }


init : E.Value -> ( Model, Cmd Msg )
init flags =
    ( case D.decodeValue decoder flags of
        Ok model ->
            model

        Err _ ->
            emptyModel
    , Cmd.none
    )


type Msg
    = NextScheme
    | PrevScheme
    | NextVariant
    | PrevVariant


advanceVariant : (Ring String -> Ring String) -> Model -> Model
advanceVariant advance ({ curr } as model) =
    let
        scheme =
            { curr | variants = advance curr.variants }
    in
    { model | curr = scheme }


update : Msg -> Model -> ( Model, Cmd Msg )
update msg model =
    case msg of
        NextScheme ->
            ( forward model, Cmd.none )

        PrevScheme ->
            ( backward model, Cmd.none )

        NextVariant ->
            ( advanceVariant forward model, Cmd.none )

        PrevVariant ->
            ( advanceVariant backward model, Cmd.none )


arrowOfMsg : Msg -> Arrow
arrowOfMsg msg =
    case msg of
        PrevScheme ->
            Arrow.Up

        NextScheme ->
            Arrow.Down

        PrevVariant ->
            Arrow.Left

        NextVariant ->
            Arrow.Right


classOfMsg : Msg -> Html.Attribute msg
classOfMsg msg =
    let
        msgClass =
            case msg of
                PrevScheme ->
                    "prev-scheme"

                NextScheme ->
                    "next-scheme"

                PrevVariant ->
                    "prev-variant"

                NextVariant ->
                    "next-variant"
    in
    class msgClass


colorNames : List String
colorNames =
    [ "red", "green", "yellow", "blue", "magenta", "cyan" ]



-- VIEW


view : Model -> Html Msg
view { curr } =
    let
        currVariant =
            curr.variants.curr

        variantNavButtonState =
            if Ring.length curr.variants == 1 then
                Disabled

            else
                Enabled
    in
    div [ id "main", class (className curr) ]
        [ header [ class "row-fill" ]
            [ viewDominantRow h1 "scheme-name" curr.name
            , viewSpan PrevScheme
            , viewSpan NextScheme
            ]
        , viewNavButton Enabled PrevScheme
        , viewNavButton Enabled NextScheme
        , viewColorDots
        , viewNavButton variantNavButtonState PrevVariant
        , viewNavButton variantNavButtonState NextVariant
        , footer [ class "row-fill" ]
            [ viewDominantRow h2 "scheme-variant" currVariant
            , viewSpan PrevVariant
            , viewSpan NextVariant
            ]
        ]


viewColorBlock : String -> Html Msg
viewColorBlock colorName =
    li []
        [ div
            [ class "color-block"
            , class colorName
            ]
            []
        ]


viewDominantRow : (List (Html.Attribute msg) -> List (Html a) -> b) -> String -> String -> b
viewDominantRow element eyeDee content =
    element
        [ class "row-fill"
        , id eyeDee
        , class "center-everything"
        ]
        [ text content ]


viewSpan : Msg -> Html Msg
viewSpan msg =
    let
        stile =
            case msg of
                PrevScheme ->
                    "left-span"

                NextScheme ->
                    "right-span"

                NextVariant ->
                    "right-span"

                PrevVariant ->
                    "left-span"
    in
    div [ class stile, onClick msg ] []


viewNavButton : ButtonState -> Msg -> Html Msg
viewNavButton state msg =
    let
        -- Appending the `onClick` attribute to a list of common attributes
        -- when the state is `Enabled` didn't work.
        -- Dealing with the repetition :(
        ( arrowAttrs, wrapperAttrs ) =
            case state of
                Disabled ->
                    ( [ "disabled" ]
                    , [ classOfMsg msg
                      , class "center-everything"
                      , class "btn-wrapper"
                      , class "disabled"
                      ]
                    )

                Enabled ->
                    ( []
                    , [ onClick msg
                      , classOfMsg msg
                      , class "center-everything"
                      , class "btn-wrapper"
                      ]
                    )
    in
    div
        wrapperAttrs
        [ viewArrow (arrowOfMsg msg) arrowAttrs ]


viewColorDots : Html Msg
viewColorDots =
    ul [ class "blocks" ]
        (colorNames
            |> List.map viewColorBlock
        )



-- SUBSCRIPTIONS


subscriptions : Model -> Sub Msg
subscriptions _ =
    Events.onKeyPress getPressedKey


msgFromChar : Char -> Maybe Msg
msgFromChar c =
    case c of
        'h' ->
            Just PrevVariant

        'j' ->
            Just NextScheme

        'k' ->
            Just PrevScheme

        'l' ->
            Just NextVariant

        _ ->
            Nothing



-- DECODERS


getPressedKey : Decoder Msg
getPressedKey =
    D.field "key" D.string |> D.andThen decodeMsg


decodeMsg : String -> Decoder Msg
decodeMsg pressed =
    case String.uncons pressed of
        Just ( c, "" ) ->
            case msgFromChar c of
                Just msg ->
                    D.succeed msg

                Nothing ->
                    D.fail "Unsupported key"

        _ ->
            D.fail "Probably a control char was entered"


decodeRing : Decoder a -> Decoder (Ring a)
decodeRing itemDecoder =
    D.oneOrMore (Ring []) itemDecoder


decodeColorscheme : Decoder Colorscheme
decodeColorscheme =
    D.map2 Colorscheme (D.index 0 D.string) (D.index 1 (decodeRing D.string))


decoder : D.Decoder Model
decoder =
    decodeRing decodeColorscheme
