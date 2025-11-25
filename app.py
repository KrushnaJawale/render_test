from flask import Flask, render_template, request, jsonify, session, redirect, url_for

# Initialize the Flask application
app = Flask(__name__)
# Set a secret key for session management (required for Flask sessions)
app.secret_key = 'super_secret_tictactoe_key' 

# --- Game State Management Functions ---

def init_game():
    """Initializes or resets the game state."""
    # The board is a list representing a 3x3 grid: [0, 1, 2, 3, 4, 5, 6, 7, 8]
    # ' ' means empty, 'X' and 'O' are player marks
    session['board'] = [''] * 9
    session['current_player'] = 'X'
    session['winner'] = None
    session['game_over'] = False

def check_win(board):
    """Checks the board for a winner. Returns the winner ('X' or 'O') or None."""
    
    # Define all winning combinations (rows, columns, and diagonals)
    winning_combinations = [
        # Rows
        [0, 1, 2], [3, 4, 5], [6, 7, 8],
        # Columns
        [0, 3, 6], [1, 4, 7], [2, 5, 8],
        # Diagonals
        [0, 4, 8], [2, 4, 6]
    ]

    for combo in winning_combinations:
        a, b, c = combo
        if board[a] != '' and board[a] == board[b] and board[a] == board[c]:
            return board[a]  # Return 'X' or 'O'

    # Check for a draw (if all cells are filled and no winner)
    if '' not in board:
        return 'Draw'
        
    return None

# --- Flask Routes ---

@app.route('/', methods=['GET'])
def index():
    """Renders the main game page and initializes the game state on first load."""
    if 'board' not in session:
        init_game()
    return render_template('index.html', game=session)

@app.route('/reset', methods=['POST'])
def reset_game():
    """Resets the game state and redirects to the homepage."""
    init_game()
    # Flash messages could be added here for a better user experience
    return redirect(url_for('index'))


@app.route('/move', methods=['POST'])
def make_move():
    """
    Handles a player's move.
    Expects JSON data: {"cell_index": 0-8}
    """
    if session['game_over']:
        return jsonify({"message": "Game over. Please reset."}), 400

    data = request.get_json()
    cell_index = data.get('cell_index')

    try:
        cell_index = int(cell_index)
        board = session['board']
        player = session['current_player']

        # 1. Validate move
        if not (0 <= cell_index <= 8) or board[cell_index] != '':
            return jsonify({"message": "Invalid move or cell already taken."}), 400

        # 2. Update board
        board[cell_index] = player

        # 3. Check for win/draw
        winner = check_win(board)
        session['winner'] = winner

        if winner:
            session['game_over'] = True
            
        # 4. Switch player if the game is not over
        if not session['game_over']:
            session['current_player'] = 'O' if player == 'X' else 'X'
            
        # 5. Return the updated game state
        return jsonify({
            "success": True,
            "board": board,
            "current_player": session['current_player'],
            "winner": session['winner'],
            "game_over": session['game_over'],
            "last_move_index": cell_index,
            "message": "Move accepted."
        })

    except Exception as e:
        print(f"Error processing move: {e}")
        return jsonify({"message": "Server error processing move."}), 500

if __name__ == '__main__':
    # Flask will look for templates in a 'templates' folder automatically.
    app.run(debug=True)
