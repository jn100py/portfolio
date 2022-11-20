
const alignmentSettings = {
    loffset: 564,
    toffset: 128,
    offset2: 42,  // half of the width
    width: 86,
};

const lettersCb = ["a", "b", "c", "d", "e", "f", "g", "h"];
const numbersCb = ["8", "7", "6", "5", "4", "3", "2", "1"];

const loffset = alignmentSettings.loffset;
const offset2 = alignmentSettings.offset2;
const width = alignmentSettings.width;

const bordersLeft = Array.from({length: 9}, (_, i) => i * width)
                    .map(function l (item) {return item + loffset;})
                    .map(function l (item) {return item.toString() + "px";});
const borders2Left = Array.from({length: 9}, (_, i) => i * width)
                    .map(function l (item) {return item + loffset;})
                    .map(function l (item) {return item + offset2;});


const toffset = alignmentSettings.toffset;

const bordersTop = Array.from({length: 9}, (_, i) => i * width)
                    .map(function l (item) {return item + toffset;})
                    .map(function l (item) {return item.toString() + "px";});
const borders2Top = Array.from({length: 9}, (_, i) => i * width)
                    .map(function l (item) {return item + toffset;})
                    .map(function l (item) {return item + offset2;});



function checkValidMove(dollar, dollarThis, newChessboardPos) {

    // if move not valid, piece remains on square

    var currentPossibleMovesStr = dollar("#current_possible_moves").text();
    if (currentPossibleMovesStr !== "") {

        var currentPossibleMoves = JSON.parse(currentPossibleMovesStr);
        var originalChessboardPos = dollarThis.attr("data-origpos");

        var possibleMovesThisPiece = "None";
        if (originalChessboardPos in currentPossibleMoves) {
            possibleMovesThisPiece = currentPossibleMoves[originalChessboardPos];
        }

        if ((possibleMovesThisPiece === "None")  || (!possibleMovesThisPiece.includes(newChessboardPos))) {

            // When you made a valid move with a piece, and you move it for the second time to its original position.
            // That position is not recognized as a value square to move to. And ... the piece is therefore moved back to the original square.

            return 0;
        }
        return 1;
    }
    return 0;
}


function checkAndPerformCastling(dollar, dollarThis, bordersLeft, bordersTop, newChessboardPos) {
    // in case of castling, the Rook also needs to move to another square

    if ((dollarThis.attr('id').includes("piece_king_white")) && ((newChessboardPos === 'c1') || (newChessboardPos === 'g1'))) {
        if (newChessboardPos === 'c1') {

            dollar("img[data-origpos='a1']").css({"left": bordersLeft[3],
                                                   "top": bordersTop[7]
                         }); // d1

        } else {

            dollar("img[data-origpos='h1']").css({"left": bordersLeft[5],
                                                  "top": bordersTop[7]
                         }); // f1

        }
    }
}


function checkAndPerformEnPassant(dollar, dollarThis, newChessboardPos, posHor) {

    var originalChessboardPos = dollarThis.attr("data-origpos");
    if ((dollarThis.attr('id').includes("piece_pawn_white")) &&
            (posHor !== originalChessboardPos.charAt(0)) &&
            (dollar("img[data-origpos=" + newChessboardPos + "]").length === 0)) {

        var posBlackPawn2remove = posHor + '5';
        var idBlackPawn2remove = dollar("img[data-origpos=" + posBlackPawn2remove + "]").attr('id');

        dollar("#" + idBlackPawn2remove).remove();

    }
}


$(function () {

    $("img[id*='img_piece_']").draggable({

        stop: function (event, ui) {

            // A piece that is moved around the board, should be placed in the middle of a square
            // Each square is defined by boundaries.
            // This function makes sure that each piece is positioned exactly inside the square
            // it was moved to, under the condition it was allowed to move to that square.

            var pos = ui.helper.position(); // just get pos.top and pos.left

            for (let i = 0; i < 8; i++) {

                if (pos.left < borders2Left[i]) {
                      var posHor = lettersCb[i];
                      $(this).css("left", bordersLeft[i]);
                      break;
                }
            }

            for (let i = 0; i < 8; i++) {

                if (pos.top < borders2Top[i]) {
                      var posVert = numbersCb[i];
                      $(this).css("top", bordersTop[i]);
                      break;
                }
            }

            var newChessboardPos = posHor + posVert;

            $(this).attr('data-moved', "1");

            var valid = checkValidMove($, $(this), newChessboardPos);
            if (valid === 1) {

                checkAndPerformCastling($, $(this), bordersLeft, bordersTop, newChessboardPos, posHor);
                checkAndPerformEnPassant($, $(this), newChessboardPos);

            } else {

                $(this).attr('data-moved', "0");
                $(this).css({
                    'left': $(this).data('originalLeft'),
                    'top': $(this).data('origionalTop')
                });

            }

            }
    });
});
