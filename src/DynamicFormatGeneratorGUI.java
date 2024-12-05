import javax.swing.*;
import java.awt.*;
import java.awt.event.ActionEvent;
import java.awt.event.ItemEvent;

public class DynamicFormatGeneratorGUI extends JFrame {
    private final FormatGenerator formatGenerator = new FormatGenerator();
// GPT :SKULL:
    private final JComboBox<CadId.SystemNameType> systemNameTypeBox;
    private final JComboBox<CadId.ModelType> modelTypeBox;
    private final JComboBox<FormatId.PartsName> partsNameBox;
    private final JComboBox<FormatId.Plate> plateBox;
    private final JComboBox<FormatId.Motor> motorBox;
    private final JComboBox<FormatId.ManufactureMethod> manufactureMethodBox;
    private final JTextField orderField;
    private final JTextField versionField;
    private final JTextField widthField;
    private final JTextArea outputArea;

    public DynamicFormatGeneratorGUI() {
        setTitle("Dynamic Format Generator");
        setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        setSize(500, 500);
        setLocationRelativeTo(null);
        setLayout(new BorderLayout());

        // Top panel for inputs
        JPanel inputPanel = new JPanel(new GridLayout(9, 2, 10, 10));
        inputPanel.setBorder(BorderFactory.createEmptyBorder(10, 10, 10, 10));

        // Adding input fields
        inputPanel.add(new JLabel("System Name Type:"));
        systemNameTypeBox = new JComboBox<>(CadId.SystemNameType.values());
        inputPanel.add(systemNameTypeBox);

        inputPanel.add(new JLabel("Model Type:"));
        modelTypeBox = new JComboBox<>(CadId.ModelType.values());
        modelTypeBox.addItemListener(this::handleModelTypeChange);
        inputPanel.add(modelTypeBox);

        inputPanel.add(new JLabel("Parts Name:"));
        partsNameBox = new JComboBox<>(FormatId.PartsName.values());
        partsNameBox.addItemListener(this::handlePartsNameChange);
        inputPanel.add(partsNameBox);

        inputPanel.add(new JLabel("Plate:"));
        plateBox = new JComboBox<>(FormatId.Plate.values());
        plateBox.addItemListener(this::handlePlateChange);
        inputPanel.add(plateBox);

        inputPanel.add(new JLabel("Motor:"));
        motorBox = new JComboBox<>(FormatId.Motor.values());
        inputPanel.add(motorBox);

        inputPanel.add(new JLabel("Manufacture Method:"));
        manufactureMethodBox = new JComboBox<>(FormatId.ManufactureMethod.values());
        inputPanel.add(manufactureMethodBox);

        inputPanel.add(new JLabel("Order:"));
        orderField = new JTextField();
        inputPanel.add(orderField);

        inputPanel.add(new JLabel("Version:"));
        versionField = new JTextField();
        inputPanel.add(versionField);

        inputPanel.add(new JLabel("Width:"));
        widthField = new JTextField();
        inputPanel.add(widthField);

        // Bottom panel for buttons and output
        JPanel bottomPanel = new JPanel(new BorderLayout());
        JButton generateButton = new JButton("Generate Format");
        generateButton.addActionListener(this::generateFormat);
        bottomPanel.add(generateButton, BorderLayout.NORTH);

        outputArea = new JTextArea();
        outputArea.setEditable(false);
        outputArea.setLineWrap(true);
        outputArea.setWrapStyleWord(true);
        bottomPanel.add(new JScrollPane(outputArea), BorderLayout.CENTER);

        // Adding panels to frame
        add(inputPanel, BorderLayout.CENTER);
        add(bottomPanel, BorderLayout.SOUTH);

        // Initial visibility setup
        updateVisibility();
    }

    private void handleModelTypeChange(ItemEvent e) {
        if (e.getStateChange() == ItemEvent.SELECTED) {
            updateVisibility();
        }
    }

    private void handlePartsNameChange(ItemEvent e) {
        if (e.getStateChange() == ItemEvent.SELECTED) {
            updateVisibility();
        }
    }

    private void handlePlateChange(ItemEvent e) {
        if (e.getStateChange() == ItemEvent.SELECTED) {
            updateVisibility();
        }
    }

    private void updateVisibility() {
        CadId.ModelType modelType = (CadId.ModelType) modelTypeBox.getSelectedItem();
        FormatId.PartsName partsName = (FormatId.PartsName) partsNameBox.getSelectedItem();
        FormatId.Plate plate = (FormatId.Plate) plateBox.getSelectedItem();

        // PartsName visibility (invisible if ModelType is Main_Assembly)
        partsNameBox.setEnabled(modelType != CadId.ModelType.Main_Assembly);

        // Plate visibility (invisible if PartsName is not PLATE)
        plateBox.setEnabled(partsName == FormatId.PartsName.PLATE);

        // Width visibility (invisible if Plate is not Aluminium)
        widthField.setEnabled(plate == FormatId.Plate.Aluminium);

        // Motor visibility (invisible if PartsName is not MOTOR)
        motorBox.setEnabled(partsName == FormatId.PartsName.MOTOR);

        // ManufactureMethod visibility (invisible if ModelType is not Part)
        manufactureMethodBox.setEnabled(modelType == CadId.ModelType.Part);
    }

    private void generateFormat(ActionEvent e) {
        try {
            // Retrieving inputs
            CadId.SystemNameType systemNameType = (CadId.SystemNameType) systemNameTypeBox.getSelectedItem();
            CadId.ModelType modelType = (CadId.ModelType) modelTypeBox.getSelectedItem();
            FormatId.PartsName partsName = partsNameBox.isEnabled() ? (FormatId.PartsName) partsNameBox.getSelectedItem() : null;
            FormatId.Plate plate = plateBox.isEnabled() ? (FormatId.Plate) plateBox.getSelectedItem() : null;
            FormatId.Motor motor = motorBox.isEnabled() ? (FormatId.Motor) motorBox.getSelectedItem() : null;
            FormatId.ManufactureMethod manufactureMethod = manufactureMethodBox.isEnabled()
                    ? (FormatId.ManufactureMethod) manufactureMethodBox.getSelectedItem()
                    : null;
            String order = orderField.getText().trim();
            String version = versionField.getText().trim();
            int width = widthField.isEnabled() && !widthField.getText().trim().isEmpty()
                    ? Integer.parseInt(widthField.getText().trim())
                    : -1;

            // Generating format
            String format = formatGenerator.getFormat(
                    systemNameType,
                    modelType,
                    order,
                    version,
                    partsName,
                    motor,
                    plate,
                    width,
                    manufactureMethod
            );

            outputArea.setText("Generated Format:\n" + format);
        } catch (Exception ex) {
            outputArea.setText("Error: " + ex.getMessage());
        }
    }

    public static void main(String[] args) {
        SwingUtilities.invokeLater(() -> {
            DynamicFormatGeneratorGUI gui = new DynamicFormatGeneratorGUI();
            gui.setVisible(true);
        });
    }
}
