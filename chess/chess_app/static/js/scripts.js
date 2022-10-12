
function buildStelling(stellingIn) {

    var stelling = stellingIn.split(",,");
    var counters = {"bpawn": 1, "wpawn": 1, "brook": 1, "wrook": 1, "bbishop": 1, "wbishop": 1,
                    "bknight": 1, "wknight": 1, "bqueen": 1, "wqueen": 1, "bking": 1, "wking": 1 };

    for (let i = 0; i < stelling.length; i++) {
        var pieceInfo = stelling[i].split(",");

        pieceName = pieceInfo[0];
        pieceColor = pieceInfo[1];
        piecePositionLeft = pieceInfo[2];
        piecePositionTop = pieceInfo[3];
        piecePosLetterNr = pieceInfo[4];

        imgIdTemplate = "img_piece_A_B_C";
        imgId = imgIdTemplate.replace("A", pieceName)
                                 .replace("B", pieceColor)
                                 .replace("C", counters[pieceColor[0] + pieceName]);
        counters[pieceColor[0] + pieceName] += 1;

        $("#" + imgId).css({"left": "VALpx".replace("VAL", piecePositionLeft),
                            "top": "VALpx".replace("VAL", piecePositionTop)});

        $("#" + imgId).addClass("on_board");
        $("#" + imgId).attr('data-origpos', piecePosLetterNr);
        $("#" + imgId).attr('data-moved', 0);

        $("#" + imgId).data({
            'originalLeft': $("#" + imgId).css('left'),
            'origionalTop': $("#" + imgId).css('top')
        });

    }

    $('img[id*="img_piece_"]').not('[class*="on_board"]').remove();
}


function checkStellingConsistency() {

    var nrPiecesMoved = 0;
    $("img[id*='img_piece_']").each(function () {

        if ($(this).attr('data-moved') === "1") {
            nrPiecesMoved += 1;
        }

    });

    if (nrPiecesMoved === 0) {

        $("#message").text("You must make a move!");
        return 0;

    }

    if (nrPiecesMoved > 1) {

        $("#message").text("Only 1 move is allowed!");
        return 0;

    }

    return 1;

}

