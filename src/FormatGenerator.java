public class FormatGenerator {
/***
 * List Of Invisible Buttons On GUI + LOGIC:
 * PartsName - If ModelType == Main_Assembly
 * Plate - if PartsName isn't PLATE
 * width - if Plate isn't Aluminum
 * Motor -  if PartsName isn't MOTOR
 * ManufactureMethod - Render only if Part
 */
    public static void main(String[] args) {
        FormatGenerator formatGenerator = new FormatGenerator();
        try {
            var s = formatGenerator.getFormat(
                    CadId.SystemNameType.SYSTEMS1,
                    CadId.ModelType.Part,
                    CadId.Version.ONE.getNumber(),
                    CadId.Version.ONE.getNumber(),
                    FormatId.PartsName.PLA,
                    null,
                    null,
                    -1,
                    FormatId.ManufactureMethod.CNC
            );
            System.out.println(s);
        } catch (IllegalArgumentException e) {
            System.err.println(e.getMessage());
        }
    }

    public String getFormat(
            CadId.SystemNameType type,
            CadId.ModelType modelType,
            String modelOrder,
            String modelVersion,
            FormatId.PartsName partsName,
            FormatId.Motor motor,
            FormatId.Plate plate,
            int width,
            FormatId.ManufactureMethod manufactureMethod
    ) {
        var space = "-";
        var format = getCadId(new CadId(type, modelType, modelOrder, modelVersion))
                + space
                + getFormatId(new FormatId(modelType, partsName, motor, plate, manufactureMethod), width);
        return format.endsWith("-") ? format.substring(0, format.length() - 1) : format;
    }

    public String getFormatId(FormatId formatId, int width) {
        if (formatId.partsName() == FormatId.PartsName.PLATE) {
            if (formatId.plate() == null || width <= 0)
                throw new IllegalArgumentException("You must provide a valid plate and width for PartsName 'PLATE'.");
        }
        if (formatId.partsName() == FormatId.PartsName.MOTOR) {
            if (formatId.motor() == null)
                throw new IllegalArgumentException("You must provide a valid motor for PartsName 'MOTOR'.");
        }
        return formatId.getFormatId(width);
    }

    public String getCadId(CadId cadId) {
        return cadId.getCadId();
    }
}
