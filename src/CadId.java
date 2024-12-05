import java.time.Year;

public record CadId(SystemNameType type, ModelType modelType, String modelOrder, String modelVersion) {

    private String getId() {
        String i = "0";
        String ii = "0";

        if (modelType == ModelType.Main_Assembly) {
            return i + ii;
        } else if (modelType == ModelType.Sub_Assembly) {
            i = modelOrder;
        } else if (modelType == ModelType.Part) {
            ii = modelOrder;
        }

        return i + ii;
    }

    public enum SystemNameType {
        ROBOT, SYSTEMS1, BLOCK_BOTS, PROTOTYPE;
    }

    public enum ModelType {
        Main_Assembly, Part, Sub_Assembly;
    }

    public enum Version {
        ONE("1"), TWO("2"), THREE("3"), FOUR("4"), FIVE("5"), SIX("6"), SEVEN("7"), EIGHT("8"), NINE("9");

        private final String number;

        Version(String number) {
            this.number = number;
        }

        public String getNumber() {
            return number;
        }
    }

    public String getCadId() {
        var space = "-";
        return Year.now().getValue() + space + type + space + getId() + modelVersion;
    }
}
