$ (document).ready (function () {
  var board = null;
  var game = new Chess ();
  var $board = $ ('#board');
  var $status = $ ('#game-status');
  var engineThinking = false; // Flag to prevent user moves while AI is thinking

  function onDragStart (source, piece, position, orientation) {
    if (game.game_over () || engineThinking) return false; // Block drag if game over or AI thinking
    if (
      (game.turn () === 'w' && piece.search (/^b/) !== -1) ||
      (game.turn () === 'b' && piece.search (/^w/) !== -1)
    ) {
      return false;
    }
  }

  function onDrop (source, target) {
    engineThinking = true;
    var move = {
      from: source,
      to: target,
      promotion: 'q',
    };

    var possibleMove = game.move (move);
    if (possibleMove === null) {
      engineThinking = false;
      return 'snapback';
    }

    updateStatus ();
    updateBoardPosition ();

    var engineType = $ ('#engine-selector').val (); // Get selected engine type (assuming a selector is added in HTML)
    var apiUrl = '/api/chess/make_move/'; // Default RL-based engine API
    if (engineType === 'traditional') {
      apiUrl = '/api/chess/make_traditional_move/'; // Use traditional engine API if selected
    }

    $.ajax ({
      type: 'POST',
      url: apiUrl,
      contentType: 'application/json',
      dataType: 'json',
      data: JSON.stringify ({
        move: possibleMove.uci (),
        fen: game.fen (),
      }),
      headers: {
        'X-CSRFToken': getCookie ('csrftoken'),
      },
      success: function (data) {
        engineThinking = false; // Reset flag - AI move received
        if (data.error) {
          alert ('Error: ' + data.error);
          game.undo ();
          updateBoardPosition ();
          updateStatus ();
        } else if (data.game_over) {
          updateStatus (true, data.result); // Game over with result
          if (data.ai_move) {
            game.move (data.ai_move);
            updateBoardPosition ();
            updateStatus (true, data.result); // Update status again after AI's final move
          }
          alert ('Game Over! Result: ' + data.result); // Alert game over result
        } else {
          game.move (data.ai_move);
          updateBoardPosition ();
          updateStatus ();
        }
      },
      error: function (xhr, textStatus, errorThrown) {
        engineThinking = false; // Reset flag in case of error
        alert ('Request failed: ' + textStatus + ', ' + errorThrown);
        game.undo ();
        updateBoardPosition ();
        updateStatus ();
      },
    });
  }

  function onSnapEnd () {
    board.position (game.fen ());
  }

  function updateBoardPosition () {
    board.position (game.fen ());
  }

  function updateStatus (gameOver = false, result = null) {
    var statusText = '';
    var turn = game.turn () === 'w'
      ? 'Your move (White)'
      : 'AI is thinking (Black)';
    if (gameOver) {
      $status.addClass ('game-over'); // Add class for game over styling
      if (game.in_checkmate ()) {
        statusText =
          'Checkmate! ' +
          (game.turn () === 'b' ? 'White wins' : 'Black wins') +
          '. Result: ' +
          result;
      } else if (game.in_draw ()) {
        statusText = 'Game drawn. Result: ' + result;
      } else {
        statusText = 'Game over. Result: ' + result; // Should not normally reach here, but for safety
      }
    } else {
      $status.removeClass ('game-over'); // Remove game-over styling
      statusText = turn;
      if (game.in_check ()) {
        statusText +=
          ', ' + (game.turn () === 'w' ? 'White' : 'Black') + ' is in check';
      }
    }
    $status.text (statusText);
  }

  var config = {
    draggable: true,
    position: 'start',
    onDragStart: onDragStart,
    onDrop: onDrop,
    onSnapEnd: onSnapEnd,
    sparePieces: false,
    orientation: 'white', // Player is white
  };

  board = Chessboard ('board', config);
  updateStatus (); // Initial status update
});

// Function to get CSRF token from cookies (for Django AJAX POST requests)
function getCookie (name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== '') {
    const cookies = document.cookie.split (';');
    for (let i = 0; i < cookies.length; i++) {
      let cookie = cookies[i].trim ();
      // Does this cookie string begin with the name we want?
      if (cookie.substring (0, name.length + 1) === name + '=') {
        cookieValue = decodeURIComponent (cookie.substring (name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}
