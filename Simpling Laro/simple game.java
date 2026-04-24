puzzleGame

import javax.swing.*;
import java.awt.*;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.util.ArrayList;
import java.util.Collections;

public class SlidingPuzzleGame extends JFrame {
    private final int gridSize = 4; // 4x4 grid
    private JButton[][] buttons = new JButton[gridSize][gridSize];
    private JPanel panel;
    private int emptyRow = gridSize - 1;
    private int emptyCol = gridSize - 1;

    public SlidingPuzzleGame() {
        setTitle("Sliding Puzzle Game");
        setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        setSize(400, 400);
        setLocationRelativeTo(null);

        panel = new JPanel(new GridLayout(gridSize, gridSize));
        initializeGame();
        add(panel);

        setVisible(true);
    }

    private void initializeGame() {
        ArrayList<String> tiles = new ArrayList<>();
        for (int i = 1; i < gridSize * gridSize; i++) {
            tiles.add(String.valueOf(i));
        }
        tiles.add(""); // Empty tile
        Collections.shuffle(tiles); // Shuffle the tiles

        int k = 0;
        for (int i = 0; i < gridSize; i++) {
            for (int j = 0; j < gridSize; j++) {
                String value = tiles.get(k++);
                JButton button = new JButton(value);
                button.setFont(new Font("Arial", Font.BOLD, 20));
                buttons[i][j] = button;
                panel.add(button);

                if (value.equals("")) {
                    emptyRow = i;
                    emptyCol = j;
                } else {
                    button.addActionListener(new ButtonClickListener(i, j));
                }
            }
        }
    }

    private void swapTiles(int row, int col) {
        String temp = buttons[row][col].getText();
        buttons[row][col].setText("");
        buttons[emptyRow][emptyCol].setText(temp);

        // Update action listeners
        buttons[row][col].removeActionListener(buttons[row][col].getActionListeners()[0]);
        buttons[emptyRow][emptyCol].addActionListener(new ButtonClickListener(row, col));
        buttons[row][col].addActionListener(null);

        emptyRow = row;
        emptyCol = col;
    }

    private boolean isAdjacentToEmpty(int row, int col) {
        return (row == emptyRow && Math.abs(col - emptyCol) == 1)
                || (col == emptyCol && Math.abs(row - emptyRow) == 1);
    }

    private boolean isSolved() {
        int k = 1;
        for (int i = 0; i < gridSize; i++) {
            for (int j = 0; j < gridSize; j++) {
                String text = buttons[i][j].getText();
                if (i == gridSize - 1 && j == gridSize - 1) {
                    return text.equals("");
                }
                if (!text.equals(String.valueOf(k))) {
                    return false;
                }
                k++;
            }
        }
        return true;
    }

    private void showWinMessage() {
        JOptionPane.showMessageDialog(this, "Congratulations! You solved the puzzle!");
    }

    private class ButtonClickListener implements ActionListener {
        private final int row;
        private final int col;

        public ButtonClickListener(int row, int col) {
            this.row = row;
            this.col = col;
        }

        @Override
        public void actionPerformed(ActionEvent e) {
            if (isAdjacentToEmpty(row, col)) {
                swapTiles(row, col);
                if (isSolved()) {
                    showWinMessage();
                }
            }
        }
    }

    public static void main(String[] args) {
        SwingUtilities.invokeLater(SlidingPuzzleGame::new);
    }
}


AppleGame


import javax.swing.*;
import java.awt.*;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.awt.event.KeyEvent;
import java.awt.event.KeyListener;

public class CatchTheAppleGame extends JFrame {
    private GamePanel gamePanel;

    public CatchTheAppleGame() {
        setTitle("Catch the Apple");
        setSize(400, 600);
        setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        setResizable(false);

        gamePanel = new GamePanel();
        add(gamePanel);

        setVisible(true);
    }

    public static void main(String[] args) {
        SwingUtilities.invokeLater(CatchTheAppleGame::new);
    }
}

class GamePanel extends JPanel implements ActionListener, KeyListener {
    private int basketX = 150; // Initial basket position
    private int basketWidth = 100, basketHeight = 20;
    private int appleX = 150, appleY = 0; // Initial apple position
    private int appleSize = 20;
    private int score = 0;
    private Timer timer;

    public GamePanel() {
        setBackground(Color.LIGHT_GRAY);
        setFocusable(true);
        addKeyListener(this);

        timer = new Timer(30, this);
        timer.start();
    }

    @Override
    protected void paintComponent(Graphics g) {
        super.paintComponent(g);

        // Draw basket
        g.setColor(Color.BLUE);
        g.fillRect(basketX, getHeight() - basketHeight - 10, basketWidth, basketHeight);

        // Draw apple
        g.setColor(Color.RED);
        g.fillOval(appleX, appleY, appleSize, appleSize);

        // Draw score
        g.setColor(Color.BLACK);
        g.setFont(new Font("Arial", Font.BOLD, 16));
        g.drawString("Score: " + score, 10, 20);
    }

    @Override
    public void actionPerformed(ActionEvent e) {
        // Move apple down
        appleY += 5;

        // Check if apple hits the basket
        if (appleY + appleSize >= getHeight() - basketHeight - 10 &&
            appleX + appleSize >= basketX &&
            appleX <= basketX + basketWidth) {
            score++;
            resetApple();
        }

        // Check if apple hits the ground
        if (appleY > getHeight()) {
            resetApple();
        }

        repaint();
    }

    private void resetApple() {
        appleY = 0;
        appleX = (int) (Math.random() * (getWidth() - appleSize));
    }

    @Override
    public void keyPressed(KeyEvent e) {
        if (e.getKeyCode() == KeyEvent.VK_LEFT && basketX > 0) {
            basketX -= 15;
        }
        if (e.getKeyCode() == KeyEvent.VK_RIGHT && basketX < getWidth() - basketWidth) {
            basketX += 15;
        }
    }

    @Override
    public void keyReleased(KeyEvent e) {
        // Not used
    }

    @Override
    public void keyTyped(KeyEvent e) {
        // Not used
    }
}

