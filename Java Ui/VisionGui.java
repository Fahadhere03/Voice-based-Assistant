import java.awt.*;
import java.awt.event.*;
import java.io.*;

import javax.swing.*;

public class VisionGui extends JFrame implements ActionListener {

    private JLabel label;
    private JButton startButton;
    private JButton exitButton;
    private Process process;
    private JTextArea textArea;

    public VisionGui() {
        initComponents();
    }

    private void initComponents() {
        label = new JLabel();
        label.setIcon(new ImageIcon("C:\\Vision\\Media\\Background.png"));
        label.setMinimumSize(new Dimension(1021, 551));
        label.setPreferredSize(new Dimension(1021, 551));

        startButton = new JButton("START");
        startButton.setFont(new Font("Lucida Sans Unicode", Font.BOLD, 14));
        startButton.setCursor(new Cursor(Cursor.HAND_CURSOR));
        startButton.setFocusPainted(false);
        startButton.addActionListener(this);
        startButton.setBorder(BorderFactory.createCompoundBorder(
                BorderFactory.createLineBorder(Color.darkGray, 3),
                BorderFactory.createEmptyBorder(30, 10, 30, 60)));

        exitButton = new JButton("Exit");
        exitButton.setFont(new Font("Lucida Sans Unicode", Font.BOLD, 14));
        exitButton.setCursor(new Cursor(Cursor.HAND_CURSOR));
        exitButton.setFocusPainted(false);
        exitButton.addActionListener(this);
        exitButton.setBorder(BorderFactory.createCompoundBorder(
                BorderFactory.createLineBorder(Color.WHITE, 3),
                BorderFactory.createEmptyBorder(30, 30, 30, 30)));

        JPanel buttonPanel = new JPanel(new BorderLayout());
        buttonPanel.add(startButton, BorderLayout.WEST);
        buttonPanel.add(exitButton, BorderLayout.EAST);

        textArea = new JTextArea(10, 20);
        textArea.setEditable(false);
        JScrollPane scrollPane = new JScrollPane(textArea);

        JPanel imagePanel = new JPanel(new BorderLayout());
        imagePanel.add(label, BorderLayout.CENTER);

        JPanel contentPane = new JPanel(new BorderLayout());
        contentPane.add(imagePanel, BorderLayout.CENTER);
        contentPane.add(buttonPanel, BorderLayout.SOUTH);
        contentPane.add(scrollPane, BorderLayout.EAST);

        setContentPane(contentPane);
        setTitle("Vision");
        setSize(1018, 583);
        setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        setLocationRelativeTo(null);
    }

    private void startPythonScript() {
        try {
            process = Runtime.getRuntime().exec("python Vision.py");
            InputStream stdout = process.getInputStream();
            BufferedReader reader = new BufferedReader(new InputStreamReader(stdout));
            String line;
            while ((line = reader.readLine()) != null) {
                textArea.append(line + "\n");
            }
        } catch (IOException e) {
            e.printStackTrace();
        }
    }

    private void stopPythonScript() {
        if (process != null) {
            process.destroy();
            try {
                process.waitFor(); // wait for the process to terminate
            } catch (InterruptedException e) {
                e.printStackTrace();
            }
        }
    }

    @Override
    public void actionPerformed(ActionEvent e) {
        if (e.getSource() == startButton) {
            startPythonScript();
        } else if (e.getSource() == exitButton) {
            stopPythonScript();
            dispose();
        }
    }

    public static void main(String[] args) {
        SwingUtilities.invokeLater(() -> {
            new VisionGui().setVisible(true);
        });
    }
}
