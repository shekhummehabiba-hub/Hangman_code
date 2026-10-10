let gameId = null;


// Start new game
async function newGame() {

    try {

        const response = await fetch("/api/new-game", {

            method: "POST",

            headers: {
                "Content-Type": "application/json"
            }

        });

        const data = await response.json();

        gameId = data.game_id;

        document.getElementById("word").textContent =
            data.word.split("").join(" ");

        document.getElementById("attempts").textContent =
            data.attempts_left;

        document.getElementById("wrongLetters").textContent =
            "None";

        document.getElementById("message").textContent =
            "";

        document.getElementById("letterInput").value = "";

        document.getElementById("letterInput").focus();

    }

    catch (error) {

        console.error(error);

        document.getElementById("message").textContent =
            "Something went wrong!";
    }
}


// Guess letter
async function guessLetter() {

    const input =
        document.getElementById("letterInput");

    const letter =
        input.value.toLowerCase();

    if (!letter) {

        document.getElementById("message").textContent =
            "Please enter a letter.";

        return;
    }

    try {

        const response = await fetch("/api/guess", {

            method: "POST",

            headers: {
                "Content-Type": "application/json"
            },

            body: JSON.stringify({

                game_id: gameId,

                letter: letter

            })

        });

        const data = await response.json();

        if (!response.ok) {

            document.getElementById("message").textContent =
                data.error;

            input.value = "";

            return;
        }

        // Update word
        document.getElementById("word").textContent =
            data.word.split("").join(" ");

        // Update attempts
        document.getElementById("attempts").textContent =
            data.attempts_left;

        // Update wrong letters
        document.getElementById("wrongLetters").textContent =
            data.wrong_letters.length > 0
                ? data.wrong_letters.join(", ")
                : "None";

        // Clear input
        input.value = "";

        // Game finished
        if (data.game_over) {

            if (data.won) {

                document.getElementById("message").textContent =
                    "🎉 Congratulations! You Won!";

            }

            else {

                document.getElementById("message").textContent =
                    "😢 Game Over! Word was: " +
                    data.correct_word;

            }

        }

        else {

            document.getElementById("message").textContent =
                "";

        }

    }

    catch (error) {

        console.error(error);

        document.getElementById("message").textContent =
            "Server error!";
    }
}


// Press Enter to guess
document
    .getElementById("letterInput")
    .addEventListener("keypress", function(event) {

        if (event.key === "Enter") {

            guessLetter();

        }

    });


// Automatically start game
newGame();