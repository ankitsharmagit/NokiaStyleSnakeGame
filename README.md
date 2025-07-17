# Enhanced Python Snake Game

A modern tribute to the classic Nokia snake game, rebuilt from the ground up in Python using the `pygame` library. This project replicates the nostalgic feel of the original while introducing a polished, enhanced user interface and a more engaging gameplay experience.

![Snake game home](https://github.com/user-attachments/assets/5eda806e-75cb-4f5f-92e6-f27f68b38758)

*Inspired by the classic Snake II title screen.*

---

## 🌟 Features

This isn't just a simple remake. This version includes a host of enhancements designed to create a more dynamic and enjoyable experience:

### 🎨 Visual Style (Enhanced Retro Look)

* **Distinct Snake Head:** The snake's head has a unique color and features eyes that move to indicate its direction.
* **Gradient Body:** A smooth color gradient runs down the snake's body, giving it a modern, polished look.
* **Pulsing Food:** The food item subtly pulses, making it easier to spot.
* **High-Contrast Theme:** A classic pale green and charcoal color palette that's easy on the eyes.
* **Prominent UI Text:** The score and menu titles use a larger font for better readability.

### 🎮 Gameplay & Experience

* **Classic Mechanics:** Simple, intuitive controls (arrow keys) and the core "eat and grow" gameplay loop.
* **Screen-Shake on Death:** A brief, intense screen-shake effect provides dramatic feedback when the game ends.
* **Dynamic Sound Effects:** Synthesized sounds for eating food and a dreadful, dissonant sound for game over.
* **Visual Feedback:** A quick screen flash occurs every time the snake eats.
* **Randomized Game Over Messages:** A variety of interesting messages are displayed on the game over screen to add personality.

### 🖥️ User Interface

* **Image-Based Start Screen:** Features the classic "Snake II" title image for a touch of nostalgia.
* **Interactive Menus:** Clean, highlighted menus for easy navigation and difficulty selection.
* **Three Difficulty Levels:** Choose from Easy, Medium, or Hard to match your skill level.
* **Custom "Game Over" Screen:** A uniquely styled game over screen with a dark red title and a bolded "ENTER" prompt.

---

## 🛠️ Requirements

To run this game, you will need:

* **Python 3.x**
* **Pygame** library

---

## 🚀 Installation

1.  **Clone the repository:**
    ```bash
    git clone [https://github.com/your-username/your-repo-name.git](https://github.com/your-username/your-repo-name.git)
    cd your-repo-name
    ```

2.  **Install Pygame:**
    If you don't have it installed, you can get it via pip:
    ```bash
    pip install pygame
    ```

---

## ▶️ How to Play

1.  **Run the script:**
    ```bash
    python main.py
    ```
    *(Assuming your main game file is named `main.py`)*

2.  **Select a Difficulty:**
    * Use the **UP** and **DOWN** arrow keys to navigate the menu.
    * Press **ENTER** to confirm your selection.

3.  **Control the Snake:**
    * Use the **ARROW KEYS** (Up, Down, Left, Right) to change the snake's direction.
    * Your goal is to eat the food to grow longer and increase your score.

4.  **Avoid Collisions:**
    * The game ends if you run into the outer walls or into the snake's own body.

---

## ✨ Acknowledgements

This game was developed with the assistance of Google's Gemini, which helped in generating code, creating prompts, and refining the overall game design and features.

---

## 🤖 Development Prompt

For those interested in the development process, this game was generated based on the following detailed prompt provided to Google's Gemini.

<details>
<summary>Click to view the full prompt</summary>

### **Prompt for Generating an Enhanced Python Snake Game**

Please develop a complete, end-to-end Snake game in Python using the `pygame` library. The game must replicate the classic feel of the snake game found on old Nokia mobile phones but with a significantly enhanced user interface and improved gameplay experience.

**1. Core Objective:**
Create a fully playable and highly polished Snake game that is self-contained in a single Python script.

**2. Visual Style (Enhanced Retro Look):**
* **Color Palette:** Use a high-contrast, monochrome theme with a pale green background (e.g., `#c7f0d8`) and dark charcoal foreground elements (e.g., `#43523d`).
* **Snake Appearance:**
    * **Head:** The snake's head must be a distinct, darker color. It must feature two white "eyes" that change position to indicate the snake's current direction of movement.
    * **Body:** The snake's body must have a smooth gradient, transitioning from the head color to a lighter shade at the tail.
* **Food Appearance:** The food should have a subtle pulsing animation to make it stand out.
* **UI Text:** Important text elements like the main menu title ("SELECT DIFFICULTY") and the in-game "SCORE" display must use a larger, more prominent font to be easily distinguishable.

**3. Gameplay Mechanics & Experience:**
* **The Snake:** The player controls a snake made of square segments that is always in motion.
* **Controls:** The player must be able to change the snake's direction using the four arrow keys. The snake cannot immediately reverse its direction.
* **Eating & Effects:**
    * When the snake eats the food, its length increases, and the score is updated.
    * Eating food must trigger immediate sensory feedback: a brief **screen flash** and a simple, synthesized **"eat" sound effect**.
* **Game Over & Effects:**
    * The game ends if the snake's head collides with the outer border or its own body.
    * A brief, intense **screen-shake effect** must occur upon collision.
    * The "GAME OVER" title must be displayed in a dreadful, dark red color.
    * A dramatic, dissonant **"game over" sound effect** must play when the game ends.
    * The game over screen must display a **randomized, interesting message** (e.g., "The snake rests," "You've been outsnaked.") along with the final score.

**4. Game Flow and User Interface:**
* **Start Screen:**
    * Upon launching, display a start screen featuring the `Snake-II-Featured.jpg` image as the main title banner.
    * The screen must feature an interactive menu to select the difficulty level. The player can navigate this menu using the Up/Down arrow keys and confirm with Enter. The currently selected option must be visually highlighted.
* **Difficulty Levels:**
    * The game must have three difficulty levels (Easy, Medium, Hard) that control the snake's speed.
* **In-Game HUD:**
    * The current score must be clearly visible at all times in a UI panel at the top of the screen, using the prominent UI font.
* **Game Over Screen:**
    * Display the "GAME OVER" title, the randomized message, the final score, and a prompt to restart.
    * The "Press ENTER to Play Again" prompt must be rendered with only the word "ENTER" appearing in a **bold** style.

**5. Technical Requirements:**
* **Language:** Python 3.
* **Library:** Use the `pygame` library for all graphics, sound, event handling, and game loop management.
* **Code Structure:** The code should be well-organized and commented, using classes for `Snake` and `Food` objects, and functions for game states.
* **Deliverable:** The final output should be a single, complete, and runnable `.py` file.

</details>

---

## 📄 License

This project is licensed under the MIT License. See the `LICENSE` file for details.
