public record FormatId(
        CadId.ModelType modelType,
        PartsName partsName,
        Motor motor,
        Plate plate,
        ManufactureMethod manufactureMethod
) {

    public enum PartsName {
        PLATE, WHEELS, PROFILE, GEAR, PULLEY, PLA, SHAFTS, MOTOR, SPROCKETS;
    }

    public enum Motor {
        Neo_Motor, Neo_Vortex, Kraken_motor, Baby_NEO;
    }

    public enum Plate {
        Aluminium(1), Wood(-1), Polycarbonate(-1);

        private int width;

        Plate(int width) {
            this.width = width;
        }

        public int getWidth() {
            return width;
        }

        public void setWidth(int width) {
            if (this == Aluminium) {
                this.width = width;
            } else {
                throw new UnsupportedOperationException("Cannot change width of this plate.");
            }
        }
    }

    public enum ManufactureMethod {
        CNC("CNC"), _3D("3D"), LASER("LASER"), MANUAL("MANUAL"), SPONSORS("SPONSORS");

        private final String content;

        ManufactureMethod(String content) {
            this.content = content;
        }

        public String getContent() {
            return content;
        }
    }

    private String getPart(int width) {
        var space = "-";
        if (partsName == PartsName.PLATE && plate == Plate.Aluminium) {
            Plate.Aluminium.setWidth(width);
            return partsName + space + plate + plate.getWidth();
        }
        if (partsName == PartsName.MOTOR && motor != null) {
            return partsName + space + motor.name();
        }
        if (partsName != null) {
            return partsName.name();
        }
        return "";
    }

    private String getManufacture() {
        return modelType == CadId.ModelType.Main_Assembly ? "" : manufactureMethod.getContent();
    }

    public String getFormatId(int width) {
        if (modelType != CadId.ModelType.Part) {
            return "";
        }
        var space = "-";
        String part = getPart(width);
        String manufacture = getManufacture();

        return part.isEmpty() ? manufacture : part + space + manufacture;
    }
}
