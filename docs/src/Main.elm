module Main exposing (main)

import Browser
import Html exposing (Html, div, footer, h1, h2, header, li, text, ul)
import Html.Attributes exposing (class, id)
import Html.Events exposing (onClick)
import Json.Decode as D exposing (Decoder)
import Json.Encode as E


main : Program E.Value Model Msg
main =
    Browser.document
        { init = init
        , view = \model -> { title = "Colors", body = [ view model ] }
        , update = update
        , subscriptions = \_ -> Sub.none
        }


type alias Colorscheme =
    { name : String
    , variants : Ring String
    }


type alias Ring a =
    { prev : List a
    , curr : a
    , next : List a
    }


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


update : Msg -> Model -> ( Model, Cmd Msg )
update msg model =
    case msg of
        NextScheme ->
            ( model, Cmd.none )

        PrevScheme ->
            Debug.todo "branch 'PrevScheme' not implemented"

        NextVariant ->
            Debug.todo "branch 'NextVariant' not implemented"

        PrevVariant ->
            Debug.todo "branch 'PrevVariant' not implemented"


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
    div [ class "main" ]
        [ header []
            [ h1 [ onClick PrevScheme, id "scheme-name" ] [ text curr.name ] ]
        , viewColorDots
        , footer []
            [ h2 [ id "scheme-variant" ] [ text currVariant ] ]
        ]



-- JSON ENCODE/DECODE


decodeRing : Decoder a -> Decoder (Ring a)
decodeRing itemDecoder =
    D.oneOrMore (Ring []) itemDecoder



-- ['a', 'b', 'c'] ==> Ring { prev = [], curr = 'a', next = ['b', 'c']}


decodeColorscheme : Decoder Colorscheme
decodeColorscheme =
    D.map2 Colorscheme (D.index 0 D.string) (D.index 1 (decodeRing D.string))


decoder : D.Decoder Model
decoder =
    decodeRing decodeColorscheme
