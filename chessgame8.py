from flask import Flask, render_template, request
import chess, chess.svg, chess.polyglot
from markupsafe import Markup

p = [0,  0,   0,   0,   0,   0,  0, 0,
                     5, 10,  10, -20, -20,  10, 10, 5,
                     5, -5, -10,   0,   0, -10, -5, 5,
                     0,  0,   0,  20,  20,   0,  0, 0,
                     5,  5,  10,  25,  25,  10,  5, 5,
                     10,10,  20,  30,  30,  20, 10,10,
                     50,50,  50,  50,  50,  50, 50,50,
                     0,  0,  0,    0,   0,   0,  0, 0
                     ]


n = [-50, -40, -30, -30, -30, -30, -40, -50,
                       -40, -20,   0,   0,   0,   0, -20, -40,
                       -30,   5,  10,  15,  15,  10,   5, -30,
                       -30,   0,  15,  20,  20,  15,   0, -30,
                       -30,   5,  15,  20,  20,  15,   5, -30,
                       -30,   0,  10,  15,  15,  10,   0, -30,
                       -40, -20,   0,   5,   5,   0, -20, -40,
                       -50, -40, -30, -30, -30, -30, -40, -50
                       ]
b = [-20,-10,-10,-10,-10,-10,-10,-20,
                       -10,  5,  0,  0,  0,  0,  5,-10,
                       -10, 10, 10, 10, 10, 10, 10,-10,
                       -10,  0, 10, 10, 10, 10,  0,-10,
                       -10,  5,  5, 10, 10,  5,  5,-10,
                       -10,  0,  5, 10, 10,  5,  0,-10,
                       -10,  0,  0,  0,  0,  0,  0,-10,
                       -20,-10,-10,-10,-10,-10,-10,-20
                       ]
r = [ 0, 0,  0,  5,  5,  0,  0,  0,
                     -5, 0,  0,  0,  0,  0,  0, -5,
                     -5, 0,  0,  0,  0,  0,  0, -5,
                     -5, 0,  0,  0,  0,  0,  0, -5,
                     -5, 0,  0,  0,  0,  0,  0, -5,
                     -5, 0,  0,  0,  0,  0,  0, -5,
                      5,10, 10, 10, 10, 10, 10,  5,
                      0, 0,  0,  0,  0,  0,  0,  0
                     ]

q = [-10,   5,   5,  5,  5,   5,   0, -10,
                      -10,   0,   5,  0,  0,   0,   0, -10,
                        0,   0,   5,  5,  5,   5,   0,  -5,
                       -5,   0,   5,  5,  5,   5,   0,  -5,
                      -10,   0,   0,  0,  0,   0,   0, -10,
                      -10,   0,   5,  5,  5,   5,   0, -10,
                      -20, -10, -10, -5, -5, -10, -10, -20,
                      -20, -10, -10, -5, -5, -10, -10, -20
                      ]

k1 = [ 20,  30,  10,   0,   0,  10,  30,  20,
                           20,  20,   0,   0,   0,   0,  20,  20,
                          -10, -20, -20, -20, -20, -20, -20, -10,
                          -20, -30, -30, -40, -40, -30, -30, -20,
                          -30, -40, -40, -50, -50, -40, -40, -30,
                          -30, -40, -40, -50, -50, -40, -40, -30,
                          -30, -40, -40, -50, -50, -40, -40, -30,
                          -30, -40, -40, -50, -50, -40, -40, -30
                          ]

k2 =  [-50, -30,-30,-30,-30,-30, -30, -50,
       -30, -30,  0,  0,  0,  0, -30, -30,
       -30, -10, 20, 30, 30, 20, -10, -30,
       -30, -10, 30, 40, 40, 30, -10, -30,
       -30, -10, 30, 40, 40, 30, -10, -30,
       -30, -10, 20, 30, 30, 20, -10, -30,
       -30, -20,-10,  0,  0,-10, -20, -30,
       -50, -40,-30,-20,-20,-30, -40, -50
          ]
def k(m):
     if m > 13:
          return k1
     else:
          return k2

app = Flask(__name__)
bd = chess.Board()

def brd_svg():
    return Markup(chess.svg.board(bd, size=500))

