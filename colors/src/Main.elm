module Main exposing (main)

import Browser
import Browser.Events as Events
import Html exposing (Html, div, footer, h1, h2, header, li, text, ul)
import Html.Attributes exposing (class, id)
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


colorNames : List String
colorNames =
    [ "red", "green", "yellow", "blue", "magenta", "cyan" ]


colorBlock : String -> Html Msg
colorBlock colorName =
    li []
        [ div [ class ("color-block " ++ colorName) ] []
        ]


viewColorDots : Html Msg
viewColorDots =
    ul [ class "blocks" ]
        (colorNames
            |> List.map colorBlock
        )


view : Model -> Html Msg
view { curr } =
    let
        currVariant =
            curr.variants.curr
    in
    div [ id "main", class (className curr) ]
        [ header []
            [ h1 [ id "scheme-name" ] [ text curr.name ] ]
        , viewColorDots
        , footer []
            [ h2 [ id "scheme-variant" ] [ text currVariant ] ]
        ]



-- SUBSCRIPTIONS
-- TODO: Listen for tap events


subscriptions : Model -> Sub Msg
subscriptions _ =
    Sub.batch
        [ Events.onKeyPress getPressedKey
        , Events.onClick <| D.succeed NextScheme
        ]


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