@app.route("/", methods=["GET", "POST"])
def idx():
    global brd
    err = None
    if request.method == "POST":
        mv = request.form.get("move")
        try:
            bd.push_san(mv)
            if not bd.turn:
                bd.push(ai_mv(4))
        except ValueError:
            err = "Invalid move! Please try again."
    return render_template("index.html", board_svg=brd_svg(), move_error=err)

def ai_mv(d):
    brd = bd
    try:
        #m = chess.polyglot.MemoryMappedReader("human.bin").weighted_choice(brd).move
        m = chess.polyglot.MemoryMappedReader("computer.bin").weighted_choice(brd).move
        #m = chess.polyglot.MemoryMappedReader("pecg_book.bin").weighted_choice(brd).move
        #return m
        raise ValueError
    except:
        bst_mv, bst_val = chess.Move.null(), -float("inf")
        a, b = -float("inf"), float("inf")
        for mv in brd.legal_moves:
            brd.push(mv)
            mv_val = -alphabeta(-b, -a, d - 1)
            brd.pop()
            if mv_val > bst_val:
                bst_val, bst_mv = mv_val, mv
            a = max(a, mv_val)
        return bst_mv

def alphabeta(a, b, d):
    brd = bd
    if d == 0 or brd.is_game_over():
        return eval_brd()
    mx_val = -float("inf")
    for mv in brd.legal_moves:
        brd.push(mv)
        v = -alphabeta(-b, -a, d - 1)
        brd.pop()
        mx_val = max(mx_val, v)
        a = max(a, v)
        if a >= b:
            break
    return mx_val

def eval_brd():
    brd = bd
    if brd.is_checkmate():
        return -float("inf") if brd.turn else float("inf")
    if brd.is_stalemate() or brd.is_insufficient_material():
        return 0

     b_m = (200 * (len(brd.pieces(chess.PAWN, chess.WHITE))) + (640 * (len(brd.pieces(chess.KNIGHT, chess.WHITE))) + (660 * (len(brd.pieces(chess.BISHOP, chess.WHITE))) + (1000 * (len(brd.pieces(chess.ROOK, chess.WHITE))) + (1800 * (len(brd.pieces(chess.QUEEN, chess.WHITE)))
     w_m = (200 * (len(brd.pieces(chess.PAWN, chess.BLACK))) + (640 * (len(brd.pieces(chess.KNIGHT, chess.BLACK))) + (660 * (len(brd.pieces(chess.BISHOP, chess.BLACK))) + (1000 * (len(brd.pieces(chess.ROOK, chess.BLACK))) + (1800 * (len(brd.pieces(chess.QUEEN, chess.BLACK)))
    
     mat_score = b_m - w_m
              
    pos_score = sum([
        sum([p[i] for i in brd.pieces(chess.PAWN, chess.WHITE)]) +
        sum([-p[chess.square_mirror(i)] for i in brd.pieces(chess.PAWN, chess.BLACK)]),
        sum([n[i] for i in brd.pieces(chess.KNIGHT, chess.WHITE)]) +
        sum([-n[chess.square_mirror(i)] for i in brd.pieces(chess.KNIGHT, chess.BLACK)]),
        sum([b[i] for i in brd.pieces(chess.BISHOP, chess.WHITE)]) +
        sum([-b[chess.square_mirror(i)] for i in brd.pieces(chess.BISHOP, chess.BLACK)]),
        sum([r[i] for i in brd.pieces(chess.ROOK, chess.WHITE)]) +
        sum([-r[chess.square_mirror(i)] for i in brd.pieces(chess.ROOK, chess.BLACK)]),
        sum([q[i] for i in brd.pieces(chess.QUEEN, chess.WHITE)]) +
        sum([-q[chess.square_mirror(i)] for i in brd.pieces(chess.QUEEN, chess.BLACK)]),
        sum([k(b_m)[i] for i in brd.pieces(chess.KING, chess.WHITE)]) +
        sum([-k(w_m)[chess.square_mirror(i)] for i in brd.pieces(chess.KING, chess.BLACK)])
    ])
    eval_val = mat_score + pos_score
    return eval_val if brd.turn else -eval_val

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
